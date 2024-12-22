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
# Checkmk ruleset to set the severity levels for the Microsoft Azure Arc State.
# This ruleset is part of the Microsoft Azure AddOn special agent (ms_azure_addon).


from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import DefaultValue, DictElement, Dictionary, ServiceState
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


def _parameter_form_ms_azure_arc_state() -> Dictionary:
    return Dictionary(
        title=Title("Microsoft Azure Arc State"),
        help_text=Help(
            "Check parameters for the Microsoft Azure Arc State. "
            "To use this service, you need to set up the <b>Microsoft Azure AddOn</b> special "
            "agent."
        ),
        elements={
            "connected": DictElement(
                parameter_form=ServiceState(
                    title=Title("State connected"),
                    help_text=Help(
                        "Set the severity level of the state <i>connected</i>. The default "
                        "severity level is ok."
                    ),
                    prefill=DefaultValue(0),
                ),
            ),
            "disconnected": DictElement(
                parameter_form=ServiceState(
                    title=Title("State disconnected"),
                    help_text=Help(
                        "Set the severity level of the state <i>disconnected</i>. "
                        "The default severity level is warning."
                    ),
                    prefill=DefaultValue(1),
                ),
            ),
            "error": DictElement(
                parameter_form=ServiceState(
                    title=Title("State error"),
                    help_text=Help(
                        "Set the severity level of the state <i>error</i>. The default "
                        "severity level is critical."
                    ),
                    prefill=DefaultValue(2),
                ),
            ),
            "expired": DictElement(
                parameter_form=ServiceState(
                    title=Title("State expired"),
                    help_text=Help(
                        "Set the severity level of the state <i>expired</i>. The default "
                        "severity level is unknown."
                    ),
                    prefill=DefaultValue(3),
                ),
            ),
        },
    )


rule_spec_ms_azure_arc_state = CheckParameters(
    name="ms_azure_arc_state",
    title=Title("Microsoft Azure Arc State"),
    parameter_form=_parameter_form_ms_azure_arc_state,
    topic=Topic.CLOUD,
    condition=HostCondition(),
)
