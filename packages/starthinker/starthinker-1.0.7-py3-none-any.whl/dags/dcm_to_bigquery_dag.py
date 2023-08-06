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

CM To BigQuery

Move existing CM report into a BigQuery table.

  - Specify an account id.
  - Specify either report name or report id to move a report.
  - The most recent valid file will overwrite the table.
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
  'account': '',  # CM network id.
  'report_id': '',  # CM report id, empty if using name .
  'report_name': '',  # CM report name, empty if using id instead.
  'dataset': '',  # Dataset to be written to in BigQuery.
  'table': '',  # Table to be written to in BigQuery.
  'is_incremental_load': False,  # Clear data in destination table during this report's time period, then append report data to existing table.
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
            'order': 0
          }
        },
        'out': {
          'bigquery': {
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
                'description': 'Dataset to be written to in BigQuery.',
                'kind': 'string',
                'name': 'dataset',
                'order': 5
              }
            },
            'header': True,
            'is_incremental_load': {
              'field': {
                'default': False,
                'description': "Clear data in destination table during this report's time period, then append report data to existing table.",
                'kind': 'boolean',
                'name': 'is_incremental_load',
                'order': 7
              }
            },
            'table': {
              'field': {
                'default': '',
                'description': 'Table to be written to in BigQuery.',
                'kind': 'string',
                'name': 'table',
                'order': 6
              }
            }
          }
        },
        'report': {
          'account': {
            'field': {
              'default': '',
              'description': 'CM network id.',
              'kind': 'integer',
              'name': 'account',
              'order': 2
            }
          },
          'name': {
            'field': {
              'default': '',
              'description': 'CM report name, empty if using id instead.',
              'kind': 'string',
              'name': 'report_name',
              'order': 4
            }
          },
          'report_id': {
            'field': {
              'default': '',
              'description': 'CM report id, empty if using name .',
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

DAG_FACTORY = DAG_Factory('dcm_to_bigquery', RECIPE, INPUTS)
DAG = DAG_FACTORY.generate()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
