# Copyright (C) 2019 Majormode.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Majormode or one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with the
# terms of the license agreement or other applicable agreement you
# entered into with Majormode.
#
# MAJORMODE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY
# OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE, OR NON-INFRINGEMENT.  MAJORMODE SHALL NOT BE LIABLE FOR ANY
# LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING
# OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.

from majormode.perseus.client.service.base_service import BaseService
from majormode.perseus.model.obj import Object


class NotificationService(BaseService):
    """
    A notification is a message that needs to be delivered to a set of
    recipients.  It informs the recipients about an event that occurs.
    """
    def __init__(self, connection):
        super(NotificationService, self).__init__(connection)

    def get_notifications(
            self,
            start_time=None, end_time=None,
            limit=BaseService.DEFAULT_RESULT_SET_SIZE,
            offset=0,
            include_read=False,
            mark_read=True):
        """
        Return a list of notifications that have been sent to the specified
        user's account, stored by ascending time of creation.

        @param start_time:
        @param offset: require to skip that many records before beginning to
               return records to the client.  Default value is ``0``.  If both
               ``offset`` and ``limit`` are specified, then ``offset`` records
               are skipped before starting to count the limit records that
               are returned.
        @param limit: constrain the number of records that are returned to the
               specified number.  Default value is ``20``. Maximum value is
               ``100``.
        @param include_read: indicate whether to include notifications that
               have already been read.  By default, notifications a user has
               read are not included.
        @param mark_read: indicate whether to mark read every notification
               that this functions returns.  By default, the function marks
               as read notifications that are returned.

        @return: a list of instances containing the following members:
                 * ``notification_id`` (required): identification of the
                   notification.
                 * ``notification_type`` (required): string representation of
                   the type of the notification, as defined by the client
                   application or the service that posted this notification to
                   the user.
                 * ``sender_id`` (optional): the identification of the account
                   of the user who initiates the notification.
                 * ``payload`` (optional): a dictionary containing additional
                   information specific to this particular notification.
                 * ``is_unread`` (required): indicate whether the notification
                   has been marked as read.
                 * ``creation_time`` (required): the time the notification was
                   originally sent.
                 * ``update_time`` (required): the time the notification was
                   originally sent, or the most recent time an attribute of
                   the notification, such as its read status, was updated.
       """
        return sorted(Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/notification',
                arguments={
                    'end_time': end_time,
                    'include_read': include_read,
                    'limit': limit,
                    'mark_read': mark_read,
                    'offset': offset,
                    'start_time': start_time
                },
                authentication_required=True,
                signature_required=True)),
            key=lambda notification: notification.creation_time)
