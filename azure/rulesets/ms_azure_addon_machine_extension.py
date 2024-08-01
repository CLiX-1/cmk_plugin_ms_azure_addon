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


from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import DefaultValue, DictElement, Dictionary, ServiceState
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


def _parameter_form_ms_azure_machine_extension() -> Dictionary:
    return Dictionary(
        title=Title("Microsoft Azure Machine Extension"),
        help_text=Help(
            "Check parameters for the Microsoft Azure machine extension. "
            "To use this service, you need to set up the <b>Microsoft Azure AddOn</b> special agent."
        ),
        elements={
            "succeeded": DictElement(
                parameter_form=ServiceState(
                    title=Title("Provisioning state succeeded"),
                    help_text=Help(
                        "Set the severity level of the provisioning state <i>succeeded</i>. "
                        "The default severity level is ok."
                    ),
                    prefill=DefaultValue(0),
                ),
            ),
            "failed": DictElement(
                parameter_form=ServiceState(
                    title=Title("Provisioning state failed"),
                    help_text=Help(
                        "Set the severity level of the provisioning state <i>failed</i>. "
                        "The default severity level is critical."
                    ),
                    prefill=DefaultValue(2),
                ),
            ),
            "canceled": DictElement(
                parameter_form=ServiceState(
                    title=Title("Provisioning state canceled"),
                    help_text=Help(
                        "Set the severity level of the provisioning state <i>canceled</i>. "
                        "The default severity level is warning."
                    ),
                    prefill=DefaultValue(1),
                ),
            ),
            "creating": DictElement(
                parameter_form=ServiceState(
                    title=Title("Provisioning state creating"),
                    help_text=Help(
                        "Set the severity level of the provisioning state <i>creating</i>. "
                        "The default severity level is ok."
                    ),
                    prefill=DefaultValue(0),
                ),
            ),
            "updating": DictElement(
                parameter_form=ServiceState(
                    title=Title("Provisioning state updating"),
                    help_text=Help(
                        "Set the severity level of the provisioning state <i>updating</i>. "
                        "The default severity level is ok."
                    ),
                    prefill=DefaultValue(0),
                ),
            ),
            "deleting": DictElement(
                parameter_form=ServiceState(
                    title=Title("Provisioning state deleting"),
                    help_text=Help(
                        "Set the severity level of the provisioning state <i>deleting</i>. "
                        "The default severity level is ok."
                    ),
                    prefill=DefaultValue(0),
                ),
            ),
        },
    )


rule_spec_ms_azure_machine_extension = CheckParameters(
    name="ms_azure_machine_extension",
    title=Title("Microsoft Azure Machine Extension"),
    parameter_form=_parameter_form_ms_azure_machine_extension,
    topic=Topic.CLOUD,
    condition=HostCondition(),
)
