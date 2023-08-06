# pylint: skip-file
import unittest

from sqlalchemy import create_engine

from unimatrix.ext.orm import Relation


class RelationBasicTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite://')

    def tearDown(self):
        self.engine.dispose()

    def test_create_all(self):
        Relation.metadata.create_all(self.engine)
