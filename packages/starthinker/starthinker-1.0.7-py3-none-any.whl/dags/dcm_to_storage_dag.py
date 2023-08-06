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

CM To Storage

Move existing CM report into a Storage bucket.

  - Specify an account id.
  - Specify either report name or report id to move a report.
  - The most recent file will be moved to the bucket.
  - Schema is pulled from the official CM specification.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_read': 'user',  # Credentials used for reading data.
  'auth_write': 'service',  # Credentials used for writing data.
  'account': '',
  'report_id': '',
  'report_name': '',
  'bucket': '',
  'path': 'CM_Report',
}

RECIPE = {
  'tasks': [
    {
      'dcm': {
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
          'storage': {
            'auth': {
              'field': {
                'default': 'service',
                'description': 'Credentials used for writing data.',
                'kind': 'authentication',
                'name': 'auth_write',
                'order': 1
              }
            },
            'bucket': {
              'field': {
                'default': '',
                'kind': 'string',
                'name': 'bucket',
                'order': 5
              }
            },
            'path': {
              'field': {
                'default': 'CM_Report',
                'kind': 'string',
                'name': 'path',
                'order': 6
              }
            }
          }
        },
        'report': {
          'account': {
            'field': {
              'default': '',
              'kind': 'integer',
              'name': 'account',
              'order': 2
            }
          },
          'name': {
            'field': {
              'default': '',
              'kind': 'string',
              'name': 'report_name',
              'order': 4
            }
          },
          'report_id': {
            'field': {
              'default': '',
              'kind': 'integer',
              'name': 'report_id',
              'order': 3
            }
          }
        }
      }
    }
  ]
}

DAG_FACTORY = DAG_Factory('dcm_to_storage', RECIPE, INPUTS)
DAG = DAG_FACTORY.generate()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
