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

import random
import settings
import unittest


class BaseTestCase(unittest.TestCase):
    def setUp(self):
#        logging.basicConfig(stream=sys.stdout)
#        logging.getLogger('UnitTest').setLevel(logging.DEBUG)
#        self.logger = logging.getLogger('UnitTest')

        random.seed()

        self.unittest_account_id = settings.PLATFORM_UNITTEST_ACCOUNT_ID
        self.unittest_app_id = settings.PLATFORM_UNITTEST_APP_ID

    def tearDown(self):
        pass

class BaseApiKeyTestCase(BaseTestCase):
    def setUp(self):
        super(BaseApiKeyTestCase, self).setUp()
        self.api_key = settings.PLATFORM_UNITTEST_API_KEY
        self.secret_key = settings.PLATFORM_UNITTEST_SECRET_KEY
        self.account_id = settings.PLATFORM_UNITTEST_ACCOUNT_ID

def suite():
    return unittest.TestSuite()
