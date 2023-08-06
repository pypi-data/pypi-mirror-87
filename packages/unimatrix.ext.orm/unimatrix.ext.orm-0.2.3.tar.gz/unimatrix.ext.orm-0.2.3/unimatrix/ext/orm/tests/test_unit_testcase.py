# pylint: skip-file
import unittest

from sqlalchemy import Column
from sqlalchemy import String

from unimatrix.ext.orm import Relation
from unimatrix.ext.orm.testing import TestDatabaseManager


class TestDatabaseManagerTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.manager = TestDatabaseManager([Relation])
        cls.manager.on_setup_class({
            'DB_ENGINE': 'sqlite',
            'DB_NAME': ":memory:"
        })

    def test_setup_and_teardown_have_clean_state(self):
        self.manager.on_setup(self)
        try:
            dao = TestModel(foo='bar')
            self.session.add(dao)
            self.session.commit()

            q = self.session.query(TestModel)\
                .filter(TestModel.foo=='bar')\
                .exists()
            self.assertTrue(self.session.query(q).scalar())
        finally:
            self.manager.on_teardown()

        try:
            session = self.manager.get_session()
            q = session.query(TestModel)\
                .filter(TestModel.foo=='bar')\
                .exists()
            self.assertFalse(session.query(q).scalar())
        finally:
            session.close()


class TestModel(Relation):
    __tablename__ = 'testmodel'

    foo = Column(String, primary_key=True)
