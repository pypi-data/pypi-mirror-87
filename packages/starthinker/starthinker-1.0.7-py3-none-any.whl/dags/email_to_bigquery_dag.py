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

Email Fetch

Import emailed CM report, Dv360 report, csv, or excel into a BigQuery table.

  - The person executing this recipe must be the recipient of the email.
  - Give a regular expression to match the email subject, link or attachment.
  - The data downloaded will overwrite the table specified.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_read': 'user',  # Credentials used for reading data.
  'email_from': '',  # Must match from field.
  'email_to': '',  # Must match to field.
  'subject': '',  # Regular expression to match subject.
  'link': '',  # Regular expression to match email.
  'attachment': '',  # Regular expression to match atttachment.
  'dataset': '',  # Existing dataset in BigQuery.
  'table': '',  # Name of table to be written to.
  'dbm_schema': '[]',  # Schema provided in JSON list format or empty list.
  'is_incremental_load': False,  # Append report data to table based on date column, de-duplicates.
}

RECIPE = {
  'tasks': [
    {
      'email': {
        'auth': {
          'field': {
            'default': 'user',
            'description': 'Credentials used for reading data.',
            'kind': 'authentication',
            'name': 'auth_read',
            'order': 1
          }
        },
        'out': {
          'bigquery': {
            'dataset': {
              'field': {
                'default': '',
                'description': 'Existing dataset in BigQuery.',
                'kind': 'string',
                'name': 'dataset',
                'order': 6
              }
            },
            'is_incremental_load': {
              'field': {
                'default': False,
                'description': 'Append report data to table based on date column, de-duplicates.',
                'kind': 'boolean',
                'name': 'is_incremental_load',
                'order': 9
              }
            },
            'schema': {
              'field': {
                'default': '[]',
                'description': 'Schema provided in JSON list format or empty list.',
                'kind': 'json',
                'name': 'dbm_schema',
                'order': 8
              }
            },
            'table': {
              'field': {
                'default': '',
                'description': 'Name of table to be written to.',
                'kind': 'string',
                'name': 'table',
                'order': 7
              }
            }
          }
        },
        'read': {
          'attachment': {
            'field': {
              'default': '',
              'description': 'Regular expression to match atttachment.',
              'kind': 'string',
              'name': 'attachment',
              'order': 5
            }
          },
          'from': {
            'field': {
              'default': '',
              'description': 'Must match from field.',
              'kind': 'string',
              'name': 'email_from',
              'order': 1
            }
          },
          'link': {
            'field': {
              'default': '',
              'description': 'Regular expression to match email.',
              'kind': 'string',
              'name': 'link',
              'order': 4
            }
          },
          'subject': {
            'field': {
              'default': '',
              'description': 'Regular expression to match subject.',
              'kind': 'string',
              'name': 'subject',
              'order': 3
            }
          },
          'to': {
            'field': {
              'default': '',
              'description': 'Must match to field.',
              'kind': 'string',
              'name': 'email_to',
              'order': 2
            }
          }
        }
      }
    }
  ]
}

DAG_FACTORY = DAG_Factory('email_to_bigquery', RECIPE, INPUTS)
DAG = DAG_FACTORY.generate()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
