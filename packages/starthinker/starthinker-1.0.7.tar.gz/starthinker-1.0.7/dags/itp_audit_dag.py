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

ITP Audit Dashboard ( 2020 )

Dashboard that shows performance metrics across browser to see the impact of ITP.

  - Follow the instructions from <a href="https://docs.google.com/document/d/1HaRCMaBBEo0tSKwnofWNtaPjlW0ORcVHVwIRabct4fY/edit?usp=sharing" target="_blank">this document</a>

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'recipe_timezone': 'America/Los_Angeles',  # Timezone for report dates.
  'recipe_name': '',  # Name of document to deploy to.
  'auth_write': 'service',  # Credentials used for writing data.
  'recipe_slug': 'ITP_Audit_Dashboard',  # BigQuery dataset for store dashboard tables.
  'auth_read': 'user',  # Credentials used for reading data.
  'cm_account_id': '',  # Campaign Manager Account Id.
  'date_range': 'LAST_365_DAYS',  # Timeframe to run the ITP report for.
  'cm_advertiser_ids': '',  # Optional: Comma delimited list of CM advertiser ids.
  'floodlight_configuration_id': '',  # Floodlight Configuration Id for the Campaign Manager floodlight report.
  'dv360_partner_ids': '',  # Comma delimited list of DV360 Partner ids.
  'dv360_advertiser_ids': '',  # Optional: Comma delimited list of DV360 Advertiser ids.
}

