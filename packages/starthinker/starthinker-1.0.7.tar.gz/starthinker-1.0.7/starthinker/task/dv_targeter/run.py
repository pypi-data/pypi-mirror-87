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

from starthinker.util.project import project

from starthinker.task.dv_editor.advertiser import advertiser_clear
from starthinker.task.dv_editor.advertiser import advertiser_load
from starthinker.task.dv_editor.audit import audit_clear
from starthinker.task.dv_editor.audit import audit_load
from starthinker.task.dv_targeter.line_item import line_item_audit
from starthinker.task.dv_targeter.line_item import line_item_clear
from starthinker.task.dv_targeter.line_item import line_item_insert
from starthinker.task.dv_targeter.line_item import line_item_load
from starthinker.task.dv_targeter.line_item import line_item_patch
from starthinker.task.dv_editor.partner import partner_clear
from starthinker.task.dv_editor.partner import partner_load


@project.from_parameters
def dv_targeter():
  print('COMMAND:', project.task['command'])

  if project.task['command'] == 'Load Partners':
    partner_clear()
    partner_load()

  elif project.task['command'] == 'Load Advertisers':
    advertiser_clear()
    advertiser_load()

  elif project.task['command'] == 'Load Line Items':
    line_item_clear()
    line_item_load()

  elif project.task['command'] in ('Preview', 'Patch'):
    audit_clear()
    patch_clear()
    audit_load()

    partner_patch(commit=project.task['command'] == 'Patch')
    advertiser_patch(commit=project.task['command'] == 'Patch')
    line_item_patch(commit=project.task['command'] == 'Patch')

  elif project.task['command'] == 'Clear Partners':
    partner_clear()

  elif project.task['command'] == 'Clear Advertisers':
    advertiser_clear()

  elif project.task['command'] == 'Clear Line Items':
    line_item_clear()

  elif project.task['command'] == 'Clear Preview':
    audit_clear()

  elif project.task['command'] == 'Clear Patch':
    patch_clear()

  elif project.task['command'] == 'Clear All':
    partner_clear()
    advertiser_clear()
    line_item_clear()

    audit_clear()
    patch_clear()

if __name__ == '__main__':
  dv_targeter()
