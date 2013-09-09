# Copyright (c) 2013 OpenStack, LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import exceptions
import json
from troveclient import base
from troveclient.common import check_for_exceptions


class Configuration(base.Resource):
    """
    Configuration is a resource used to hold configuration information.
    """
    def __repr__(self):
        return "<Configuration: %s>" % self.name


class Configurations(base.ManagerWithFind):
    """
    Manage :class:`Configurations` information.
    """

    resource_class = Configuration

    def get(self, configuration):
        """
        Get a specific configuration.

        :rtype: :class:`Configurations`
        """
        return self._get("/configurations/%s" % base.getid(configuration),
                         "configuration")

    def list(self, limit=None, marker=None):
        """
        Get a list of all configurations.

        :rtype: list of :class:`Configurations`.
        """
        return self._list("/configurations", "configurations", limit, marker)

    def create(self, name, values, description=None):
        """
        Create a new configuration.
        """
        body = {
            "configuration": {
                "name": name,
                "values": json.loads(values)
            }
        }
        if description:
            body['configuration']['description'] = description
        return self._create("/configurations", body, "configuration")

    def update(self, configuration_id, values, name=None, description=None):
        """
        Update an existing configuration.
        """
        body = {
            "configuration": {
                "values": json.loads(values)
            }
        }
        if name:
            body['configuration']['name'] = name
        if description:
            body['configuration']['description'] = description
        url = "/configurations/%s" % configuration_id
        resp, body = self.api.client.put(url, body=body)
        check_for_exceptions(resp, body)

    def delete(self, configuration_id):
        """
        Delete the specified configuration.

        :param configuration_id: The configuration id to delete
        """
        url = "/configurations/%s" % configuration_id
        resp, body = self.api.client.delete(url)
        if resp.status in (422, 500):
            raise exceptions.from_response(resp, body)

    def parameters(self):
        """
        Get a list of valid parameters that can be changed.
        """
        return self._get("/configurations/parameters")
