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


from collections.abc import Iterator
from pydantic import BaseModel

from cmk.server_side_calls.v1 import (
    HostConfig,
    Secret,
    SpecialAgentCommand,
    SpecialAgentConfig,
)


class Params(BaseModel):
    tenant_id: str
    app_id: str
    app_secret: Secret
    services_to_monitor: list[str] = []
    filter: tuple[str, list[str]] = ("", [])


def commands_function(
    params: Params,
    _host_config: HostConfig,
) -> Iterator[SpecialAgentCommand]:
    args: list[str | Secret] = [
        "--tenant-id",
        params.tenant_id,
        "--app-id",
        params.app_id,
        "--app-secret",
        params.app_secret,
    ]

    if params.services_to_monitor:
        args += ["--services-to-monitor", ",".join(params.services_to_monitor)]

    if params.filter[0] == "filter_subscriptions":
        args += ["--filter-subscriptions", ",".join(params.filter[1])]
    elif params.filter[0] == "filter_management_groups":
        args += ["--filter-management-groups", ",".join(params.filter[1])]

    yield SpecialAgentCommand(command_arguments=args)


special_agent_ms_azure_addon = SpecialAgentConfig(
    name="ms_azure_addon",
    parameter_parser=Params.model_validate,
    commands_function=commands_function,
)
