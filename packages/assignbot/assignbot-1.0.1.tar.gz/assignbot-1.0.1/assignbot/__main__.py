#!/usr/bin/env python3
# coding: utf-8
#
# copyright 2020-2020 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of assignbot.
#
# Assignbot is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# Assignbot is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with assignbot.  If not, see <http://www.gnu.org/licenses/>.

import os
from argparse import ArgumentParser
from random import choice, shuffle
from datetime import datetime, timedelta, timezone

import yaml
import pandas as pd
from gitlab import Gitlab
from gitlab.exceptions import GitlabHttpError

from assignbot.s3_utils import download_file, upload_file

TO_REVIEW_LABEL = "To Review"
REVIEW_ACCESS_LEVEL = 30  # developper
DO_NOT_REVIEW_TAG = "no-assignbot"

STATE_FILENAME = "auto_assigned_reviewers.csv"
PENDING_MR_MESSAGE = """\
Dear contributors,

It seems that there hasn't been any activity concerning this merge request for
some time.

Do you think it should still be merged?

Thank you for your time.
"""


class ReviewAssigner:
    def __init__(self, gitlab_url, gitlab_token, users_preferences_filepath):
        self.cnx = Gitlab(gitlab_url, gitlab_token)
        self.user_preferences = self._load_users_preferences(users_preferences_filepath)
        self.review_states = self._load_review_states()

    def _load_users_preferences(self, users_preferences_filepath):
        with open(users_preferences_filepath) as fobj:
            state = yaml.load(fobj, Loader=yaml.Loader)
        return state or {}

    def _load_review_states(self):
        try:
            return pd.read_csv(
                download_file(STATE_FILENAME),
                index_col=0,
                parse_dates=[
                    2,
                ],
            )
        except Exception:  # XXX
            df = pd.DataFrame([], columns=["username", "datetime", "mr_url"])
            df.datetime = pd.to_datetime(df.datetime)
            return df

    def save_review_states(self):
        upload_file(STATE_FILENAME, self.review_states.to_csv().encode("utf-8"))

    def _get_user_nb_auto_review_since(self, username, since):
        oldest_date = datetime.now() - since
        user_reviews = self.review_states.query(f"username == '{username}'")
        return sum(user_reviews.datetime > oldest_date)

    def get_user_nb_auto_review_this_day(self, username):
        return self._get_user_nb_auto_review_since(username, timedelta(hours=20))

    def get_user_nb_auto_review_this_week(self, username):
        return self._get_user_nb_auto_review_since(username, timedelta(days=6))

    def user_has_already_been_assigned_to_this_mr(self, user, merge_request):
        return self.review_states.query(
            f"username == '{user.username}' and " f"mr_url == '{merge_request.web_url}'"
        ).empty

    def user_can_review(self, user, project, merge_request):
        try:
            user_preferences = self.user_preferences[user.username]
        except KeyError:
            # the user did not specify any preferences
            # let's assume that s·he is not volunteer
            return False

        max_auto_review_per_week = user_preferences["max_auto_review_per_week"]
        max_auto_review_per_day = user_preferences["max_auto_review_per_day"]

        auto_review_this_day = self.get_user_nb_auto_review_this_day(user.username)
        auto_review_this_week = self.get_user_nb_auto_review_this_week(user.username)

        return (
            user.access_level >= REVIEW_ACCESS_LEVEL
            and user.state == "active"
            and auto_review_this_day < max_auto_review_per_day
            and auto_review_this_week < max_auto_review_per_week
            and merge_request.author["id"] != user.id
            and self.user_has_already_been_assigned_to_this_mr(user, merge_request)
        )

    def all_possible_reviewers(self, merge_request):
        project = self.cnx.projects.get(merge_request.project_id)
        members_with_review_access = (
            member
            for member in project.members.all(all=True, as_list=False)
            if self.user_can_review(member, project, merge_request)
        )

        return members_with_review_access

    def a_possible_reviewer(self, merge_request):
        return choice(list(self.all_possible_reviewers(merge_request)))

    def assign_reviewer(self, merge_request, user):
        try:
            self.cnx.http_put(
                f"/projects/{merge_request.project_id}/merge_requests/{merge_request.iid}",
                query_data={"assignee_id": user.id},
            )
        except GitlabHttpError:
            print(
                f"ERROR: no permission to assign a reviewer to {merge_request.title}"
                f" ({merge_request.web_url})"
            )
            return

        self.review_states.loc[len(self.review_states)] = (
            user.username,
            datetime.now(),
            merge_request.web_url,
        )
        print(f"{user.name} has been assigned to {merge_request.title}")

    def _all_reviews(self, assignee_id="None"):
        merge_requests = self.cnx.mergerequests.list(
            labels=TO_REVIEW_LABEL,
            state="opened",
            wip="no",
            scope="all",
            assignee_id=assignee_id,
            all=True,
        )

        merge_requests.extend(
            self.cnx.mergerequests.list(
                labels="None",
                state="opened",
                wip="no",
                scope="all",
                assignee_id=assignee_id,
                all=True,
            )
        )

        shuffle(merge_requests)

        for merge_request in merge_requests:
            if merge_request.work_in_progress:
                # double check that the MR is not WIP.
                # it seems that filtering in the search parameters is not enough
                # XXX is it a Gitlab bug ?
                continue

            project = self.cnx.projects.get(merge_request.project_id)
            if DO_NOT_REVIEW_TAG in project.tag_list:
                # has the 'no-assignbot' tag. Let's assume that someone will take
                # care of this MR.
                print(
                    f"INFO: {merge_request.web_url} would need review, but it "
                    f"has the '{DO_NOT_REVIEW_TAG}' tag"
                )
                continue
            yield merge_request

    def all_reviews_to_do(self):
        return self._all_reviews(assignee_id="None")

    def all_pending_reviews_older_than(self, older_than):
        now = datetime.now(timezone.utc)
        for mr in self._all_reviews(assignee_id="Any"):
            mr_last_update = datetime.fromisoformat(
                mr.updated_at.replace("Z", "+00:00")
            )
            if mr_last_update + older_than < now:
                yield mr

    def assign_reviews(self):
        for mr in self.all_reviews_to_do():
            try:
                reviewer = self.a_possible_reviewer(mr)
            except IndexError:
                print(f"WARNING: no reviewer available for {mr.title}.")
                continue
            self.assign_reviewer(mr, reviewer)

    def notify_contributors_for_pending_reviews(self, older_than=timedelta(days=10)):
        for mr in self.all_pending_reviews_older_than(older_than):
            # we have a MergeRequest object,
            # but discussions can only be created on ProjectMergeRequest,
            # hence this gymnastic.
            # XXX what's the difference between MergeRequest and
            # ProjectMergeRequest ?
            project = self.cnx.projects.get(mr.project_id)
            project_mr = project.mergerequests.get(mr.iid)

            print(
                f"INFO: no activity on {project_mr.title} ({project_mr.web_url})"
                " for a while, let's add a friendly notification"
            )
            project_mr.discussions.create(data={"body": PENDING_MR_MESSAGE})


def main():
    parser = ArgumentParser()
    parser.add_argument("users_preferences_filepath")
    parser.add_argument("--gitlab-url", type=str, default=os.getenv("GITLAB_URL"))
    parser.add_argument("--gitlab-token", type=str, default=os.getenv("GITLAB_TOKEN"))
    args = parser.parse_args()

    assigner = ReviewAssigner(
        args.gitlab_url, args.gitlab_token, args.users_preferences_filepath
    )
    assigner.notify_contributors_for_pending_reviews()
    assigner.assign_reviews()
    assigner.save_review_states()


if __name__ == "__main__":
    main()
