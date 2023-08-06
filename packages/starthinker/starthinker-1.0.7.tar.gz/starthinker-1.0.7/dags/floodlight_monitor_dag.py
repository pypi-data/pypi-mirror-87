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

Floodlight Monitor

Monitor floodlight impressions specified in sheet and send email alerts.

  - Specify an account_id or account_id:subaccount_id.
  - Will copy <a href='https://docs.google.com/spreadsheets/d/1tjF5styxMvFJsNETEa5x2F5DSmqleGl71cmujB7Ier8/edit?usp=sharing'>Floodlight Monitor Sheet</a> to the sheet you specify.
  - Follow instructions on sheet.
  - Emails are sent once a day.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'dcm_account': '',  # Specify an account_id as a number.
  'auth_read': 'user',  # Credentials used for reading data.
  'sheet': '',  # Full Name or URL to Google Sheet, Floodlight Monitor tab will be added.
}

RECIPE = {
  'tasks': [
    {
      'floodlight_monitor': {
        'account': {
          'field': {
            'default': '',
            'description': 'Specify an account_id as a number.',
            'kind': 'string',
            'name': 'dcm_account',
            'order': 1
          }
        },
        'auth': {
          'field': {
            'default': 'user',
            'description': 'Credentials used for reading data.',
            'kind': 'authentication',
            'name': 'auth_read',
            'order': 1
          }
        },
        'sheet': {
          'range': 'A2:B',
          'sheet': {
            'field': {
              'default': '',
              'description': 'Full Name or URL to Google Sheet, Floodlight Monitor tab will be added.',
              'kind': 'string',
              'name': 'sheet',
              'order': 2
            }
          },
          'tab': 'Floodlight Monitor'
        },
        'template': {
          'template': {
            'range': 'A1',
            'sheet': 'https://docs.google.com/spreadsheets/d/1tjF5styxMvFJsNETEa5x2F5DSmqleGl71cmujB7Ier8/edit?usp=sharing',
            'tab': 'Floodlight Monitor'
          }
        }
      }
    }
  ]
}

DAG_FACTORY = DAG_Factory('floodlight_monitor', RECIPE, INPUTS)
DAG = DAG_FACTORY.generate()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
