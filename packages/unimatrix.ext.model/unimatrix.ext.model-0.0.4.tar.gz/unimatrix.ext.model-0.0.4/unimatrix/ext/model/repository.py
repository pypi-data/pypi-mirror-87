"""Declares :class:`Repository`."""
import abc


class Repository(metaclass=abc.ABCMeta):
    """The base class for all :term:`Repository` implementations."""

    #: Raised when a new entity with an existing key is being persisted.
    Duplicate = type('Duplicate', (Exception,), {})

    #: Raised when an entity is requested with a search predicate that
    #: yielded no result.
    DoesNotExist = type('DoesNotExist', (Exception,), {})

    #: Raised when an entity is requested but the search predicated yielded
    #: more than one result.
    MultipleObjectsReturned = type('MultipleObjectsReturned', (Exception,), {})

    @classmethod
    def class_factory(cls, impl):
        """Create a new :class:`Repository` subclass using the
        provided implementation class `impl`.
        """
        return type('%sRepository' % impl.__name__, (impl, cls), {
            '__module__': impl.__module__,
            '_in_transaction': False
        })

    @classmethod
    def new(cls, impl, *args, **kwargs):
        """Create a new instance with the specified implementation class."""
        return cls.class_factory(impl)(*args, **kwargs)

    def __init__(self):
        self._in_transaction = False

    def with_context(self, *args, **kwargs):
        """Hook that is executed when a transaction is started."""
        if self._in_transaction:
            raise RuntimeError("Nested transactions are not supported.")
        repo = type(self)()
        repo._in_transaction = True
        repo.setup_context(*args, **kwargs)
        return repo

    def setup_context(self, *args, **kwargs):
        """Hook to setup the context."""
        pass

    def teardown_context(self, cls, exc, tb):
        """Hook to teardown the context."""
        pass

    def __enter__(self):
        return self

    def __exit__(self, cls, exc, tb):
        self.teardown_context(cls, exc, tb)

    async def __aenter__(self):
        return self

    async def __aexit__(self, cls, exc, tb):
        pass
