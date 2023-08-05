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

from majormode.perseus.client.service.team.team_service import TeamService
from majormode.perseus.client.unittest.base_unittest import BaseApiKeyTestCases

import unittest
import uuid

class TeamServiceTestCase(BaseApiKeyTestCase):
    def test_add_team(self):
        TeamService().add_team(self.unittest_app_id, self.unittest_account_id,
            'test_%s' % uuid.uuid1().hex)

    def test_add_duplicated_team(self):
        name = 'test_%s' % uuid.uuid1().hex
        TeamService().add_team(self.unittest_app_id, self.unittest_account_id, name)
        self.assertRaises(TeamService.NameAlreadyUsedException,
            TeamService().add_team,
            self.unittest_app_id, self.unittest_account_id, name)

    def test_get_account_teams(self):
        TeamService().add_team(self.unittest_app_id, self.unittest_account_id,
            'test_%s' % uuid.uuid1().hex)
        TeamService().get_account_teams(self.unittest_app_id, self.unittest_account_id)

    def test_add_members(self):
        team = TeamService().add_team(self.unittest_app_id, self.unittest_account_id,
            'test_%s' % uuid.uuid1().hex)
        account = AccountServiceTestCase.generate_account(self.unittest_app_id)
        TeamService().add_members(self.unittest_app_id, self.unittest_account_id,
            team.team_id, [ account.email_address ])

    def test_add_duplicated_master_members(self):
        team = TeamService().add_team(self.unittest_app_id, self.unittest_account_id,
            'test_%s' % uuid.uuid1().hex)

        account = AccountService().get_account(self.unittest_account_id)
        TeamService().add_members(self.unittest_app_id, self.unittest_account_id,
            team.team_id, [ account.email_address ])

    def test_add_duplicated_members(self):
        team = TeamService().add_team(self.unittest_app_id, self.unittest_account_id,
            'test_%s' % uuid.uuid1().hex)

        account = AccountServiceTestCase.generate_account(self.unittest_app_id)
        TeamService().add_members(self.unittest_app_id, self.unittest_account_id,
            team.team_id, [ account.email_address ])
        TeamService().add_members(self.unittest_app_id, self.unittest_account_id,
            team.team_id, [ account.email_address ])

    def test_accept_member_request(self):
        team = TeamService().add_team(self.unittest_app_id, self.unittest_account_id,
            'test_%s' % uuid.uuid1().hex)
        account = AccountServiceTestCase.generate_account(self.unittest_app_id)
        TeamService().add_members(self.unittest_app_id, self.unittest_account_id,
            team.team_id, [ account.email_address ])
        request_secured_key = TeamService()._get_request_secured_key(team.team_id, account.account_id)
        TeamService().accept_member_request(self.unittest_app_id, request_secured_key)

    def test_decline_member_request(self):
        team = TeamService().add_team(self.unittest_app_id, self.unittest_account_id,
            'test_%s' % uuid.uuid1().hex)
        account = AccountServiceTestCase.generate_account(self.unittest_app_id)
        TeamService().add_members(self.unittest_app_id, self.unittest_account_id,
            team.team_id, [ account.email_address ])
        request_secured_key = TeamService()._get_request_secured_key(team.team_id, account.account_id)
        TeamService().decline_member_request(self.unittest_app_id, request_secured_key)

    def test_revoke_member(self):
        team = TeamService().add_team(self.unittest_app_id, self.unittest_account_id,
            'test_%s' % uuid.uuid1().hex)
        account = AccountServiceTestCase.generate_account(self.unittest_app_id)
        TeamService().add_members(self.unittest_app_id, self.unittest_account_id,
            team.team_id, [ account.email_address ])
        request_secured_key = TeamService()._get_request_secured_key(team.team_id, account.account_id)
        TeamService().accept_member_request(self.unittest_app_id, request_secured_key, account.account_id)

        TeamService().revoke_member(self.unittest_app_id, self.unittest_account_id,
            team.team_id, account.account_id)
        self.assertRaises(TeamService.InvalidOperationException, TeamService().revoke_member,
            self.unittest_app_id, self.unittest_account_id,
            team.team_id, account.account_id)

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TeamServiceTestCase))
    return test_suite

if __name__ == '__main__':
    unittest.main()
