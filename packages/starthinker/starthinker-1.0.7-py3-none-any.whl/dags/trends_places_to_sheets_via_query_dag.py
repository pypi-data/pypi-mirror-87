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

Trends Places To Sheets Via Query

Move using a WOEID query.

  - Provide <a href='https://apps.twitter.com/' target='_blank'>Twitter credentials</a>.
  - Provide BigQuery WOEID source query.
  - Specify Sheet url and tab to write API call results to.
  - Writes: WOEID, Name, Url, Promoted_Content, Query, Tweet_Volume
  - Note Twitter API is rate limited to 15 requests per 15 minutes. So keep WOEID lists short.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_write': 'service',  # Credentials used for writing data.
  'secret': '',
  'key': '',
  'places_dataset': '',
  'places_query': '',
  'places_legacy': False,
  'destination_sheet': '',
  'destination_tab': '',
}

RECIPE = {
  'tasks': [
    {
      'twitter': {
        'auth': {
          'field': {
            'default': 'service',
            'description': 'Credentials used for writing data.',
            'kind': 'authentication',
            'name': 'auth_write',
            'order': 1
          }
        },
        'key': {
          'field': {
            'default': '',
            'kind': 'string',
            'name': 'key',
            'order': 2
          }
        },
        'out': {
          'sheets': {
            'range': 'A1',
            'sheet': {
              'field': {
                'default': '',
                'kind': 'string',
                'name': 'destination_sheet',
                'order': 6
              }
            },
            'tab': {
              'field': {
                'default': '',
                'kind': 'string',
                'name': 'destination_tab',
                'order': 7
              }
            }
          }
        },
        'secret': {
          'field': {
            'default': '',
            'kind': 'string',
            'name': 'secret',
            'order': 1
          }
        },
        'trends': {
          'places': {
            'bigquery': {
              'dataset': {
                'field': {
                  'default': '',
                  'kind': 'string',
                  'name': 'places_dataset',
                  'order': 3
                }
              },
              'legacy': {
                'field': {
                  'default': False,
                  'kind': 'boolean',
                  'name': 'places_legacy',
                  'order': 5
                }
              },
              'query': {
                'field': {
                  'default': '',
                  'kind': 'string',
                  'name': 'places_query',
                  'order': 4
                }
              }
            },
            'single_cell': True
          }
        }
      }
    }
  ]
}

DAG_FACTORY = DAG_Factory('trends_places_to_sheets_via_query', RECIPE, INPUTS)
DAG = DAG_FACTORY.generate()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
