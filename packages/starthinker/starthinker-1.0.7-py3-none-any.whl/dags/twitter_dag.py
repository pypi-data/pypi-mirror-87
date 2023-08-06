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

Twitter Targeting

Adjusts line item settings based on Twitter hashtags and locations specified in a sheet.

  - Click <b>Run Now</b> and a sheet called <b>Twitter Targeting UNDEFINED</b> will be generated with a tab called <b>Twitter Triggers</b>.
  - Follow instructions on the sheets tab to provide triggers and lineitems.
  - Click <b>Run Now</b> again, trends are downloaded and triggered.
  - Or give these intructions to the client.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'recipe_slug': '',  # Place where tables will be created in BigQuery.
  'auth_read': 'user',  # Credentials used for reading data.
  'recipe_project': '',  # Place where tables will be created in BigQuery.
  'auth_write': 'service',  # Credentials used for writing data.
  'recipe_name': '',  # Name of sheet where Line Item settings will be read from.
  'twitter_secret': '',  # Twitter API secret token.
  'twitter_key': '',  # Twitter API key token.
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
            'name': 'recipe_slug',
            'order': 1
          }
        },
        'description': 'Create a dataset where data will be combined and transfored for upload.'
      }
    },
    {
      'sheets': {
        'auth': {
          'field': {
            'default': 'user',
            'description': 'Credentials used for reading data.',
            'kind': 'authentication',
            'name': 'auth_read',
            'order': 0
          }
        },
        'description': 'Read mapping of hash tags to line item toggles from sheets.',
        'out': {
          'bigquery': {
            'dataset': {
              'field': {
                'description': 'Place where tables will be created in BigQuery.',
                'kind': 'string',
                'name': 'recipe_slug'
              }
            },
            'schema': [
              {
                'mode': 'REQUIRED',
                'name': 'Location',
                'type': 'STRING'
              },
              {
                'mode': 'REQUIRED',
                'name': 'WOEID',
                'type': 'INTEGER'
              },
              {
                'mode': 'REQUIRED',
                'name': 'Hashtag',
                'type': 'STRING'
              },
              {
                'mode': 'REQUIRED',
                'name': 'Line_Item_Id',
                'type': 'INTEGER'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Line_Item_Name',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Line_Item_Status',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Line_Item_Start_Date',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Line_Item_End_Date',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Line_Item_Budget_Type',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Line_Item_Budget_Amount',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Line_Item_Pacing',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Line_Item_Pacing_Rate',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Line_Item_Pacing_Amount',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Line_Item_Frequency_Enabled',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Line_Item_Frequency_Exposures',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Line_Item_Frequency_Period',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Line_Item_Frequency_Amount',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Bid_Price',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Partner_Revenue_Model',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Partner_Revenue_Amount',
                'type': 'STRING'
              }
            ],
            'table': 'Twitter_Triggers'
          }
        },
        'range': 'A8:T',
        'sheet': {
          'field': {
            'default': '',
            'description': 'Name of sheet where Line Item settings will be read from.',
            'kind': 'string',
            'name': 'recipe_name',
            'order': 2,
            'prefix': 'Twitter Targeting For '
          }
        },
        'tab': 'Twitter Triggers',
        'template': {
          'sheet': 'https://docs.google.com/spreadsheets/d/1iYCGa2NKOZiL2mdT4yiDfV_SWV9C7SUosXdIr4NAEXE/edit?usp=sharing',
          'tab': 'Twitter Triggers'
        }
      }
    },
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
        'description': 'Read trends from Twitter and place into BigQuery.',
        'key': {
          'field': {
            'default': '',
            'description': 'Twitter API key token.',
            'kind': 'string',
            'name': 'twitter_key',
            'order': 4
          }
        },
        'out': {
          'bigquery': {
            'dataset': {
              'field': {
                'description': 'Place where tables will be created in BigQuery.',
                'kind': 'string',
                'name': 'recipe_slug'
              }
            },
            'table': 'Twitter_Trends_Place'
          }
        },
        'secret': {
          'field': {
            'default': '',
            'description': 'Twitter API secret token.',
            'kind': 'string',
            'name': 'twitter_secret',
            'order': 3
          }
        },
        'trends': {
          'places': {
            'bigquery': {
              'dataset': {
                'field': {
                  'description': 'Place where tables will be created in BigQuery.',
                  'kind': 'string',
                  'name': 'recipe_slug'
                }
              },
              'legacy': False,
              'parameters': {
                'dataset': {
                  'field': {
                    'description': 'Place where tables will be created in BigQuery.',
                    'kind': 'string',
                    'name': 'recipe_slug'
                  }
                }
              },
              'query': 'SELECT WOEID FROM {dataset}.Twitter_Triggers'
            },
            'single_cell': True
          }
        }
      }
    },
    {
      'lineitem': {
        'auth': {
          'field': {
            'default': 'user',
            'description': 'Credentials used for reading data.',
            'kind': 'authentication',
            'name': 'auth_read',
            'order': 0
          }
        },
        'description': 'Read current lineitem settings from DV360 into BigQuery, so it can be joined with Twitter analysis.',
        'read': {
          'line_items': {
            'bigquery': {
              'dataset': {
                'field': {
                  'description': 'Place where tables will be created in BigQuery.',
                  'kind': 'string',
                  'name': 'recipe_slug'
                }
              },
              'parameters': {
                'dataset': {
                  'field': {
                    'description': 'Place where tables will be created in BigQuery.',
                    'kind': 'string',
                    'name': 'recipe_slug'
                  }
                }
              },
              'query': 'SELECT Line_Item_Id FROM {dataset}.Twitter_Triggers'
            },
            'single_cell': True
          },
          'out': {
            'bigquery': {
              'dataset': {
                'field': {
                  'description': 'Place where tables will be created in BigQuery.',
                  'kind': 'string',
                  'name': 'recipe_slug'
                }
              },
              'table': 'LineItem_Reads'
            }
          }
        }
      }
    },
    {
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
        'description': 'Get all triggered lineitmes from sheet, if they have a keyword match in twitter, take the triger values, else take the default values (default>trigger).  Take all non-null values from trigger and overlay over current DV360 values. Will be used to upload to DV360.',
        'from': {
          'legacy': False,
          'parameters': {
            'dataset': {
              'field': {
                'description': 'Place where tables will be created in BigQuery.',
                'kind': 'string',
                'name': 'recipe_slug'
              }
            },
            'project': {
              'field': {
                'description': 'Place where tables will be created in BigQuery.',
                'kind': 'string',
                'name': 'recipe_project'
              }
            }
          },
          'query': "SELECT o.Line_Item_Id AS Line_Item_Id, o.Partner_Name AS Partner_Name, o.Partner_Id AS Partner_Id, o.Advertiser_Name AS Advertiser_Name, o.IO_Name AS IO_Name, IFNULL(t.Line_Item_Name, o.Line_Item_Name) AS Line_Item_Name, o.Line_Item_Timestamp AS Line_Item_Timestamp , IFNULL(t.Line_Item_Status, o.Line_Item_Status) AS Line_Item_Status, o.IO_Start_Date AS IO_Start_Date, o.IO_End_Date AS IO_End_Date, o.IO_Budget_Type AS IO_Budget_Type, o.IO_Budget_Amount AS IO_Budget_Amount, o.IO_Pacing AS IO_Pacing, o.IO_Pacing_Rate AS IO_Pacing_Rate, o.IO_Pacing_Amount AS IO_Pacing_Amount, IFNULL(t.Line_Item_Start_Date, o.Line_Item_Start_Date) AS Line_Item_Start_Date, IFNULL(t.Line_Item_End_Date, o.Line_Item_End_Date) AS Line_Item_End_Date, IFNULL(t.Line_Item_Budget_Type, o.Line_Item_Budget_Type) AS Line_Item_Budget_Type, IFNULL(t.Line_Item_Budget_Amount, o.Line_Item_Budget_Amount) AS Line_Item_Budget_Amount, IFNULL(t.Line_Item_Pacing, o.Line_Item_Pacing) AS Line_Item_Pacing, IFNULL(t.Line_Item_Pacing_Rate, o.Line_Item_Pacing_Rate) AS Line_Item_Pacing_Rate, IFNULL(t.Line_Item_Pacing_Amount, o.Line_Item_Pacing_Amount) AS Line_Item_Pacing_Amount, IFNULL(t.Line_Item_Frequency_Enabled, o.Line_Item_Frequency_Enabled) AS Line_Item_Frequency_Enabled, IFNULL(t.Line_Item_Frequency_Exposures, o.Line_Item_Frequency_Exposures) AS Line_Item_Frequency_Exposures, IFNULL(t.Line_Item_Frequency_Period, o.Line_Item_Frequency_Period) AS Line_Item_Frequency_Period, IFNULL(t.Line_Item_Frequency_Amount, o.Line_Item_Frequency_Amount) AS Line_Item_Frequency_Amount, IFNULL(t.Bid_Price, o.Bid_Price) AS Bid_Price, IFNULL(t.Partner_Revenue_Model, o.Partner_Revenue_Model) AS Partner_Revenue_Model, IFNULL(t.Partner_Revenue_Amount, o.Partner_Revenue_Amount) AS Partner_Revenue_Amount, o.Current_Audience_Targeting_Ids AS Current_Audience_Targeting_Ids , o.Current_Audience_Targeting_Names AS Current_Audience_Targeting_Names FROM `{project}.{dataset}.LineItem_Reads` AS o LEFT JOIN ( SELECT Line_Item_Id, ANY_VALUE(SPLIT(Line_Item_Name, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))]) AS Line_Item_Name, ANY_VALUE(SPLIT(Line_Item_Status, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))]) AS Line_Item_Status, ANY_VALUE(SPLIT(Line_Item_Start_Date, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))]) AS Line_Item_Start_Date, ANY_VALUE(SPLIT(Line_Item_End_Date, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))]) AS Line_Item_End_Date, ANY_VALUE(SPLIT(Line_Item_Budget_Type, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))]) AS Line_Item_Budget_Type, ANY_VALUE(CAST(SPLIT(Line_Item_Budget_Amount, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))] AS FLOAT64)) AS Line_Item_Budget_Amount, ANY_VALUE(SPLIT(Line_Item_Pacing, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))]) AS Line_Item_Pacing, ANY_VALUE(SPLIT(Line_Item_Pacing_Rate, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))]) AS Line_Item_Pacing_Rate, ANY_VALUE(CAST(SPLIT(Line_Item_Pacing_Amount, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))] AS FLOAT64)) AS Line_Item_Pacing_Amount, ANY_VALUE(CAST(SPLIT(Line_Item_Frequency_Enabled, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))] AS BOOL)) AS Line_Item_Frequency_Enabled, ANY_VALUE(SPLIT(Line_Item_Frequency_Exposures, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))]) AS Line_Item_Frequency_Exposures, ANY_VALUE(SPLIT(Line_Item_Frequency_Period, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))]) AS Line_Item_Frequency_Period, ANY_VALUE(CAST(SPLIT(Line_Item_Frequency_Amount, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))] AS INT64)) AS Line_Item_Frequency_Amount, ANY_VALUE(CAST(SPLIT(Bid_Price, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))] AS FLOAT64)) AS Bid_Price, ANY_VALUE(SPLIT(Partner_Revenue_Model, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))]) AS Partner_Revenue_Model, ANY_VALUE(CAST(SPLIT(Partner_Revenue_Amount, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))] AS FLOAT64)) AS Partner_Revenue_Amount FROM ( SELECT WOEID, Hashtag, Line_Item_Id, Line_Item_Name, Line_Item_Status, Line_Item_Start_Date, Line_Item_End_Date, Line_Item_Budget_Type, Line_Item_Budget_Amount, Line_Item_Pacing, Line_Item_Pacing_Rate, Line_Item_Pacing_Amount, Line_Item_Frequency_Enabled, Line_Item_Frequency_Exposures, Line_Item_Frequency_Period, Line_Item_Frequency_Amount, Bid_Price, Partner_Revenue_Model, Partner_Revenue_Amount, CONCAT(CAST(WOEID AS STRING), LOWER(Hashtag)) IN (SELECT CONCAT(CAST(WOEID AS STRING), LOWER(REPLACE(name, '#', ''))) FROM `{project}.{dataset}.Twitter_Trends_Place` GROUP BY 1) AS Triggered FROM `{project}.{dataset}.Twitter_Triggers`) GROUP BY 1) AS t ON o.Line_Item_Id=t.Line_Item_Id;"
        },
        'to': {
          'dataset': {
            'field': {
              'description': 'Place where tables will be created in BigQuery.',
              'kind': 'string',
              'name': 'recipe_slug'
            }
          },
          'view': 'LineItem_Writes'
        }
      }
    },
    {
      'lineitem': {
        'auth': {
          'field': {
            'default': 'user',
            'description': 'Credentials used for reading data.',
            'kind': 'authentication',
            'name': 'auth_read',
            'order': 0
          }
        },
        'description': 'Write lineitem settings to DV360 after transformation.',
        'write': {
          'bigquery': {
            'dataset': {
              'field': {
                'description': 'Place where tables will be created in BigQuery.',
                'kind': 'string',
                'name': 'recipe_slug'
              }
            },
            'legacy': False,
            'parameters': {
              'dataset': {
                'field': {
                  'description': 'Place where tables will be created in BigQuery.',
                  'kind': 'string',
                  'name': 'recipe_slug'
                }
              }
            },
            'query': 'Select * FROM {dataset}.LineItem_Writes'
          },
          'dry_run': False
        }
      }
    }
  ]
}

DAG_FACTORY = DAG_Factory('twitter', RECIPE, INPUTS)
DAG = DAG_FACTORY.generate()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
