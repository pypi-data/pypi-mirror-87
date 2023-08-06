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

from starthinker.util.bigquery import query_to_view
from starthinker.util.bigquery import table_create
from starthinker.util.data import get_rows
from starthinker.util.data import put_rows
from starthinker.util.google_api import API_DV360
from starthinker.util.google_api.discovery_to_bigquery import Discovery_To_BigQuery
from starthinker.util.project import project
from starthinker.util.regexp import lookup_id
from starthinker.util.sheets import sheets_clear

from starthinker.task.dv_editor.patch import patch_clear
from starthinker.task.dv_editor.patch import patch_log
from starthinker.task.dv_editor.patch import patch_masks
from starthinker.task.dv_editor.patch import patch_preview


def line_item_clear():
  table_create(
      project.task["auth_bigquery"],
      project.id,
      project.task["dataset"],
      "DV_LineItems",
      Discovery_To_BigQuery("displayvideo",
                            "v1").method_schema("advertisers.lineItems.list"),
  )

  sheets_clear(project.task["auth_sheets"], project.task["sheet"], "Line Items",
               "A2:Z")


def line_item_load():

  # load multiple from user defined sheet
  def line_item_load_multiple():
    rows = get_rows(
        project.task["auth_sheets"], {
            "sheets": {
                "sheet": project.task["sheet"],
                "tab": "Advertisers",
                "range": "A2:A"
            }
        })

    for row in rows:
      yield from API_DV360(
          project.task["auth_dv"], iterate=True).advertisers().lineItems().list(
              advertiserId=lookup_id(row[0])).execute()

  # write line_items to database
  put_rows(
      project.task["auth_bigquery"], {
          "bigquery": {
              "dataset":
                  project.task["dataset"],
              "table":
                  "DV_LineItems",
              "schema":
                  Discovery_To_BigQuery(
                      "displayvideo",
                      "v1").method_schema("advertisers.lineItems.list"),
              "format":
                  "JSON"
          }
      }, line_item_load_multiple())

  # write line_items to sheet
  rows = get_rows(
    project.task["auth_bigquery"],
    { "bigquery": {
      "dataset": project.task["dataset"],
      "query": """SELECT
        CONCAT(P.displayName, ' - ', P.partnerId),
        CONCAT(A.displayName, ' - ', A.advertiserId),
        CONCAT(C.displayName, ' - ', C.campaignId),
        CONCAT(I.displayName, ' - ', I.insertionOrderId),
        CONCAT(L.displayName, ' - ', L.lineItemId),
        L.entityStatus,
        FROM `{dataset}.DV_LineItems` AS L
        LEFT JOIN `{dataset}.DV_Advertisers` AS A
        ON L.advertiserId=A.advertiserId
        LEFT JOIN `{dataset}.DV_Campaigns` AS C
        ON L.advertiserId=C.advertiserId
        LEFT JOIN `{dataset}.DV_InsertionOrders` AS I
        ON L.insertionOrderId=I.insertionOrderId
        LEFT JOIN `{dataset}.DV_Partners` AS P
        ON A.partnerId=P.partnerId
      """.format(**project.task),
      "legacy": False
    }}
  )

  put_rows(
    project.task["auth_sheets"],
    { "sheets": {
      "sheet": project.task["sheet"],
      "tab": "Line Items",
      "range": "B2"
    }},
    rows
  )


