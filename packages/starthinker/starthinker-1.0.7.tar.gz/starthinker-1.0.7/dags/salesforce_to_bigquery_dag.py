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

Salesforce To BigQuery

Move query results into a BigQuery table.

  - Specify <a href='https://developer.salesforce.com/' target='_blank'>Salesforce</a> credentials.
  - Specify the query youd like to execute.
  - Specify a <a href='https://cloud.google.com/bigquery/docs/schemas#creating_a_json_schema_file' target='_blank'>SCHEMA</a> for that query ( optional ).

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'client': '',  # Retrieve from a Salesforce App.
  'domain': 'login.salesforce.com',  # Retrieve from a Salesforce Domain.
  'password': '',  # Your Salesforce login password.
  'query': '',  # The query to run in Salesforce.
  'secret': '',  # Retrieve from a Salesforce App.
  'username': '',  # Your Salesforce user email.
  'auth_read': 'user',  # Credentials used for reading data.
  'dataset': '',  # Existing BigQuery dataset.
  'table': '',  # Table to create from this report.
  'schema': '[]',  # Schema provided in JSON list format or empty list.
}

RECIPE = {
  'tasks': [
    {
      'salesforce': {
        'auth': {
          'field': {
            'default': 'user',
            'description': 'Credentials used for reading data.',
            'kind': 'authentication',
            'name': 'auth_read',
            'order': 1
          }
        },
        'client': {
          'field': {
            'default': '',
            'description': 'Retrieve from a Salesforce App.',
            'kind': 'string',
            'name': 'client'
          }
        },
        'domain': {
          'field': {
            'default': 'login.salesforce.com',
            'description': 'Retrieve from a Salesforce Domain.',
            'kind': 'string',
            'name': 'domain'
          }
        },
        'out': {
          'bigquery': {
            'dataset': {
              'field': {
                'default': '',
                'description': 'Existing BigQuery dataset.',
                'kind': 'string',
                'name': 'dataset',
                'order': 3
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
            'table': {
              'field': {
                'default': '',
                'description': 'Table to create from this report.',
                'kind': 'string',
                'name': 'table',
                'order': 4
              }
            }
          }
        },
        'password': {
          'field': {
            'default': '',
            'description': 'Your Salesforce login password.',
            'kind': 'password',
            'name': 'password'
          }
        },
        'query': {
          'field': {
            'default': '',
            'description': 'The query to run in Salesforce.',
            'kind': 'string',
            'name': 'query'
          }
        },
        'secret': {
          'field': {
            'default': '',
            'description': 'Retrieve from a Salesforce App.',
            'kind': 'string',
            'name': 'secret'
          }
        },
        'username': {
          'field': {
            'default': '',
            'description': 'Your Salesforce user email.',
            'kind': 'email',
            'name': 'username'
          }
        }
      }
    }
  ]
}

DAG_FACTORY = DAG_Factory('salesforce_to_bigquery', RECIPE, INPUTS)
DAG = DAG_FACTORY.generate()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