RECIPE = {
  'setup': {
    'day': [
      'Mon'
    ],
    'hour': [
      3
    ]
  },
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
              'prefix': 'ITP Audit '
            }
          },
          'source': 'https://docs.google.com/spreadsheets/d/1rH_PGXOYW2mVdmAYnKbv6kcaB6lQihAyMsGtFfinnqg/'
        },
        'hour': [
        ]
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
            'default': 'ITP_Audit_Dashboard',
            'description': 'BigQuery dataset for store dashboard tables.',
            'kind': 'string',
            'name': 'recipe_slug',
            'order': 1
          }
        }
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
              'dataRange': {
                'field': {
                  'choices': [
                    'LAST_7_DAYS',
                    'LAST_14_DAYS',
                    'LAST_30_DAYS',
                    'LAST_365_DAYS',
                    'LAST_60_DAYS',
                    'LAST_7_DAYS',
                    'LAST_90_DAYS',
                    'MONTH_TO_DATE',
                    'PREVIOUS_MONTH',
                    'PREVIOUS_QUARTER',
                    'PREVIOUS_WEEK',
                    'PREVIOUS_YEAR',
                    'QUARTER_TO_DATE',
                    'WEEK_TO_DATE',
                    'YEAR_TO_DATE'
                  ],
                  'default': 'LAST_365_DAYS',
                  'description': 'Timeframe to run the ITP report for.',
                  'kind': 'choice',
                  'name': 'date_range',
                  'order': 3
                }
              },
              'format': 'CSV',
              'title': {
                'field': {
                  'description': 'Name of report in DV360, should be unique.',
                  'kind': 'string',
                  'name': 'recipe_name',
                  'order': 1,
                  'prefix': 'ITP_Audit_Browser_'
                }
              }
            },
            'params': {
              'groupBys': [
                'FILTER_PARTNER',
                'FILTER_PARTNER_NAME',
                'FILTER_ADVERTISER',
                'FILTER_ADVERTISER_NAME',
                'FILTER_ADVERTISER_CURRENCY',
                'FILTER_MEDIA_PLAN',
                'FILTER_MEDIA_PLAN_NAME',
                'FILTER_INSERTION_ORDER',
                'FILTER_INSERTION_ORDER_NAME',
                'FILTER_LINE_ITEM',
                'FILTER_LINE_ITEM_NAME',
                'FILTER_PAGE_LAYOUT',
                'FILTER_WEEK',
                'FILTER_MONTH',
                'FILTER_YEAR',
                'FILTER_LINE_ITEM_TYPE',
                'FILTER_DEVICE_TYPE',
                'FILTER_BROWSER'
              ],
              'metrics': [
                'METRIC_MEDIA_COST_ADVERTISER',
                'METRIC_IMPRESSIONS',
                'METRIC_CLICKS',
                'METRIC_TOTAL_CONVERSIONS',
                'METRIC_LAST_CLICKS',
                'METRIC_LAST_IMPRESSIONS',
                'METRIC_CM_POST_CLICK_REVENUE',
                'METRIC_CM_POST_VIEW_REVENUE',
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
                  'description': 'Optional: Comma delimited list of DV360 Advertiser ids.',
                  'kind': 'integer_list',
                  'name': 'dv360_advertiser_ids',
                  'order': 6
                }
              }
            },
            'FILTER_PARTNER': {
              'values': {
                'field': {
                  'default': '',
                  'description': 'Comma delimited list of DV360 Partner ids.',
                  'kind': 'integer_list',
                  'name': 'dv360_partner_ids',
                  'order': 5
                }
              }
            }
          },
          'timeout': 90
        }
      }
    },
    {
      'dcm': {
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
        'out': {
          'bigquery': {
            'dataset': {
              'field': {
                'default': 'ITP_Audit_Dashboard',
                'description': 'BigQuery dataset for store dashboard tables.',
                'kind': 'string',
                'name': 'recipe_slug',
                'order': 1
              }
            },
            'is_incremental_load': False,
            'table': 'z_Floodlight_CM_Report'
          }
        },
        'report': {
          'account': {
            'field': {
              'default': '',
              'description': 'Campaign Manager Account Id.',
              'kind': 'string',
              'name': 'cm_account_id',
              'order': 2
            }
          },
          'body': {
            'delivery': {
              'emailOwner': False
            },
            'floodlightCriteria': {
              'dateRange': {
                'kind': 'dfareporting#dateRange',
                'relativeDateRange': 'LAST_30_DAYS'
              },
              'dimensions': [
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:site'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:floodlightAttributionType'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:interactionType'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:pathType'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:browserPlatform'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:platformType'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:week'
                }
              ],
              'floodlightConfigId': {
                'dimensionName': 'dfa:floodlightConfigId',
                'kind': 'dfareporting#dimensionValue',
                'matchType': 'EXACT',
                'value': {
                  'field': {
                    'default': '',
                    'description': 'Floodlight Configuration Id for the Campaign Manager floodlight report.',
                    'kind': 'integer',
                    'name': 'floodlight_configuration_id',
                    'order': 4
                  }
                }
              },
              'metricNames': [
                'dfa:activityClickThroughConversions',
                'dfa:activityViewThroughConversions',
                'dfa:totalConversions',
                'dfa:totalConversionsRevenue'
              ],
              'reportProperties': {
                'includeUnattributedCookieConversions': True,
                'includeUnattributedIPConversions': False
              }
            },
            'format': 'CSV',
            'kind': 'dfareporting#report',
            'name': {
              'field': {
                'description': 'Name of report in DV360, should be unique.',
                'kind': 'string',
                'name': 'recipe_name',
                'order': 1,
                'prefix': 'ITP_Audit_Floodlight_'
              }
            },
            'schedule': {
              'active': True,
              'every': 1,
              'repeats': 'WEEKLY',
              'repeatsOnWeekDays': [
                'Sunday'
              ]
            },
            'type': 'FLOODLIGHT'
          },
          'timeout': 90
        }
      }
    },
    {
      'dcm': {
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
        'out': {
          'bigquery': {
            'dataset': {
              'field': {
                'default': 'ITP_Audit_Dashboard',
                'description': 'BigQuery dataset for store dashboard tables.',
                'kind': 'string',
                'name': 'recipe_slug',
                'order': 1
              }
            },
            'is_incremental_load': False,
            'table': 'z_CM_Browser_Report_Dirty'
          }
        },
        'report': {
          'account': {
            'field': {
              'default': '',
              'description': 'Campaign Manager Account Id.',
              'kind': 'string',
              'name': 'cm_account_id',
              'order': 2
            }
          },
          'body': {
            'criteria': {
              'dateRange': {
                'kind': 'dfareporting#dateRange',
                'relativeDateRange': {
                  'field': {
                    'choices': [
                      'LAST_7_DAYS',
                      'LAST_14_DAYS',
                      'LAST_30_DAYS',
                      'LAST_365_DAYS',
                      'LAST_60_DAYS',
                      'LAST_7_DAYS',
                      'LAST_90_DAYS',
                      'MONTH_TO_DATE',
                      'PREVIOUS_MONTH',
                      'PREVIOUS_QUARTER',
                      'PREVIOUS_WEEK',
                      'PREVIOUS_YEAR',
                      'QUARTER_TO_DATE',
                      'WEEK_TO_DATE',
                      'YEAR_TO_DATE'
                    ],
                    'default': 'LAST_365_DAYS',
                    'description': 'Timeframe to run the ITP report for.',
                    'kind': 'choice',
                    'name': 'date_range',
                    'order': 3
                  }
                }
              },
              'dimensionFilters': [
              ],
              'dimensions': [
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:campaign'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:campaignId'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:site'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:advertiser'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:advertiserId'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:browserPlatform'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:platformType'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:month'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:week'
                }
              ],
              'metricNames': [
                'dfa:impressions',
                'dfa:clicks',
                'dfa:totalConversions',
                'dfa:activityViewThroughConversions',
                'dfa:activityClickThroughConversions'
              ]
            },
            'delivery': {
              'emailOwner': False
            },
            'fileName': {
              'field': {
                'default': 'ITP_Audit_Dashboard_Browser',
                'description': 'Name of the Campaign Manager browser report.',
                'kind': 'string',
                'name': 'recipe_name',
                'order': 1,
                'prefix': 'ITP_Audit_Browser_'
              }
            },
            'format': 'CSV',
            'kind': 'dfareporting#report',
            'name': {
              'field': {
                'default': 'ITP_Audit_Dashboard_Browser',
                'description': 'Name of the Campaign Manager browser report.',
                'kind': 'string',
                'name': 'recipe_name',
                'order': 1,
                'prefix': 'ITP_Audit_Browser_'
              }
            },
            'schedule': {
              'active': True,
              'every': 1,
              'repeats': 'WEEKLY',
              'repeatsOnWeekDays': [
                'Sunday'
              ]
            },
            'type': 'STANDARD'
          },
          'filters': {
            'dfa:advertiser': {
              'values': {
                'field': {
                  'default': '',
                  'description': 'Optional: Comma delimited list of CM advertiser ids.',
                  'kind': 'integer_list',
                  'name': 'cm_advertiser_ids',
                  'order': 3
                }
              }
            }
          },
          'timeout': 90
        }
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
            'order': 1
          }
        },
        'header': True,
        'out': {
          'auth': {
            'field': {
              'default': 'service',
              'description': 'Credentials used for writing data.',
              'kind': 'authentication',
              'name': 'auth_write',
              'order': 1
            }
          },
          'bigquery': {
            'dataset': {
              'field': {
                'default': 'ITP_Audit_Dashboard',
                'description': 'BigQuery dataset for store dashboard tables.',
                'kind': 'string',
                'name': 'recipe_slug',
                'order': 1
              }
            },
            'table': 'z_Environment'
          }
        },
        'range': 'A:B',
        'sheet': {
          'field': {
            'default': '',
            'description': 'Name of document to deploy to.',
            'kind': 'string',
            'name': 'recipe_name',
            'order': 1,
            'prefix': 'ITP Audit '
          }
        },
        'tab': 'Enviroment'
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
            'order': 1
          }
        },
        'header': True,
        'out': {
          'auth': {
            'field': {
              'default': 'service',
              'description': 'Credentials used for writing data.',
              'kind': 'authentication',
              'name': 'auth_write',
              'order': 1
            }
          },
          'bigquery': {
            'dataset': {
              'field': {
                'default': 'ITP_Audit_Dashboard',
                'description': 'BigQuery dataset for store dashboard tables.',
                'kind': 'string',
                'name': 'recipe_slug',
                'order': 1
              }
            },
            'table': 'z_Browser'
          }
        },
        'range': 'A:C',
        'sheet': {
          'field': {
            'default': '',
            'description': 'Name of document to deploy to.',
            'kind': 'string',
            'name': 'recipe_name',
            'order': 1,
            'prefix': 'ITP Audit '
          }
        },
        'tab': 'Browser'
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
            'order': 1
          }
        },
        'header': True,
        'out': {
          'auth': {
            'field': {
              'default': 'service',
              'description': 'Credentials used for writing data.',
              'kind': 'authentication',
              'name': 'auth_write',
              'order': 1
            }
          },
          'bigquery': {
            'dataset': {
              'field': {
                'default': 'ITP_Audit_Dashboard',
                'description': 'BigQuery dataset for store dashboard tables.',
                'kind': 'string',
                'name': 'recipe_slug',
                'order': 1
              }
            },
            'table': 'z_CM_Browser_lookup'
          }
        },
        'range': 'A:C',
        'sheet': {
          'field': {
            'default': '',
            'description': 'Name of document to deploy to.',
            'kind': 'string',
            'name': 'recipe_name',
            'order': 1,
            'prefix': 'ITP Audit '
          }
        },
        'tab': 'CM_Browser_lookup'
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
            'order': 1
          }
        },
        'header': True,
        'out': {
          'auth': {
            'field': {
              'default': 'service',
              'description': 'Credentials used for writing data.',
              'kind': 'authentication',
              'name': 'auth_write',
              'order': 1
            }
          },
          'bigquery': {
            'dataset': {
              'field': {
                'default': 'ITP_Audit_Dashboard',
                'description': 'BigQuery dataset for store dashboard tables.',
                'kind': 'string',
                'name': 'recipe_slug',
                'order': 1
              }
            },
            'table': 'z_Device_Type'
          }
        },
        'range': 'A:B',
        'sheet': {
          'field': {
            'default': '',
            'description': 'Name of document to deploy to.',
            'kind': 'string',
            'name': 'recipe_name',
            'order': 1,
            'prefix': 'ITP Audit '
          }
        },
        'tab': 'Device_Type'
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
            'order': 1
          }
        },
        'header': True,
        'out': {
          'auth': {
            'field': {
              'default': 'service',
              'description': 'Credentials used for writing data.',
              'kind': 'authentication',
              'name': 'auth_write',
              'order': 1
            }
          },
          'bigquery': {
            'dataset': {
              'field': {
                'default': 'ITP_Audit_Dashboard',
                'description': 'BigQuery dataset for store dashboard tables.',
                'kind': 'string',
                'name': 'recipe_slug',
                'order': 1
              }
            },
            'table': 'z_Floodlight_Attribution'
          }
        },
        'range': 'A:B',
        'sheet': {
          'field': {
            'default': '',
            'description': 'Name of document to deploy to.',
            'kind': 'string',
            'name': 'recipe_name',
            'order': 1,
            'prefix': 'ITP Audit '
          }
        },
        'tab': 'Floodlight_Attribution'
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
        'out': {
          'bigquery': {
            'dataset': {
              'field': {
                'default': 'ITP_Audit_Dashboard',
                'description': 'BigQuery dataset for store dashboard tables.',
                'kind': 'string',
                'name': 'recipe_slug',
                'order': 1
              }
            },
            'header': True,
            'schema': [
              {
                'name': 'Partner_Id',
                'type': 'INTEGER'
              },
              {
                'name': 'Partner',
                'type': 'STRING'
              },
              {
                'name': 'Advertiser_Id',
                'type': 'INTEGER'
              },
              {
                'name': 'Advertiser',
                'type': 'STRING'
              },
              {
                'name': 'Advertiser_Currency',
                'type': 'STRING'
              },
              {
                'name': 'Campaign_Id',
                'type': 'INTEGER'
              },
              {
                'name': 'Campaign',
                'type': 'STRING'
              },
              {
                'name': 'Insertion_Order_Id',
                'type': 'INTEGER'
              },
              {
                'name': 'Insertion_Order',
                'type': 'STRING'
              },
              {
                'name': 'Line_Item_Id',
                'type': 'INTEGER'
              },
              {
                'name': 'Line_Item',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Environment',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Week',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Month',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Year',
                'type': 'INTEGER'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Line_Item_Type',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Device_Type',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Browser',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Media_Cost_Advertiser_Currency',
                'type': 'FLOAT'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Impressions',
                'type': 'INTEGER'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Clicks',
                'type': 'INTEGER'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Total_Conversions',
                'type': 'FLOAT'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Post_Click_Conversions',
                'type': 'FLOAT'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Post_View_Conversions',
                'type': 'FLOAT'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Cm_Post_Click_Revenue',
                'type': 'FLOAT'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Cm_Post_View_Revenue',
                'type': 'FLOAT'
              },
              {
                'mode': 'NULLABLE',
                'name': 'Revenue_Adv_Currency',
                'type': 'FLOAT'
              }
            ],
            'table': 'z_Dv360_Browser_Report_Dirty'
          }
        },
        'report': {
          'name': {
            'field': {
              'description': 'Name of report in DV360, should be unique.',
              'kind': 'string',
              'name': 'recipe_name',
              'order': 1,
              'prefix': 'ITP_Audit_Browser_'
            }
          }
        }
      }
    },
    {
      'itp_audit': {
        'account': {
          'field': {
            'default': '',
            'description': 'Campaign Manager Account Id.',
            'kind': 'string',
            'name': 'cm_account_id',
            'order': 2
          }
        },
        'auth': 'service',
        'dataset': {
          'field': {
            'default': 'ITP_Audit_Dashboard',
            'description': 'BigQuery dataset for store dashboard tables.',
            'kind': 'string',
            'name': 'recipe_slug',
            'order': 1
          }
        },
        'sheet': {
          'field': {
            'default': '',
            'description': 'Name of document to deploy to.',
            'kind': 'string',
            'name': 'recipe_name',
            'order': 1,
            'prefix': 'ITP Audit '
          }
        },
        'timeout': 60
      }
    }
  ]
}

DAG_FACTORY = DAG_Factory('itp_audit', RECIPE, INPUTS)
DAG = DAG_FACTORY.generate()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
