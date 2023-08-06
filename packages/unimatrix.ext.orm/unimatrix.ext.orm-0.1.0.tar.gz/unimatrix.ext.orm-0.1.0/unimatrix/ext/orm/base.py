"""Declares the base class for all models in the Unimatrix framework."""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import DeclarativeMeta


class RelationCollection(dict):
    """Registry for all mapped classes that inherit from :class:`Relation`."""
    __name__ = 'RelationCollection'


# All classes that are mapped in the Unimatrix packages can be found in this
# dictionary.
RELATIONS = RelationCollection()


class RelationMeta(DeclarativeMeta):
    pass


class RelationBase:
    pass


Relation = declarative_base(
    class_registry=RELATIONS,
    cls=RelationBase,
    metaclass=RelationMeta,
    name='Relation'
)
