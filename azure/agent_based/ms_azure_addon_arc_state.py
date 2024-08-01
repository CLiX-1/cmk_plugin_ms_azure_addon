#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

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

from typing import Any, Mapping

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

Section = str

# Example data from special agent:
# <<<ms_azure_arc_state:sep(0)>>>
# Connected


def parse_ms_azure_arc_state(string_table: StringTable) -> Section:
    return string_table[0][0]


def discover_ms_azure_arc_state(section: Section) -> DiscoveryResult:
    yield Service()


def check_ms_azure_arc_state(params: Mapping[str, Any], section: Section) -> CheckResult:
    state = section.lower()

    if state in ["connected", "disconnected", "error", "expired"]:
        yield Result(
            state=State(params[state]),
            summary=f"State: {section}",
        )
    else:
        yield Result(
            state=State.UNKNOWN,
            summary=f"State: {section} (undefined)",
        )


agent_section_ms_azure_arc_state = AgentSection(
    name="ms_azure_arc_state",
    parse_function=parse_ms_azure_arc_state,
)


check_plugin_ms_azure_arc_state = CheckPlugin(
    name="ms_azure_arc_state",
    service_name="Azure Arc state",
    discovery_function=discover_ms_azure_arc_state,
    check_function=check_ms_azure_arc_state,
    check_ruleset_name="ms_azure_arc_state",
    check_default_parameters={"connected": 0, "disconnected": 1, "error": 2, "expired": 3},
)
