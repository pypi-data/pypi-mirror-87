# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
test_gerritlib
----------------------------------

Tests for `gerritlib` module.
"""

from gerritlib.gerrit import GerritConnection
from gerritlib.tests import base
from paramiko.ssh_exception import NoValidConnectionsError


class TestGerritlib(base.TestCase):

    def test_invalid_connection(self):
        with self.assertRaises(NoValidConnectionsError):
            GerritConnection(connection_attempts=1, retry_delay=1).connect()
