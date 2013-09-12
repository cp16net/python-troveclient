# Copyright 2013 Rackspace Inc.
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
#

from troveclient import base

import urlparse

from troveclient.common import limit_url
from troveclient.common import Paginated


class ScheduledTask(base.Resource):
    """
    Scheduled Task is a resource used to hold scheduled task information.
    """
    def __repr__(self):
        return "<ScheduledTask: %s>" % self.name


class ScheduledTasks(base.ManagerWithFind):
    """
    Manage :class:`ScheduledTask` resources.
    """
    resource_class = ScheduledTask

    def _list(self, url, response_key, limit=None, marker=None):
        resp, body = self.api.client.get(limit_url(url, limit, marker))
        if not body:
            raise Exception("Call to " + url + " did not return a body.")
        links = body.get('links', [])
        next_links = [link['href'] for link in links if link['rel'] == 'next']
        next_marker = None
        for link in next_links:
            # Extract the marker from the url.
            parsed_url = urlparse.urlparse(link)
            query_dict = dict(urlparse.parse_qsl(parsed_url.query))
            next_marker = query_dict.get('marker', None)
        instances = body[response_key]
        instances = [self.resource_class(self, res) for res in instances]
        return Paginated(instances, next_marker=next_marker, links=links)

    def list(self, instance, limit=None, marker=None):
        """
        Get a list of all scheduled tasks.

        :rtype: list of :class:`ScheduledTask`.
        """
        return self._list("/instances/%s/scheduledtasks" % base.getid(instance),
                          "scheduled_tasks", limit, marker)

    def get(self, instance, scheduledtask):
        """
        Get a specific scheduled task.

        :rtype: :class:`ScheduledTask`
        """
        return self._get("/instances/%s/scheduledtasks/%s" % (
                         base.getid(instance),
                         base.getid(scheduledtask)),
                         "scheduled_task")

    def create(self, id, name, type, enabled=True, description=None):
        """
        Create a new security group rule.
        """
        body = {
            "scheduled_task": {
                "name": name,
                "enabled": enabled,
                "type": type,
                # "frequency" : "hourly|daily|weekly|monthly",
                # "time_window":"2012-03-28T22:00Z/2012-03-28T23:00Z",
                "description" : description,
                # "task_metadata" : {
                #     "retentionPeriod" : "7|14|21|28",
                #     "notifications" : {
                #         "recipient" : "email@openstack.org",
                #         "notifySuccess" : "true|false", # default to False
                #         "notifyFailure" : "true|false"  # default to False
                #     }
                # }
            }
        }
        return self._create("/instances/%s/scheduledtasks" % base.getid(id),
                            body,
                            "scheduled_task")


