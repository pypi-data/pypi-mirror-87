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

Conversion Upload Sheets

Move form Sheets to CM.

  - Specify a CM Account ID, Floodligh Activity ID and Conversion Type.
  - Include Sheets url, tab, and range, omit headers in range.
  - Columns: Ordinal, timestampMicros, encryptedUserId | encryptedUserIdCandidates | gclid | mobileDeviceId
  - Include encryption information if using encryptedUserId or encryptedUserIdCandidates.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'dcm_account': '',
  'floodlight_activity_id': '',
  'auth_read': 'user',  # Credentials used for reading data.
  'floodlight_conversion_type': 'encryptedUserId',
  'encryption_entity_id': '',
  'encryption_entity_type': 'DCM_ACCOUNT',
  'encryption_entity_source': 'DATA_TRANSFER',
  'sheet_url': '',
  'sheet_tab': '',
  'sheet_range': '',
}

RECIPE = {
  'tasks': [
    {
      'conversion_upload': {
        'account_id': {
          'field': {
            'default': '',
            'kind': 'string',
            'name': 'dcm_account',
            'order': 0
          }
        },
        'activity_id': {
          'field': {
            'default': '',
            'kind': 'integer',
            'name': 'floodlight_activity_id',
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
        'conversion_type': {
          'field': {
            'choices': [
              'encryptedUserId',
              'encryptedUserIdCandidates',
              'gclid',
              'mobileDeviceId'
            ],
            'default': 'encryptedUserId',
            'kind': 'choice',
            'name': 'floodlight_conversion_type',
            'order': 2
          }
        },
        'encryptionInfo': {
          'encryptionEntityId': {
            'field': {
              'default': '',
              'kind': 'integer',
              'name': 'encryption_entity_id',
              'order': 3
            }
          },
          'encryptionEntityType': {
            'field': {
              'choices': [
                'ADWORDS_CUSTOMER',
                'DBM_ADVERTISER',
                'DBM_PARTNER',
                'DCM_ACCOUNT',
                'DCM_ADVERTISER',
                'ENCRYPTION_ENTITY_TYPE_UNKNOWN'
              ],
              'default': 'DCM_ACCOUNT',
              'kind': 'choice',
              'name': 'encryption_entity_type',
              'order': 4
            }
          },
          'encryptionSource': {
            'field': {
              'choices': [
                'AD_SERVING',
                'DATA_TRANSFER',
                'ENCRYPTION_SCOPE_UNKNOWN'
              ],
              'default': 'DATA_TRANSFER',
              'kind': 'choice',
              'name': 'encryption_entity_source',
              'order': 5
            }
          }
        },
        'sheets': {
          'range': {
            'field': {
              'default': '',
              'kind': 'string',
              'name': 'sheet_range',
              'order': 11
            }
          },
          'tab': {
            'field': {
              'default': '',
              'kind': 'string',
              'name': 'sheet_tab',
              'order': 10
            }
          },
          'url': {
            'field': {
              'default': '',
              'kind': 'string',
              'name': 'sheet_url',
              'order': 9
            }
          }
        }
      }
    }
  ]
}

DAG_FACTORY = DAG_Factory('conversion_upload_from_sheets', RECIPE, INPUTS)
DAG = DAG_FACTORY.generate()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
