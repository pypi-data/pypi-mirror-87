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

Census Data Normalized

Convert given census table to percent of population, normalizing it.

  - Specify the geography, year, and span that make up the <a href='https://pantheon.corp.google.com/bigquery?redirect_from_classic=true&p=bigquery-public-data&d=census_bureau_acs&page=dataset' target='_blank'>census table names</a>.
  - Not every combination of geography, year, and span exists or contains all the required fields.
  - Every time the query runs it will overwrite the table.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth': 'service',  # Credentials used for writing data.
  'census_geography': 'zip_codes',  # Census table to get data from.
  'census_year': '2018',  # Census table to get data from.
  'census_span': '5yr',  # Census table to get data from.
  'dataset': '',  # Existing BigQuery dataset.
  'type': 'table',  # Write Census_Percent as table or view.
}

RECIPE = {
  'tasks': [
    {
      'census': {
        'auth': {
          'field': {
            'default': 'service',
            'description': 'Credentials used for writing data.',
            'kind': 'authentication',
            'name': 'auth',
            'order': 0
          }
        },
        'normalize': {
          'census_geography': {
            'field': {
              'choices': [
                'zip_codes',
                'state',
                'zcta5',
                'schooldistrictunified',
                'puma',
                'place',
                'county',
                'congressionaldistrict',
                'censustract',
                'cbsa'
              ],
              'default': 'zip_codes',
              'description': 'Census table to get data from.',
              'kind': 'choice',
              'name': 'census_geography',
              'order': 1
            }
          },
          'census_span': {
            'field': {
              'choices': [
                '1yr',
                '3yr',
                '5yr'
              ],
              'default': '5yr',
              'description': 'Census table to get data from.',
              'kind': 'choice',
              'name': 'census_span',
              'order': 3
            }
          },
          'census_year': {
            'field': {
              'choices': [
                2018,
                2017,
                2016,
                2015,
                2014,
                2013,
                2012,
                2011,
                2010,
                2009,
                2008,
                2007
              ],
              'default': '2018',
              'description': 'Census table to get data from.',
              'kind': 'choice',
              'name': 'census_year',
              'order': 2
            }
          }
        },
        'to': {
          'dataset': {
            'field': {
              'default': '',
              'description': 'Existing BigQuery dataset.',
              'kind': 'string',
              'name': 'dataset',
              'order': 4
            }
          },
          'type': {
            'field': {
              'choices': [
                'table',
                'view'
              ],
              'default': 'table',
              'description': 'Write Census_Percent as table or view.',
              'kind': 'choice',
              'name': 'type',
              'order': 5
            }
          }
        }
      }
    }
  ]
}

DAG_FACTORY = DAG_Factory('bigquery_census_normalize', RECIPE, INPUTS)
DAG = DAG_FACTORY.generate()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
