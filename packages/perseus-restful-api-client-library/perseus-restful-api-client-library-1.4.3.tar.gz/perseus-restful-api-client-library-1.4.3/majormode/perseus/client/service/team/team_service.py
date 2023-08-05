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


class TeamService(BaseService):
    BaseService._declare_custom_exceptions({
    })

    def __init__(self, connection):
        super(TeamService, self).__init__(connection)

    def accept_invite(self, invite_code):
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.POST,
                path='/team/invite/(invite_code)/acceptance',
                url_bits={'invite_code': invite_code},
                authentication_required=False,
                signature_required=True))


    def add_team(self, name, description=None,
            invite_url=None, invite_email=None):
        """
        Add a new team on behalf of a user who becomes then the de facto
        master administrator for this team.

        @param app_id: identification of the client application such as a Web,
                a desktop, or a mobile application, that accesses the service.
        @param account_id: identification of the account of a user who add a
               team.
        @param name: name of the team.  This name MUST be unique among all the
               teams that have been registered so far against the platform.
               Case is not sensitive.
        @param description: a short textual description of the team, if any
               provided.
        @param invite_url: Uniform Resource Locator (URL) that is provided as
               a link in the email the platform sends to a user who is invited
               to join the team.  When the user clicks on the link embedded in
               the email, the email reader application issues a HTTP GET
               request to this URL.
        @param invite_email: template of the letter to be sent by email to a
               user who is invited to join a team.  If no specific template is
               specified for this team, the platform provides a default
               template.

        @raise DeletedObjectException: if the user account has been deleted.
        @raise DisabledObjectException: if the user account has been disabled.
        @raise NameAlreadyUsedException: if the name of the team passed to
               this function is already registered for an other team.
        @raise UndefinedObjectException: if the specified identification
               doesn't refer to a user account registered against the
               platform.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.POST,
                path='/team',
                message_body={
                    'name': name,
                    'description': description,
                    'invite_url': invite_url,
                    'invite_email': invite_email
                },
                authentication_required=True,
                signature_required=True))


    def cancel_invite(self, invite_id):
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.DELETE,
                path='/team/invite/(invite_id)',
                url_bits={'invite_id': invite_id},
                authentication_required=True,
                signature_required=True))


    def decline_invite(self, invite_code):
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.POST,
                path='/team/invite/(invite_code)/declination',
                url_bits={'invite_code': invite_code},
                authentication_required=False,
                signature_required=True))


    def get_member(self, team_id, account_id):
        """
        Indicate whether the authenticated user belongs to a given team.

        @param team_id: identification of a team.

        @param account_id: identification of the account of the user to check
            his membership to the specified team.

        @return: an instance containing the following members:

        @raise DeletedObjectException: if the team has been deleted.

        @raise DisabledObjectException: if the team has been disabled.

        @raise IllegalAccessException: if the user on behalf of the request is
            is not a member of this team.

        @raise UndefinedObjectException: if the specified identification
            doesn't refer to a team registered against the platform.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/team/(team_id)/member/(account_id)',
                url_bits={
                    'account_id': account_id,
                    'team_id': team_id },
                authentication_required=True,
                signature_required=True))


    def get_members(self, team_id,
            limit=BaseService.DEFAULT_RESULT_SET_SIZE, offset=0):
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/team/(team_id)/member',
                url_bits={'team_id': team_id },
                arguments={
                    'limit': limit,
                    'offset': offset,
                },
                authentication_required=True,
                signature_required=True))


    def get_account_teams(self, limit=BaseService.DEFAULT_RESULT_SET_SIZE, offset=0):
        """
        Return a list of teams the authenticated account is member of.

        @param offset: require to skip that many teams before beginning to
               return teams.
        @param limit: constrain the number of teams that are returned to the
               specified number.

        @return: an array of instance containing the following members:
                 * ``team_id``: identification of an team the
                   specified user is member of.
                 * ``name``: the title of the team.
                 * ``description``: a short textual description of the
                   team, if any provided.
                 * ``creation_time``: date and time when the team has
                   been registered.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/team',
                arguments={
                    'limit': limit,
                    'offset': offset,
                },
                authentication_required=True,
                signature_required=True))


    def invite_users(self, team_id, account_ids):
        """
        Invite a list of users to join the specified team.  The platform will
        eventually send them an invitation, either by an email or an in-app
        notification.  Their membership is pending until they accept or
        decline the invitation.

        The function filters out email addresses of users who are already
        members of the team and email addresses of users who have been already
        invited but who have not yet accepted.

        @note: only an administrator of the team is allowed to add members to
               a team.

        @note: the function silently creates ghost accounts for users who have
               not an email address registered against the platform yet.  The
               locale that is used to reference the preferred language of such
               users is the same than for the administrator of the team.


        @param team_id: identification of the team to add the specified user
               as a new member.
        @param account_ids: a list of valid email addresses of the users
               to add as new members to the specified team.

        @return: the list of email addresses of new members who have been
                 added to the team; users who were already members of the team
                 are filtered out.

        @raise DeletedObjectException: if the team has been deleted.
        @raise DisabledObjectException: if the team has been disabled.
        @raise IllegalAccessException: if the user on behalf of the new member
               is added to the team is not the master administrator or one of
               the regular administrators of this team.
        @raise InvalidArgumentException: if some email addresses are of a
               wrong format, i.e., not compliant with RFC 2822.
        @raise InvalidOperationException: if no URL callback for accepting
               member request has been defined for this team.
        @raise UndefinedObjectException: if the specified identification
               doesn't refer to a team registered against the platform.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.POST,
                path='/team/(team_id)/invite',
                url_bits={'team_id': team_id},
                message_body=account_ids,
                authentication_required=True,
                signature_required=True))


    def is_administrator(self, team_id):
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.HEAD,
                path='/team/(team_id)/administrator',
                url_bits={
                    'team_id': team_id
                },
                authentication_required=False,
                signature_required=True))


    def revoke_member(self, team_id, account_id):
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.DELETE,
                path='/team/(team_id)/member/(account_id)',
                url_bits={
                    'account_id': account_id,
                    'team_id': team_id
                },
                authentication_required=True,
                signature_required=True))


    def search_teams(self, keywords, limit=BaseService.DEFAULT_RESULT_SET_SIZE, offset=0):
        """
        Return a list of teams which names match, even partially, the
        specified keywords.

        @param keywords: a list of keywords.

        @param limit: constrain the number of teams that are returned to the
            specified number.

        @param offset: require to skip that many teams before beginning to
            return teams.

        @return: an instance containing the following members:

            * ``team_id``: identification of the team.

            * ``name``: the name of the team.

            * ``description``: a short textual description of the team, if any
              provided.

            * ``account_id``: identification of the account of the agent for
              this team.

            * ``picture_id``: identification of the picture that represents
              the team, if any picture defined for this team.

            * ``picture_url``: Uniform Resource Locator (URL) that specifies
              the location of the picture representing the team, if any
              defined.  The client application can use this URL and append the
              query parameter ``size`` to specify a given pixel resolution of
              the team's picture:

               * ``thumbnail``

               * ``small``

               * ``medium``

               * ``large``

            * ``creation_time``: time when the team has been registered.

            * ``update_time``: most recent time when some information, such as
              the name or the description of the team, has been modified.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.GET,
                path='/team',
                arguments={
                    'keywords': keywords,
                    'limit': limit,
                    'offset': offset,
                },
                authentication_required=False,
                signature_required=True))


    def submit_join_request(self, team_id):
        """
        Submit a request on behalf of a user to join a team.  This join
        request has to be approved by one of the administrators of this team.

        @param team_id: identification of the team the user requests to join.

        @raise DeletedObjectException: if the team has been deleted.

        @raise DisabledObjectException: if the team has been disabled.

        @raise UndefinedObjectException: if the specified identification
            doesn't refer to a team registered against the platform.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.POST,
                path='/team/(team_id)/join',
                url_bits={'team_id': team_id},
                authentication_required=True,
                signature_required=True))
