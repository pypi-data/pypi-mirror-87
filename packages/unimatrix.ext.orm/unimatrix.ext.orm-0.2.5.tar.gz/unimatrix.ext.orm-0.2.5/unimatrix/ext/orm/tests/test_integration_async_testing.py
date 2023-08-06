# pylint: skip-file
from sqlalchemy import select

from unimatrix.ext.orm import async_session
from unimatrix.ext.orm import destroy_engines
from unimatrix.ext.orm.testing import AsyncSessionTestCase
from .orm import Foo


class TestAsyncSessionTestCase(AsyncSessionTestCase):
    target_metadata = [Foo.metadata]

    def test_no_data_is_persisted(self):
        session = self.get_session()
        session.add(Foo())
        
        result = self.execute_query(session, select(Foo))
        self.assertEqual(len(list(result)), 1)

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown(destroy=False)
        try:
            session = async_session()
            result = self.execute_query(session, select(Foo))
            self.assertEqual(len(list(result)), 0)
        finally:
            destroy_engines()
