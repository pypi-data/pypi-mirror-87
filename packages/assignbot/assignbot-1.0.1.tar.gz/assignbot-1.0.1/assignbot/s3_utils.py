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
from io import BytesIO

import boto3


def get_client():
    endpoint_url = os.getenv("S3_ENDPOINT_URL")
    return boto3.client("s3", endpoint_url=endpoint_url)


def get_bucket_name():
    return os.getenv("S3_BUCKET_NAME")


def download_file(key):
    client = get_client()
    bucket = get_bucket_name()
    return client.get_object(Bucket=bucket, Key=key)["Body"]


def upload_file(key, content):
    client = get_client()
    bucket = get_bucket_name()
    return client.upload_fileobj(BytesIO(content), Bucket=bucket, Key=key)
