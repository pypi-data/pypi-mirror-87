#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Tuple

from polyaxon.exceptions import PolyaxonSchemaError

DEFAULT_HUB = "polyaxon"


def get_component_full_name(component: str, owner: str = None, tag: str = None) -> str:
    if tag:
        component = "{}:{}".format(component, tag)
    if owner:
        component = "{}/{}".format(owner, component)

    return component


def get_component_info(hub: str) -> Tuple[str, str, str]:
    if not hub:
        raise PolyaxonSchemaError("Received an invalid hub reference: `{}`".format(hub))
    hub_values = hub.split(":")
    if len(hub_values) > 2:
        raise PolyaxonSchemaError("Received an invalid hub reference: `{}`".format(hub))
    if len(hub_values) == 2:
        hub_name, version = hub_values
    else:
        hub_name, version = hub_values[0], "latest"
    version = version or "latest"
    parts = hub_name.replace(".", "/").split("/")
    owner = DEFAULT_HUB
    if not parts or len(parts) > 2:
        raise PolyaxonSchemaError("Received an invalid hub reference: `{}`".format(hub))
    if len(parts) == 2:
        owner, component = parts
    else:
        component = hub_name
    return owner, component, version
