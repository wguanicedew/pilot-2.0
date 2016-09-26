# Copyright European Organization for Nuclear Research (CERN)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Authors:
# - Wen Guan, <wen.guan@cern.ch>, 2016

"""
DB Test instance
"""

from pilot.db import models, atomic

class TestDB():

    def test_db_connection(self):
        """ DB (CORE): Test db connection """
        session = get_session()
        if session.bind.dialect.name == 'oracle':
            session.execute('select 1 from dual')
        else:
            session.execute('select 1')
        session.close()

