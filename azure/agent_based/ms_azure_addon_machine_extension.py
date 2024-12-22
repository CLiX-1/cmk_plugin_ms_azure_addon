#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4; max-line-length: 100 -*-

# Copyright (C) 2024  Christopher Pommer <cp.software@outlook.de>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


####################################################################################################
# Checkmk check plugin for monitoring the Azure Arc and Azure machine extensions.
# The plugin works with data from the Microsoft Azure AddOn special agent (ms_azure_addon).

# Example data from special agent:
# <<<ms_azure_machine_extension:sep(0)>>>
# {
#     "arc_status": "Connected",
#     "extensions_exists": 1,
#     "extensions": [
#         {
#             "ExtensionName": "AzureSecurityWindowsAgent",
#             "ProvisioningState": "Succeeded"
#         },
#         {
#             "ExtensionName": "AzureMonitorWindowsAgent",
#             "ProvisioningState": "Succeeded"
#         },
#         {
#             "ExtensionName": "MDE.Windows",
#             "ProvisioningState": "Succeeded"
#         }
#     ],
#     "type": "microsoft.hybridcompute/machines"
# }


import json
from dataclasses import dataclass
from typing import Any, List, Mapping, TypedDict

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    State,
    StringTable,
)


class Extension(TypedDict):
    ExtensionName: str
    ProvisioningState: str


@dataclass(frozen=True)
class AzureMachine:
    arc_status: str
    extensions_exists: int
    extensions: List[Extension]
    type: str


Section = AzureMachine


def parse_ms_azure_machine_extension(string_table: StringTable) -> Section:
    parsed = json.loads(string_table[0][0])
    return AzureMachine(**parsed)


def discover_ms_azure_machine_extension(section: Section) -> DiscoveryResult:
    yield Service()


def check_ms_azure_machine_extension(params: Mapping[str, Any], section: Section) -> CheckResult:

    state_values = []
    extension_list = []
    extension_not_ok_list = []
    for extension in section.extensions:
        extension_name = extension["ExtensionName"]
        extension_state = extension["ProvisioningState"].lower()

        extension_summary = extension_name
        if extension_state in [
            "succeeded",
            "failed",
            "canceled",
            "creating",
            "updating",
            "deleting",
        ]:
            state_param = params[extension_state]
            state_values.append(state_param)
            if state_param != 0:
                extension_summary += f" ({extension_state})"
        else:
            state_values.append(3)
            extension_summary += f" ({extension_state} - undefined)"

        extension_not_ok_list.append(extension_summary)
        extension_list.append(f"{extension_name} ({extension_state})")

    result_summary = f"Extensions: {', '.join(sorted(extension_not_ok_list))}"
    result_details = "\n".join(sorted(extension_list))

    yield Result(
        state=State.worst(*state_values),
        summary=f"{result_summary}",
        details=f"{result_details}",
    )


agent_section_ms_azure_machine_extension = AgentSection(
    name="ms_azure_machine_extension",
    parse_function=parse_ms_azure_machine_extension,
)


check_plugin_ms_azure_machine_extension = CheckPlugin(
    name="ms_azure_machine_extension",
    service_name="Azure machine extension",
    discovery_function=discover_ms_azure_machine_extension,
    check_function=check_ms_azure_machine_extension,
    check_ruleset_name="ms_azure_machine_extension",
    check_default_parameters={
        "succeeded": 0,
        "failed": 2,
        "canceled": 1,
        "creating": 0,
        "updating": 0,
        "deleting": 0,
    },
)
