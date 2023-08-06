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

Monthly Budget Mover

Apply the previous month's budget/spend delta to the current month.  Aggregate up the budget and spend from the previous month of each category declared then apply the delta of the spend and budget equally to each Line Item under that Category.

  - No changes made can be made in DV360 from the start to the end of this process
  - Make sure there is budget information for the current and previous month's IOs in DV360
  - Make sure the provided spend report has spend data for every IO in the previous month
  - Spend report must contain 'Revenue (Adv Currency)' and 'Insertion Order ID'
  - There are no duplicate IO Ids in the categories outlined below
  - This process must be ran during the month of the budget it is updating
  - If you receive a 502 error then you must separate your jobs into two, because there is too much information being pulled in the sdf
  - Manually run this job
  - Once the job has completed go to the table for the new sdf and export to a csv
  - Take the new sdf and upload it into DV360

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'recipe_timezone': 'America/Los_Angeles',  # Timezone for report dates.
  'auth_write': 'service',  # Credentials used for writing data.
  'auth_read': 'user',  # Credentials used for reading data.
  'recipe_name': '',  # Name of report in DV360, should be unique.
  'partner_id': '',  # The sdf file types.
  'budget_categories': '{}',  # A dictionary to show which IO Ids go under which Category. {"CATEGORY1":[12345,12345,12345], "CATEGORY2":[12345,12345]}
  'filter_ids': [],  # Comma separated list of filter ids for the request.
  'excluded_ios': '',  # A comma separated list of Inserion Order Ids that should be exluded from the budget calculations
  'dataset': '',  # Dataset to be written to in BigQuery.
  'version': '5',  # The sdf version to be returned.
  'is_colab': True,  # Are you running this in Colab? (This will store the files in Colab instead of Bigquery)
}

RECIPE = {
  'setup': {
    'day': [
      'Mon',
      'Tue',
      'Wed',
      'Thu',
      'Fri',
      'Sat',
      'Sun'
    ],
    'hour': [
      2,
      4,
      6,
      8,
      10,
      12,
      14,
      16,
      18,
      20,
      22,
      24
    ]
  },
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
            'description': 'Place where tables will be created in BigQuery.',
            'kind': 'string',
            'name': 'dataset',
            'order': 1
          }
        },
        'description': 'Create a dataset where data will be combined and transfored for upload.'
      }
    },
    {
      'dbm': {
        'auth': {
          'field': {
            'default': 'user',
            'description': 'Credentials used for reading data.',
            'kind': 'authentication',
            'name': 'auth_read',
            'order': 1
          }
        },
        'delete': False,
        'report': {
          'body': {
            'metadata': {
              'dataRange': 'PREVIOUS_MONTH',
              'format': 'CSV',
              'title': {
                'field': {
                  'description': 'Name of report in DV360, should be unique.',
                  'kind': 'string',
                  'name': 'recipe_name',
                  'order': 1,
                  'prefix': 'Monthly_Budget_Mover_'
                }
              }
            },
            'params': {
              'groupBys': [
                'FILTER_ADVERTISER_CURRENCY',
                'FILTER_INSERTION_ORDER'
              ],
              'metrics': [
                'METRIC_REVENUE_ADVERTISER'
              ],
              'type': 'TYPE_GENERAL'
            },
            'timezoneCode': {
              'field': {
                'default': 'America/Los_Angeles',
                'description': 'Timezone for report dates.',
                'kind': 'timezone',
                'name': 'recipe_timezone'
              }
            }
          },
          'filters': {
            'FILTER_ADVERTISER': {
              'values': {
                'field': {
                  'default': '',
                  'description': 'The comma separated list of Advertiser Ids.',
                  'kind': 'integer_list',
                  'name': 'filter_ids',
                  'order': 7
                }
              }
            }
          },
          'timeout': 90
        }
      }
    },
    {
      'monthly_budget_mover': {
        'auth': 'user',
        'budget_categories': {
          'field': {
            'default': '{}',
            'description': 'A dictionary to show which IO Ids go under which Category. {"CATEGORY1":[12345,12345,12345], "CATEGORY2":[12345,12345]}',
            'kind': 'json',
            'name': 'budget_categories',
            'order': 3
          }
        },
        'excluded_ios': {
          'field': {
            'description': 'A comma separated list of Inserion Order Ids that should be exluded from the budget calculations',
            'kind': 'integer_list',
            'name': 'excluded_ios',
            'order': 4
          }
        },
        'is_colab': {
          'field': {
            'default': True,
            'description': 'Are you running this in Colab? (This will store the files in Colab instead of Bigquery)',
            'kind': 'boolean',
            'name': 'is_colab',
            'order': 7
          }
        },
        'out_changes': {
          'bigquery': {
            'dataset': {
              'field': {
                'default': '',
                'description': 'Dataset that you would like your output tables to be produced in.',
                'kind': 'string',
                'name': 'dataset',
                'order': 8
              }
            },
            'disposition': 'WRITE_TRUNCATE',
            'schema': [
            ],
            'skip_rows': 0,
            'table': {
              'field': {
                'description': '',
                'kind': 'string',
                'name': 'recipe_name',
                'prefix': 'SDF_BUDGET_MOVER_LOG_'
              }
            }
          },
          'file': '/content/log.csv'
        },
        'out_new_sdf': {
          'bigquery': {
            'dataset': {
              'field': {
                'default': '',
                'description': 'Dataset that you would like your output tables to be produced in.',
                'kind': 'string',
                'name': 'dataset',
                'order': 8
              }
            },
            'disposition': 'WRITE_TRUNCATE',
            'schema': [
            ],
            'skip_rows': 0,
            'table': {
              'field': {
                'description': '',
                'kind': 'string',
                'name': 'recipe_name',
                'prefix': 'SDF_NEW_'
              }
            }
          },
          'file': '/content/new_sdf.csv'
        },
        'out_old_sdf': {
          'bigquery': {
            'dataset': {
              'field': {
                'default': '',
                'description': 'Dataset that you would like your output tables to be produced in.',
                'kind': 'string',
                'name': 'dataset',
                'order': 8
              }
            },
            'disposition': 'WRITE_TRUNCATE',
            'schema': [
            ],
            'skip_rows': 0,
            'table': {
              'field': {
                'description': '',
                'kind': 'string',
                'name': 'recipe_name',
                'prefix': 'SDF_OLD_'
              }
            }
          },
          'file': '/content/old_sdf.csv'
        },
        'report_name': {
          'field': {
            'description': 'Name of report in DV360, should be unique.',
            'kind': 'string',
            'name': 'recipe_name',
            'order': 1,
            'prefix': 'Monthly_Budget_Mover_'
          }
        },
        'sdf': {
          'auth': 'user',
          'create_single_day_table': False,
          'dataset': {
            'field': {
              'default': '',
              'description': 'Dataset to be written to in BigQuery.',
              'kind': 'string',
              'name': 'dataset',
              'order': 6
            }
          },
          'file_types': 'INSERTION_ORDER',
          'filter_type': 'FILTER_TYPE_ADVERTISER_ID',
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
          'table_suffix': '',
          'time_partitioned_table': False,
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
    }
  ]
}

DAG_FACTORY = DAG_Factory('monthly_budget_mover', RECIPE, INPUTS)
DAG = DAG_FACTORY.generate()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
