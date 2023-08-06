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

CM Report Replicate

Replicate a report across multiple networks and advertisers.

  - Provide the name or ID of an existing report.
  - Run the recipe once to generate the input sheet called CM Replicate For UNDEFINED.
  - Enter network and advertiser ids to replicate the report.
  - Data will be written to BigQuery &gt; UNDEFINED &gt; UNDEFINED &gt; [REPORT NAME]_All

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_read': 'user',  # Credentials used for reading data.
  'recipe_name': '',  # Sheet to read ids from.
  'auth_write': 'service',  # Credentials used for writing data.
  'account': '',  # CM network id.
  'recipe_slug': '',
  'report_id': '',  # CM template report id, for template
  'report_name': '',  # CM template report name, empty if using id instead.
  'delete': False,  # Use only to reset the reports if setup changes.
  'Aggregate': False,  # Append report data to existing table, requires Date column.
}

RECIPE = {
  'tasks': [
    {
      'drive': {
        'auth': 'user',
        'copy': {
          'destination': {
            'field': {
              'default': '',
              'description': 'Name of document to deploy to.',
              'kind': 'string',
              'name': 'recipe_name',
              'order': 1,
              'prefix': 'CM Replicate For '
            }
          },
          'source': 'https://docs.google.com/spreadsheets/d/1Su3t2YUWV_GG9RD63Wa3GNANmQZswTHstFY6aDPm6qE/'
        }
      }
    },
    {
      'dataset': {
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
            'description': 'Name of Google BigQuery dataset to create.',
            'kind': 'string',
            'name': 'recipe_slug',
            'order': 2
          }
        }
      }
    },
    {
      'dcm_replicate': {
        'auth': {
          'field': {
            'default': 'user',
            'description': 'Credentials used for reading data.',
            'kind': 'authentication',
            'name': 'auth_read',
            'order': 0
          }
        },
        'in': {
          'sheet': {
            'field': {
              'default': '',
              'description': 'Sheet to read ids from.',
              'kind': 'string',
              'name': 'recipe_name',
              'order': 1,
              'prefix': 'CM Replicate For '
            }
          },
          'tab': 'Accounts'
        },
        'out': {
          'bigquery': {
            'dataset': {
              'field': {
                'default': '',
                'kind': 'string',
                'name': 'recipe_slug',
                'order': 4
              }
            },
            'is_incremental_load': {
              'field': {
                'default': False,
                'description': 'Append report data to existing table, requires Date column.',
                'kind': 'boolean',
                'name': 'Aggregate',
                'order': 7
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
              'order': 3
            }
          },
          'delete': {
            'field': {
              'default': False,
              'description': 'Use only to reset the reports if setup changes.',
              'kind': 'boolean',
              'name': 'delete',
              'order': 6
            }
          },
          'id': {
            'field': {
              'default': '',
              'description': 'CM template report id, for template',
              'kind': 'integer',
              'name': 'report_id',
              'order': 4
            }
          },
          'name': {
            'field': {
              'default': '',
              'description': 'CM template report name, empty if using id instead.',
              'kind': 'string',
              'name': 'report_name',
              'order': 5
            }
          }
        }
      }
    }
  ]
}

DAG_FACTORY = DAG_Factory('dcm_replicate_to_bigquery', RECIPE, INPUTS)
DAG = DAG_FACTORY.generate()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
