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

DV360 Audience Analysis

The Audience Wizard Dashboard helps you to track the audience performance across all audiences on Display.

  - Wait for <b>BigQuery->UNDEFINED->UNDEFINED->DV360_Audience_Analysis</b> to be created.
  - Join the <a hre='https://groups.google.com/d/forum/starthinker-assets' target='_blank'>StarThinker Assets Group</a> to access the following assets
  - Copy <a href='https://datastudio.google.com/open/1d2vlf4C1roN95NsdsvWNZqKFcYN8N9Jg' target='_blank'>Sample DV360 Audience Analysis Dataset</a>.
  - Click Edit Connection, and change to <b>BigQuery->UNDEFINED->UNDEFINED->DV360_Audience_Analysis</b>.
  - Copy <a href='https://datastudio.google.com/open/1Ij_RluqolElm7Nny9fBrIAPRB9ObUl0M' target='_blank'>Sample DV360 Audience Analysis Report</a>.
  - When prompted choose the new data source you just created.
  - Or give these intructions to the client.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'recipe_slug': '',  # Place where tables will be created in BigQuery.
  'recipe_name': '',  # Name of report in DV360, should be unique.
  'recipe_timezone': 'America/Los_Angeles',  # Timezone for report dates.
  'partners': [],  # DV360 partner id.
  'advertisers': [],  # Comma delimited list of DV360 advertiser ids.
  'recipe_project': '',  # Google Cloud Project Id.
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
      6
    ]
  },
  'tasks': [
    {
      'dataset': {
        'auth': 'service',
        'dataset': {
          'field': {
            'description': 'Place where tables will be created in BigQuery.',
            'kind': 'string',
            'name': 'recipe_slug'
          }
        },
        'description': 'Create a dataset for bigquery tables.',
        'hour': [
          1
        ]
      }
    },
    {
      'dbm': {
        'auth': 'user',
        'hour': [
          2
        ],
        'report': {
          'body': {
            'metadata': {
              'dataRange': 'LAST_7_DAYS',
              'format': 'CSV',
              'title': {
                'field': {
                  'description': 'Name of report in DV360, should be unique.',
                  'kind': 'string',
                  'name': 'recipe_name',
                  'prefix': 'Audience Analysis Performance '
                }
              }
            },
            'params': {
              'groupBys': [
                'FILTER_ADVERTISER_NAME',
                'FILTER_ADVERTISER',
                'FILTER_AUDIENCE_LIST',
                'FILTER_USER_LIST',
                'FILTER_AUDIENCE_LIST_TYPE',
                'FILTER_AUDIENCE_LIST_COST',
                'FILTER_PARTNER_CURRENCY'
              ],
              'metrics': [
                'METRIC_IMPRESSIONS',
                'METRIC_CLICKS',
                'METRIC_TOTAL_CONVERSIONS',
                'METRIC_LAST_CLICKS',
                'METRIC_LAST_IMPRESSIONS',
                'METRIC_TOTAL_MEDIA_COST_PARTNER'
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
                  'default': [
                  ],
                  'description': 'Comma delimited list of DV360 advertiser ids.',
                  'kind': 'integer_list',
                  'name': 'advertisers',
                  'order': 6
                }
              }
            },
            'FILTER_PARTNER': {
              'values': {
                'field': {
                  'default': [
                  ],
                  'description': 'DV360 partner id.',
                  'kind': 'integer_list',
                  'name': 'partners',
                  'order': 5
                }
              }
            }
          }
        }
      }
    },
    {
      'dbm': {
        'auth': 'user',
        'hour': [
          6
        ],
        'out': {
          'bigquery': {
            'dataset': {
              'field': {
                'description': 'Place where tables will be created in BigQuery.',
                'kind': 'string',
                'name': 'recipe_slug'
              }
            },
            'header': True,
            'schema': [
              {
                'mode': 'REQUIRED',
                'name': 'advertiser',
                'type': 'STRING'
              },
              {
                'mode': 'REQUIRED',
                'name': 'advertiser_id',
                'type': 'INT64'
              },
              {
                'mode': 'REQUIRED',
                'name': 'audience_list',
                'type': 'STRING'
              },
              {
                'mode': 'REQUIRED',
                'name': 'audience_list_id',
                'type': 'INT64'
              },
              {
                'mode': 'NULLABLE',
                'name': 'audience_list_type',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'audience_list_cost_usd',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'partner_currency',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'impressions',
                'type': 'INT64'
              },
              {
                'mode': 'NULLABLE',
                'name': 'clicks',
                'type': 'INT64'
              },
              {
                'mode': 'NULLABLE',
                'name': 'total_conversions',
                'type': 'FLOAT'
              },
              {
                'mode': 'NULLABLE',
                'name': 'post_click_conversions',
                'type': 'FLOAT'
              },
              {
                'mode': 'NULLABLE',
                'name': 'post_view_conversions',
                'type': 'FLOAT'
              },
              {
                'mode': 'NULLABLE',
                'name': 'total_media_cost_partner_currency',
                'type': 'FLOAT'
              }
            ],
            'table': 'DV360_Audience_Performance'
          }
        },
        'report': {
          'name': {
            'field': {
              'description': 'Name of report in DV360, should be unique.',
              'kind': 'string',
              'name': 'recipe_name',
              'prefix': 'Audience Analysis Performance '
            }
          }
        }
      }
    },
    {
      'dbm': {
        'auth': 'user',
        'hour': [
          2
        ],
        'report': {
          'body': {
            'metadata': {
              'dataRange': 'LAST_7_DAYS',
              'format': 'CSV',
              'title': {
                'field': {
                  'description': 'Name of report in DV360, should be unique.',
                  'kind': 'string',
                  'name': 'recipe_name',
                  'prefix': 'Audience Analysis First Party'
                }
              }
            },
            'params': {
              'groupBys': [
                'FILTER_ADVERTISER_NAME',
                'FILTER_ADVERTISER',
                'FILTER_USER_LIST_FIRST_PARTY_NAME',
                'FILTER_USER_LIST_FIRST_PARTY',
                'FILTER_FIRST_PARTY_AUDIENCE_LIST_TYPE',
                'FILTER_FIRST_PARTY_AUDIENCE_LIST_COST'
              ],
              'metrics': [
                'METRIC_BID_REQUESTS',
                'METRIC_UNIQUE_VISITORS_COOKIES'
              ],
              'type': 'TYPE_INVENTORY_AVAILABILITY'
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
                  'default': [
                  ],
                  'description': 'Comma delimited list of DV360 advertiser ids.',
                  'kind': 'integer_list',
                  'name': 'advertisers',
                  'order': 6
                }
              }
            },
            'FILTER_PARTNER': {
              'values': {
                'field': {
                  'default': [
                  ],
                  'description': 'DV360 partner id.',
                  'kind': 'integer_list',
                  'name': 'partners',
                  'order': 5
                }
              }
            }
          }
        }
      }
    },
    {
      'dbm': {
        'auth': 'user',
        'hour': [
          6
        ],
        'out': {
          'bigquery': {
            'dataset': {
              'field': {
                'description': 'Place where tables will be created in BigQuery.',
                'kind': 'string',
                'name': 'recipe_slug'
              }
            },
            'header': True,
            'schema': [
              {
                'mode': 'REQUIRED',
                'name': 'advertiser',
                'type': 'STRING'
              },
              {
                'mode': 'REQUIRED',
                'name': 'advertiser_id',
                'type': 'INT64'
              },
              {
                'mode': 'REQUIRED',
                'name': 'audience_list',
                'type': 'STRING'
              },
              {
                'mode': 'REQUIRED',
                'name': 'audience_list_id',
                'type': 'INT64'
              },
              {
                'mode': 'NULLABLE',
                'name': 'audience_list_type',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'audience_list_cost_usd',
                'type': 'FLOAT'
              },
              {
                'mode': 'NULLABLE',
                'name': 'potential_impressions',
                'type': 'INT64'
              },
              {
                'mode': 'NULLABLE',
                'name': 'unique_cookies_with_impressions',
                'type': 'INT64'
              }
            ],
            'table': 'DV360_First_Party_Audience'
          }
        },
        'report': {
          'name': {
            'field': {
              'description': 'Name of report in DV360, should be unique.',
              'kind': 'string',
              'name': 'recipe_name',
              'prefix': 'Audience Analysis First Party'
            }
          }
        }
      }
    },
    {
      'dbm': {
        'auth': 'user',
        'hour': [
          2
        ],
        'report': {
          'body': {
            'metadata': {
              'dataRange': 'LAST_7_DAYS',
              'format': 'CSV',
              'title': {
                'field': {
                  'description': 'Name of report in DV360, should be unique.',
                  'kind': 'string',
                  'name': 'recipe_name',
                  'prefix': 'Audience Analysis Google'
                }
              }
            },
            'params': {
              'groupBys': [
                'FILTER_ADVERTISER_NAME',
                'FILTER_ADVERTISER',
                'FILTER_AUDIENCE_LIST',
                'FILTER_USER_LIST',
                'FILTER_AUDIENCE_LIST_TYPE',
                'FILTER_AUDIENCE_LIST_COST'
              ],
              'metrics': [
                'METRIC_BID_REQUESTS',
                'METRIC_UNIQUE_VISITORS_COOKIES'
              ],
              'type': 'TYPE_INVENTORY_AVAILABILITY'
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
                  'default': [
                  ],
                  'description': 'Comma delimited list of DV360 advertiser ids.',
                  'kind': 'integer_list',
                  'name': 'advertisers',
                  'order': 6
                }
              }
            },
            'FILTER_PARTNER': {
              'values': {
                'field': {
                  'default': [
                  ],
                  'description': 'DV360 partner id.',
                  'kind': 'integer_list',
                  'name': 'partners',
                  'order': 5
                }
              }
            }
          }
        }
      }
    },
    {
      'dbm': {
        'auth': 'user',
        'hour': [
          6
        ],
        'out': {
          'bigquery': {
            'dataset': {
              'field': {
                'description': 'Place where tables will be created in BigQuery.',
                'kind': 'string',
                'name': 'recipe_slug'
              }
            },
            'header': True,
            'schema': [
              {
                'mode': 'REQUIRED',
                'name': 'advertiser',
                'type': 'STRING'
              },
              {
                'mode': 'REQUIRED',
                'name': 'advertiser_id',
                'type': 'INT64'
              },
              {
                'mode': 'REQUIRED',
                'name': 'audience_list',
                'type': 'STRING'
              },
              {
                'mode': 'REQUIRED',
                'name': 'audience_list_id',
                'type': 'INT64'
              },
              {
                'mode': 'NULLABLE',
                'name': 'audience_list_type',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'audience_list_cost_usd',
                'type': 'FLOAT'
              },
              {
                'mode': 'NULLABLE',
                'name': 'potential_impressions',
                'type': 'INT64'
              },
              {
                'mode': 'NULLABLE',
                'name': 'unique_cookies_with_impressions',
                'type': 'INT64'
              }
            ],
            'table': 'DV360_Google_Audience'
          }
        },
        'report': {
          'name': {
            'field': {
              'description': 'Name of report in DV360, should be unique.',
              'kind': 'string',
              'name': 'recipe_name',
              'prefix': 'Audience Analysis Google'
            }
          }
        }
      }
    },
    {
      'dbm': {
        'auth': 'user',
        'hour': [
          2
        ],
        'report': {
          'body': {
            'metadata': {
              'dataRange': 'LAST_7_DAYS',
              'format': 'CSV',
              'title': {
                'field': {
                  'description': 'Name of report in DV360, should be unique.',
                  'kind': 'string',
                  'name': 'recipe_name',
                  'prefix': 'Audience Analysis Third Party'
                }
              }
            },
            'params': {
              'groupBys': [
                'FILTER_ADVERTISER_NAME',
                'FILTER_ADVERTISER',
                'FILTER_USER_LIST_THIRD_PARTY_NAME',
                'FILTER_USER_LIST_THIRD_PARTY',
                'FILTER_THIRD_PARTY_AUDIENCE_LIST_TYPE',
                'FILTER_THIRD_PARTY_AUDIENCE_LIST_COST'
              ],
              'metrics': [
                'METRIC_BID_REQUESTS',
                'METRIC_UNIQUE_VISITORS_COOKIES'
              ],
              'type': 'TYPE_INVENTORY_AVAILABILITY'
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
                  'default': [
                  ],
                  'description': 'Comma delimited list of DV360 advertiser ids.',
                  'kind': 'integer_list',
                  'name': 'advertisers',
                  'order': 6
                }
              }
            },
            'FILTER_PARTNER': {
              'values': {
                'field': {
                  'default': [
                  ],
                  'description': 'DV360 partner id.',
                  'kind': 'integer_list',
                  'name': 'partners',
                  'order': 5
                }
              }
            }
          }
        }
      }
    },
    {
      'dbm': {
        'auth': 'user',
        'hour': [
          6
        ],
        'out': {
          'bigquery': {
            'dataset': {
              'field': {
                'description': 'Place where tables will be created in BigQuery.',
                'kind': 'string',
                'name': 'recipe_slug'
              }
            },
            'header': True,
            'schema': [
              {
                'mode': 'REQUIRED',
                'name': 'advertiser',
                'type': 'STRING'
              },
              {
                'mode': 'REQUIRED',
                'name': 'advertiser_id',
                'type': 'INT64'
              },
              {
                'mode': 'REQUIRED',
                'name': 'audience_list',
                'type': 'STRING'
              },
              {
                'mode': 'REQUIRED',
                'name': 'audience_list_id',
                'type': 'INT64'
              },
              {
                'mode': 'NULLABLE',
                'name': 'audience_list_type',
                'type': 'STRING'
              },
              {
                'mode': 'NULLABLE',
                'name': 'audience_list_cost_usd',
                'type': 'FLOAT'
              },
              {
                'mode': 'NULLABLE',
                'name': 'potential_impressions',
                'type': 'INT64'
              },
              {
                'mode': 'NULLABLE',
                'name': 'unique_cookies_with_impressions',
                'type': 'INT64'
              }
            ],
            'table': 'DV360_Third_Party_Audience'
          }
        },
        'report': {
          'name': {
            'field': {
              'description': 'Name of report in DV360, should be unique.',
              'kind': 'string',
              'name': 'recipe_name',
              'prefix': 'Audience Analysis Third Party'
            }
          }
        }
      }
    },
    {
      'bigquery': {
        'auth': 'service',
        'from': {
          'legacy': False,
          'parameters': [
            {
              'field': {
                'default': '',
                'description': 'Google Cloud Project Id.',
                'kind': 'string',
                'name': 'recipe_project',
                'order': 6
              }
            },
            {
              'field': {
                'description': 'Place where tables will be created in BigQuery.',
                'kind': 'string',
                'name': 'recipe_slug'
              }
            },
            {
              'field': {
                'default': '',
                'description': 'Google Cloud Project Id.',
                'kind': 'string',
                'name': 'recipe_project',
                'order': 6
              }
            },
            {
              'field': {
                'description': 'Place where tables will be created in BigQuery.',
                'kind': 'string',
                'name': 'recipe_slug'
              }
            },
            {
              'field': {
                'default': '',
                'description': 'Google Cloud Project Id.',
                'kind': 'string',
                'name': 'recipe_project',
                'order': 6
              }
            },
            {
              'field': {
                'description': 'Place where tables will be created in BigQuery.',
                'kind': 'string',
                'name': 'recipe_slug'
              }
            },
            {
              'field': {
                'default': '',
                'description': 'Google Cloud Project Id.',
                'kind': 'string',
                'name': 'recipe_project',
                'order': 6
              }
            },
            {
              'field': {
                'description': 'Place where tables will be created in BigQuery.',
                'kind': 'string',
                'name': 'recipe_slug'
              }
            }
          ],
          'query': " SELECT   p.advertiser_id,   p.advertiser,   p.audience_list_id,   IF (p.audience_list_type = 'Bid Manager Audiences', 'Google', p.audience_list_type) AS audience_list_type,   CASE     WHEN REGEXP_CONTAINS(p.audience_list, 'Affinity') THEN 'Affinity'     WHEN REGEXP_CONTAINS(p.audience_list, 'Demographics') THEN 'Demographics'     WHEN REGEXP_CONTAINS(p.audience_list, 'In-Market') THEN 'In-Market'     WHEN REGEXP_CONTAINS(p.audience_list, 'Similar') THEN 'Similar'     ELSE 'Custom'   END AS audience_list_category,   p.audience_list,   IF(p.audience_list_cost_usd = 'Unknown', 0.0, CAST(p.audience_list_cost_usd AS FLOAT64)) AS audience_list_cost,   p.total_media_cost_partner_currency AS total_media_cost,   p.impressions,   p.clicks,   p.total_conversions,   COALESCE(ggl.potential_impressions, fst.potential_impressions, trd.potential_impressions) AS potential_impressions,   COALESCE(ggl.unique_cookies_with_impressions, fst.unique_cookies_with_impressions, trd.unique_cookies_with_impressions) AS potential_reach FROM   `[PARAMETER].[PARAMETER].DV360_Audience_Performance` p LEFT JOIN   `[PARAMETER].[PARAMETER].DV360_Google_Audience` ggl   USING (advertiser_id, audience_list_id) LEFT JOIN   `[PARAMETER].[PARAMETER].DV360_First_Party_Audience` fst   USING (advertiser_id, audience_list_id) LEFT JOIN   `[PARAMETER].[PARAMETER].DV360_Third_Party_Audience` trd   USING (advertiser_id, audience_list_id) "
        },
        'hour': [
          6
        ],
        'to': {
          'dataset': {
            'field': {
              'description': 'Place where tables will be created in BigQuery.',
              'kind': 'string',
              'name': 'recipe_slug'
            }
          },
          'view': 'DV360_Audience_Analysis'
        }
      }
    }
  ]
}

DAG_FACTORY = DAG_Factory('audience_analysis', RECIPE, INPUTS)
DAG = DAG_FACTORY.generate()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
