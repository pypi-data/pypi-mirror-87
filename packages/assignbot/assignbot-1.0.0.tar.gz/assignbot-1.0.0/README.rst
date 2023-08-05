Automatically assign reviews
============================

This project aims to automatically assign unassigned pending
merge-requests on a gitlab/heptapod instance.

Each member of a project can be randomly assigned to a pending
merge-requests.

Assignbot assigns reviews to users, based on their preferences. Their
preferences are store in a simple yaml file. The history of the
assignment is stored in a CSV file, in a S3 storage.

The preferences file
--------------------

The users define their “review preferences” in a preferences file,
formatted in yaml.

The “preferences file” is a yaml file constructed as follow :

::

   username_1:
       max_auto_review_per_week: XXX
       max_auto_review_per_day: YYY
   username_2:
       max_auto_review_per_week: ZZZ
       max_auto_review_per_day: WWW

where ``username_1`` is the username of a gitlab user, and
``max_auto_review_per_week`` (``max_auto_review_per_day``) is the maximum
of automatically assigned review per week (per day).

The S3 storage
--------------

Assignbot uses a CSV file to keep track of users assignments. This CSV
file is stored in an S3 storage. When you execute the bot, you must
provide the following environment variables:

-  AWS_ACCESS_KEY_ID: your S3 key ID
-  AWS_SECRET_ACCESS_KEY: your S3 secret access key
-  S3_ENDPOINT_URL: your S3 endpoint url
-  S3_BUCKET_NAME: the S3 bucket to be used

Executing the bot
-----------------

Once assignbot installed, you can run it as follow :

.. code:: bash


   $ GITLAB_URL="https://your.forge.org" \
     GITLAB_TOKEN="XXX-an-api-token" \
     S3_ENDPOINT_URL="https://your.s3.storage.fr" \
     S3_BUCKET_NAME="you_bucket_name" \
     AWS_SECRET_ACCESS_KEY="your_secret_access_key" \
     AWS_ACCESS_KEY_ID="your_access_key_id" \
     python3 -m assignbot ./users_preferences.yml

and the bot should start assigning merge requests to the users.

Use case example
----------------

To use this bot, you can add a new repository on your forge with the following
``.gitlab-ci.yml`` :

.. code:: yaml

   assign:
     stage: assign
     only:
       - schedules
     variables:
         # there is a gitlab bug in the validation of AWS variables. We work
         # around it while waiting for the correction.
         # see: https://gitlab.com/gitlab-org/gitlab/-/issues/215927
         AWS_ACCESS_KEY_ID: "$_AWS_ACCESS_KEY_ID"
         AWS_SECRET_ACCESS_KEY: "$_AWS_SECRET_ACCESS_KEY"
     script:
       - pip install assignbot
       - python -m assignbot ./users_preferences.yml


This job assumes that you have defined the appropriate environment variables,
and that you have a ``users_preferences.yml`` file at the root of this
repository.

Then, you can create a new “schedule job” in gitlab, to call this job
periodically.
