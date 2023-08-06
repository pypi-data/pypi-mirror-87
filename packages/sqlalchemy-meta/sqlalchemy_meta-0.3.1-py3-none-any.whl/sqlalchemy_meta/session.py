from collections import Mapping, Sequence
from functools import partialmethod
from operator import attrgetter
from types import MappingProxyType

from sqlalchemy import Column, and_, inspect, or_, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.elements import UnaryExpression

__all__ = [
    'SessionDeclarativeMeta'
]


def _get_abs_int(value):
    if value is None:
        return

    return abs(int(value))


_JOINT_OR_MARKER = frozenset({or_, False, 'or', 'OR'})


def _select_joint(value):
    """Get joint expression of sqlalchemy by marker."""
    return or_ if value in _JOINT_OR_MARKER else and_


def _normalize_order_by(value):
    """Get order_by tuple of expressions."""
    if isinstance(
        # Check for strings
        value, str
    ) or isinstance(
        # Check for sqlalchemy allowed structures
        value, (UnaryExpression, InstrumentedAttribute, Column)
    ):
        return value,

    if isinstance(value, Sequence):
        # Check for sequences becides strings
        return value

    raise ValueError('order_by should be ordered sequence or suitable '
                     'sqlalchemy order_by expression.')


def _compile_primary_key_filter(primary_key, *identities):
    """Compile sqlalchemy compalible filter expression for primary key
    columns."""
    single_primary_key = len(primary_key) == 1

    for identity in identities:

        if not isinstance(identity, Mapping):

            if not single_primary_key:
                raise ValueError('For multi primary key it must be declared '
                                 'dict-like identity.')

            yield primary_key[0] == identity
            continue

        # identity is Mapping
        if single_primary_key and len(identity) > 1:
            raise ValueError('Primary key identity must be a string or '
                             'single-key Mapping.')

        yield and_(
            *map(lambda column: column == identity[column.key], primary_key)
        )


def _get_setable_unique_hybrid_keys(data, mapper):
    """Filter sqlalchemy hybrid_property keys, which can be setted by input
    data."""
    class_ = mapper.class_

    for key, descriptor in mapper.all_orm_descriptors.items():

        if not isinstance(
                descriptor, hybrid_property
        ) or getattr(
            descriptor, 'fset', None
        ) is None:
            # descriptor is not setable ``hybrid_property``
            continue

        original_key = getattr(class_, key).property.class_attribute.key

        if original_key not in data:
            # original column not in unput data, so, we can use hybrid key
            yield key


def _filter_kwargs(mapper, kwargs):
    """Filter input kwargs with allowed columns or hybdir_property keys of
    model."""

    # Hybrid properties may represent actual column for backward
    # compatibility.
    hybrid_property_keys = frozenset(_get_setable_unique_hybrid_keys(
        kwargs, mapper
    ))
    column_keys = frozenset(mapper.columns.keys())
    allowed_keys = hybrid_property_keys | column_keys

    return {
        k: v for k, v in kwargs.items() if k in allowed_keys
    }


def _delete_method(self, silent=False):
    """Delete method for child class of metaclass."""
    db_session = type(self).db_session

    try:
        with db_session.begin_nested():
            db_session.delete(self)
            db_session.flush()

    except SQLAlchemyError:
        if not silent:
            raise


_delete_method.__name__ = 'delete'


def _edit_method(self, *args, **kwargs):
    """Edit method for child class of metaclass."""
    self.__init__(*args, **_filter_kwargs(self.__class__.mapper, kwargs))
    return self


_edit_method.__name__ = 'edit'


def _get_primary_key_dict_method(self):
    """Calculate read-only dict value for primary key columns."""
    return MappingProxyType({
        key: getattr(self, key) for key in map(
            attrgetter('key'), self.__class__.mapper.primary_key
        )
    })


class SessionDeclarativeMeta(DeclarativeMeta):
    """
    Declarative metaclass for sqlalchemy models, that required incapsulation
    of sqlalchemy database scoped session methods for session-based model
    operations.
    """

    def __new__(mcs, classname, bases, namespace):
        # Set additional methods during type construction.
        namespace.setdefault('delete', _delete_method)
        namespace.setdefault('edit', _edit_method)
        namespace.setdefault('primary_key',
                             property(_get_primary_key_dict_method))
        return super().__new__(mcs, classname, bases, namespace)

    def __init__(cls, classname, bases, namespace):
        super().__init__(classname, bases, namespace)

        if not hasattr(cls, '_db_session'):
            # session could be setted already in any parent class
            cls._db_session = None

        cls._mapper = None

    @property
    def db_session(cls):
        """Sqlalchemy database scoped session."""
        return cls._db_session

    @db_session.setter
    def db_session(cls, value):
        assert isinstance(value, scoped_session), \
            'An instance of sqlalchemy.orm.scoped_session is required.'
        cls._db_session = value

    @db_session.deleter
    def db_session(cls):
        cls._db_session = None

    def get_query(cls, arg, *args):
        """Execution of sqlalchemy session query method."""
        return cls.db_session.query(arg, *args)

    @property
    def query(cls):
        return cls.get_query(cls)

    @property
    def mapper(cls):
        """Cached property of sqlalchemy model mapper."""
        if cls._mapper is None:
            cls._mapper = inspect(cls)
        return cls._mapper

    def _build_query(
            cls, *conditions, joint=None, query=None, order_by=None, start=None,
            stop=None
    ):
        """Build session-based query with declared filter conditions, sorting
        and slicing."""
        query = query or cls.query

        if conditions:
            query = query.filter(_select_joint(joint)(*conditions))

        if order_by is not None:
            query = query.order_by(*_normalize_order_by(order_by))

        start = _get_abs_int(start)

        if start:
            query = query.offset(start)

        stop = _get_abs_int(stop)

        if stop:
            query = query.limit(stop - (start or 0))

        return query

    def all(cls, *args, **kwargs):
        """Fetching all entities with declared filter conditions, sorting and
        slicing."""
        return cls._build_query(*args, **kwargs).all()

    def first(cls, *args, **kwargs):
        """Fetching first entity with declared filter conditions, sorting and
        slicing."""
        return cls._build_query(*args, **kwargs).first()

    def create(cls, *args, **kwargs):
        """Create instance and add it into session."""
        item = cls(*args, **kwargs)

        cls._db_session.add(item)
        cls._db_session.flush()

        return item

    def truncate(cls, cascade=False, engine=None):
        """Truncate associated with declarative class SQL table."""
        if engine is None:
            engine = cls.db_session.get_bind()

        engine.execute(text(
            'TRUNCATE %s%s' % (
                cls.__table__.name,
                cascade and ' CASCADE' or ''
            )
        ).execution_options(autocommit=True))

    truncate_cascade = partialmethod(truncate, cascade=True)

    def byid(cls, *identities, first=False, **params):
        """Get instances by their primary keys."""
        if not identities:
            return

        query = cls.query.filter(or_(
            *_compile_primary_key_filter(cls.mapper.primary_key, *identities)
        ))

        method = first and cls.first or cls.all
        return method(query=query, **params)

    def __call__(cls, *args, **kwargs):
        """Initialization of child class with proper filtration of input
        keyword arguments, consireding sqlalchemy hybrid properties."""
        return super().__call__(*args, **_filter_kwargs(cls.mapper, kwargs))

    def commit(cls):
        """Short link to database session commit."""
        cls._db_session.commit()

    def flush(cls):
        """Short link to database session flush."""
        cls._db_session.flush()

    def rollback(cls):
        """Short link to database session rollback."""
        cls._db_session.rollback()
