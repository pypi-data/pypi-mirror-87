###########################################################################
#
#  Copyright 2020 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
###########################################################################

'''
--------------------------------------------------------------

Before running this Airflow module...

  Install StarThinker in cloud composer ( recommended ):

    From Release: pip install starthinker
    From Open Source: pip install git+https://github.com/google/starthinker

  Or push local code to the cloud composer plugins directory ( if pushing local code changes ):

    source install/deploy.sh
    4) Composer Menu
    l) Install All

--------------------------------------------------------------

  If any recipe task has "auth" set to "user" add user credentials:

    1. Ensure an RECIPE['setup']['auth']['user'] = [User Credentials JSON]

  OR

    1. Visit Airflow UI > Admin > Connections.
    2. Add an Entry called "starthinker_user", fill in the following fields. Last step paste JSON from authentication.
      - Conn Type: Google Cloud Platform
      - Project: Get from https://github.com/google/starthinker/blob/master/tutorials/cloud_project.md
      - Keyfile JSON: Get from: https://github.com/google/starthinker/blob/master/tutorials/deploy_commandline.md#optional-setup-user-credentials

--------------------------------------------------------------

  If any recipe task has "auth" set to "service" add service credentials:

    1. Ensure an RECIPE['setup']['auth']['service'] = [Service Credentials JSON]

  OR

    1. Visit Airflow UI > Admin > Connections.
    2. Add an Entry called "starthinker_service", fill in the following fields. Last step paste JSON from authentication.
      - Conn Type: Google Cloud Platform
      - Project: Get from https://github.com/google/starthinker/blob/master/tutorials/cloud_project.md
      - Keyfile JSON: Get from: https://github.com/google/starthinker/blob/master/tutorials/cloud_service.md

--------------------------------------------------------------

Storage To Table

Move using bucket and path prefix.

  - Specify a bucket and path prefix, * suffix is NOT required.
  - Every time the job runs it will overwrite the table.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_read': 'user',  # Credentials used for reading data.
  'bucket': '',  # Google cloud bucket.
  'auth_write': 'service',  # Credentials used for writing data.
  'path': '',  # Path prefix to read from, no * required.
  'dataset': '',  # Existing BigQuery dataset.
  'table': '',  # Table to create from this query.
  'schema': '[]',  # Schema provided in JSON list format or empty list.
}

RECIPE = {
  'tasks': [
    {
      'bigquery': {
        'auth': {
          'field': {
            'default': 'user',
            'description': 'Credentials used for reading data.',
            'kind': 'authentication',
            'name': 'auth_read',
            'order': 1
          }
        },
        'from': {
          'bucket': {
            'field': {
              'default': '',
              'description': 'Google cloud bucket.',
              'kind': 'string',
              'name': 'bucket',
              'order': 1
            }
          },
          'path': {
            'field': {
              'default': '',
              'description': 'Path prefix to read from, no * required.',
              'kind': 'string',
              'name': 'path',
              'order': 2
            }
          }
        },
        'schema': {
          'field': {
            'default': '[]',
            'description': 'Schema provided in JSON list format or empty list.',
            'kind': 'json',
            'name': 'schema',
            'order': 5
          }
        },
        'to': {
          'auth': {
            'field': {
              'default': 'service',
              'description': 'Credentials used for writing data.',
              'kind': 'authentication',
              'name': 'auth_write',
              'order': 1
            }
          },
          'dataset': {
            'field': {
              'default': '',
              'description': 'Existing BigQuery dataset.',
              'kind': 'string',
              'name': 'dataset',
              'order': 3
            }
          },
          'table': {
            'field': {
              'default': '',
              'description': 'Table to create from this query.',
              'kind': 'string',
              'name': 'table',
              'order': 4
            }
          }
        }
      }
    }
  ]
}

DAG_FACTORY = DAG_Factory('bigquery_storage', RECIPE, INPUTS)
DAG = DAG_FACTORY.generate()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
