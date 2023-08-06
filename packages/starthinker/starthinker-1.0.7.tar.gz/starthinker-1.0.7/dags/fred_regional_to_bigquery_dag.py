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

Federal Reserve Regional Data

Download federal reserve region.

  - Specify the values for a <a href='https://research.stlouisfed.org/docs/api/geofred/regional_data.html' target='_blank'>Fred observations API call</a>.
  - A table will appear in the dataset.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth': 'service',  # Credentials used for writing data.
  'fred_api_key': '',  # 32 character alpha-numeric lowercase string.
  'fred_series_group': '',  # The ID for a group of seriess found in GeoFRED.
  'fred_region_type': 'county',  # The region you want want to pull data for.
  'fred_units': 'lin',  # A key that indicates a data value transformation.
  'fred_frequency': '',  # An optional parameter that indicates a lower frequency to aggregate values to.
  'fred_season': 'SA',  # The seasonality of the series group.
  'fred_aggregation_method': 'avg',  # A key that indicates the aggregation method used for frequency aggregation.
  'project': '',  # Existing BigQuery project.
  'dataset': '',  # Existing BigQuery dataset.
}

RECIPE = {
  'tasks': [
    {
      'fred': {
        'api_key': {
          'field': {
            'default': '',
            'description': '32 character alpha-numeric lowercase string.',
            'kind': 'string',
            'name': 'fred_api_key',
            'order': 1
          }
        },
        'auth': {
          'field': {
            'default': 'service',
            'description': 'Credentials used for writing data.',
            'kind': 'authentication',
            'name': 'auth',
            'order': 0
          }
        },
        'frequency': {
          'field': {
            'choices': [
              '',
              'd',
              'w',
              'bw',
              'm',
              'q',
              'sa',
              'a',
              'wef',
              'weth',
              'wew',
              'wetu',
              'wem',
              'wesu',
              'wesa',
              'bwew',
              'bwem'
            ],
            'default': '',
            'description': 'An optional parameter that indicates a lower frequency to aggregate values to.',
            'kind': 'choice',
            'name': 'fred_frequency',
            'order': 4
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
                'order': 11
              }
            },
            'project': {
              'field': {
                'default': '',
                'description': 'Existing BigQuery project.',
                'kind': 'string',
                'name': 'project',
                'order': 10
              }
            }
          }
        },
        'region_type': {
          'field': {
            'choices': [
              'bea',
              'msa',
              'frb',
              'necta',
              'state',
              'country',
              'county',
              'censusregion'
            ],
            'default': 'county',
            'description': 'The region you want want to pull data for.',
            'kind': 'choice',
            'name': 'fred_region_type',
            'order': 3
          }
        },
        'regions': [
          {
            'aggregation_method': {
              'field': {
                'choices': [
                  'avg',
                  'sum',
                  'eop'
                ],
                'default': 'avg',
                'description': 'A key that indicates the aggregation method used for frequency aggregation.',
                'kind': 'choice',
                'name': 'fred_aggregation_method',
                'order': 5
              }
            },
            'season': {
              'field': {
                'choices': [
                  'SA',
                  'NSA',
                  'SSA'
                ],
                'default': 'SA',
                'description': 'The seasonality of the series group.',
                'kind': 'choice',
                'name': 'fred_season',
                'order': 4
              }
            },
            'series_group': {
              'field': {
                'default': '',
                'description': 'The ID for a group of seriess found in GeoFRED.',
                'kind': 'string',
                'name': 'fred_series_group',
                'order': 2
              }
            },
            'units': {
              'field': {
                'choices': [
                  'lin',
                  'chg',
                  'ch1',
                  'pch',
                  'pc1',
                  'pca',
                  'cch',
                  'cca',
                  'log'
                ],
                'default': 'lin',
                'description': 'A key that indicates a data value transformation.',
                'kind': 'choice',
                'name': 'fred_units',
                'order': 3
              }
            }
          }
        ]
      }
    }
  ]
}

DAG_FACTORY = DAG_Factory('fred_regional_to_bigquery', RECIPE, INPUTS)
DAG = DAG_FACTORY.generate()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
