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

SDF Download

Download SDF reports into a BigQuery table.

  - Select your filter types and the filter ideas.
  - Enter the <a href='https://developers.google.com/bid-manager/v1.1/sdf/download' target='_blank'>file types</a> using commas.
  - SDF_ will be prefixed to all tables and date appended to daily tables.
  - File types take the following format: FILE_TYPE_CAMPAIGN, FILE_TYPE_AD_GROUP,...

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_write': 'service',  # Credentials used for writing data.
  'partner_id': '',  # The sdf file types.
  'file_types': [],  # The sdf file types.
  'filter_type': '',  # The filter type for the filter ids.
  'filter_ids': [],  # Comma separated list of filter ids for the request.
  'dataset': '',  # Dataset to be written to in BigQuery.
  'table_suffix': '',  # Optional: Suffix string to put at the end of the table name (Must contain alphanumeric or underscores)
  'version': '5',  # The sdf version to be returned.
  'time_partitioned_table': False,  # Is the end table a time partitioned
  'create_single_day_table': False,  # Would you like a separate table for each day? This will result in an extra table each day and the end table with the most up to date SDF.
}

RECIPE = {
  'tasks': [
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
            'description': 'Dataset to be written to in BigQuery.',
            'kind': 'string',
            'name': 'dataset',
            'order': 6
          }
        }
      }
    },
    {
      'sdf': {
        'auth': 'user',
        'create_single_day_table': {
          'field': {
            'default': False,
            'description': 'Would you like a separate table for each day? This will result in an extra table each day and the end table with the most up to date SDF.',
            'kind': 'boolean',
            'name': 'create_single_day_table',
            'order': 8
          }
        },
        'dataset': {
          'field': {
            'default': '',
            'description': 'Dataset to be written to in BigQuery.',
            'kind': 'string',
            'name': 'dataset',
            'order': 6
          }
        },
        'file_types': {
          'field': {
            'default': [
            ],
            'description': 'The sdf file types.',
            'kind': 'string_list',
            'name': 'file_types',
            'order': 2
          }
        },
        'filter_type': {
          'field': {
            'choices': [
              'FILTER_TYPE_ADVERTISER_ID',
              'FILTER_TYPE_CAMPAIGN_ID',
              'FILTER_TYPE_INSERTION_ORDER_ID',
              'FILTER_TYPE_MEDIA_PRODUCT_ID',
              'FILTER_TYPE_LINE_ITEM_ID'
            ],
            'default': '',
            'description': 'The filter type for the filter ids.',
            'kind': 'choice',
            'name': 'filter_type',
            'order': 3
          }
        },
        'partner_id': {
          'field': {
            'description': 'The sdf file types.',
            'kind': 'integer',
            'name': 'partner_id',
            'order': 1
          }
        },
        'read': {
          'filter_ids': {
            'single_cell': True,
            'values': {
              'field': {
                'default': [
                ],
                'description': 'Comma separated list of filter ids for the request.',
                'kind': 'integer_list',
                'name': 'filter_ids',
                'order': 4
              }
            }
          }
        },
        'table_suffix': {
          'field': {
            'default': '',
            'description': 'Optional: Suffix string to put at the end of the table name (Must contain alphanumeric or underscores)',
            'kind': 'string',
            'name': 'table_suffix',
            'order': 6
          }
        },
        'time_partitioned_table': {
          'field': {
            'default': False,
            'description': 'Is the end table a time partitioned',
            'kind': 'boolean',
            'name': 'time_partitioned_table',
            'order': 7
          }
        },
        'version': {
          'field': {
            'choices': [
              'SDF_VERSION_5',
              'SDF_VERSION_5_1'
            ],
            'default': '5',
            'description': 'The sdf version to be returned.',
            'kind': 'choice',
            'name': 'version',
            'order': 6
          }
        }
      }
    }
  ]
}

DAG_FACTORY = DAG_Factory('sdf_to_bigquery', RECIPE, INPUTS)
DAG = DAG_FACTORY.generate()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