def line_item_patch(commit=False):

  def date_edited(value):
    y, m, d = value.split("-")
    return {"year": y, "month": m, "day": d}

  patches = []

  rows = get_rows(
    project.task["auth_bigquery"],
    { "bigquery": {
      "dataset": project.task["dataset"],
      "table":"PATCH_LineItems",
    }},
    as_object=True
  )

  for row in rows:

    if row['Action'] == "DELETE":
      patches.append({
        "operation": "Line Items",
        "action": "DELETE",
        "partner": row['Partner'],
        "advertiser": row['Advertiser'],
        "campaign": row['Campaign'],
        "line_item": row['Line_Item'],
        "parameters": {
          "advertiserId": lookup_id(row['Advertiser']),
          "lineItemId": lookup_id(row['Line_Item'])
        }
      })

    elif row['Action'] == "PATCH":
      line_item = {}

      if row['Line_Item_Type'] != row['Line_Item_Type_Edit']:
        line_item["lineItemType"] = row['Line_Item_Type_Edit']

      if row['Flight_Data_Type'] != row['Flight_Data_Type_Edit']:
        line_item.setdefault("flight", {})
        line_item["flight"]["flightDateType"] = row['Flight_Data_Type_Edit']

      if row['Flight_Start_Date'] != row['Flight_Start_Date_Edit']:
        line_item.setdefault("flight", {}).setdefault("dateRange", {})
        line_item["flight"]["dateRange"]["startDate"] = date_edited(row['Flight_Start_Date_Edit'])

      if row['Flight_End_Date'] != row['Flight_End_Date_Edit']:
        line_item.setdefault("flight", {}).setdefault("endDate", {})
        line_item["flight"]["dateRange"]["endDate"] = date_edited(row['Flight_End_Date_Edit'])

      if row['Flight_Trigger'] != row['Flight_Trigger_Edit']:
        line_item.setdefault("flight", {})
        line_item["flight"]["triggerId"] = row['Flight_Trigger_Edit']

      if row['Budget_Allocation_Type'] != row['Budget_Allocation_Type_Edit']:
        line_item.setdefault("budget", {})
        line_item["budget"]["budgetAllocationType"] = row['Budget_Allocation_Type_Edit']

      if row['Budget_Unit'] != row['Budget_Unit_Edit']:
        line_item.setdefault("budget", {})
        line_item["budget"]["budgetUnit"] = row['Budget_Unit_Edit']

      if row['Budget_Max'] != row['Budget_Max_Edit']:
        line_item.setdefault("budget", {})
        line_item["budget"]["maxAmount"] = int(
          float(row['Budget_Max_Edit']) * 100000
        )

      if row['Partner_Revenue_Model'] != row['Partner_Revenue_Model_Edit']:
        line_item.setdefault("partnerRevenueModel", {})
        line_item["partnerRevenueModel"]["markupType"] = row['Partner_Revenue_Model_Edit']

      if row['Partner_Markup'] != row['Partner_Markup_Edit']:
        line_item.setdefault("partnerRevenueModel", {})
        line_item["partnerRevenueModel"]["markupAmount"] = int(
          float(row['Partner_Markup_Edit']) * 100000
        )

      if row['Conversion_Percent'] != row['Conversion_Percent_Edit']:
        line_item.setdefault("conversionCounting", {})
        line_item["conversionCounting"]["postViewCountPercentageMillis"] = int(
          float(row['Conversion_Percent_Edit']) * 1000
        )

      if row['Targeting_Expansion_Level'] != row['Targeting_Expansion_Level_Edit']:
        line_item.setdefault("targetingExpansion", {})
        line_item["targetingExpansion"]["targetingExpansionLevel"] = row['Targeting_Expansion_Level_Edit']

      if row['Exclude_1P'] != row['Exclude_1P_Edit']:
        line_item.setdefault("targetingExpansion", {})
        line_item["targetingExpansion"]["excludeFirstPartyAudience"] = row['Exclude_1P_Edit']

      if line_item:
        patches.append({
          "operation": "Line Items",
          "action": "PATCH",
          "partner": row['Partner'],
          "advertiser": row['Advertiser'],
          "campaign": row['Campaign'],
          "line_item": row['Line_Item'],
          "parameters": {
            "advertiserId": lookup_id(row['Advertiser']),
            "lineItemId": lookup_id(row['Line_Item']),
            "body": line_item
          }
        })

  patch_masks(patches)

  if commit:
    line_item_commit(patches)
  else:
    patch_preview(patches)


def line_item_insert(commit=False):
  inserts = []

  rows = get_rows(
    project.task["auth_bigquery"],
    { "bigquery": {
      "dataset": project.task["dataset"],
      "table":"INSERT_LineItems",
    }},
    as_object=True
  )

  for row in rows:
    inserts.append({
      "operation": "Line Items",
      "action": "INSERT",
      "partner": None,
      "advertiser": row['advertiserId'],
      "campaign": row['campaignId'],
      "line_item": row['displayName'],
      "parameters": {
        "advertiserId": row['advertiserId'],
        "body":row
      }
    })

  if commit:
    line_item_commit(inserts)
  else:
    patch_preview(inserts)


def line_item_commit(patches):
  for patch in patches:
    if not patch.get("line_item"):
      continue
    print("API LINE ITEM:", patch["action"], patch["line_item"])
    try:
      if patch["action"] == "DELETE":
        response = API_DV360(
          project.task["auth_dv"]
        ).advertisers().lineItems().delete(
          **patch["parameters"]
        ).execute()
        patch["success"] = response
      elif patch["action"] == "PATCH":
        response = API_DV360(
          project.task["auth_dv"]
        ).advertisers().lineItems().patch(
          **patch["parameters"]
        ).execute()
        patch["success"] = response["lineItemId"]
      elif patch["action"] == "INSERT":
        response = API_DV360(
          project.task["auth_dv"]
        ).advertisers().lineItems().create(
          **patch["parameters"]
        ).execute()
        patch["success"] = response["lineItemId"]
    except Exception as e:
      patch["error"] = str(e)
    finally:
      patch_log(patch)
  patch_log()
