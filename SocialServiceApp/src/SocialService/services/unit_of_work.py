from __future__ import annotations
import abc
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from SocialService import config
from SocialService.adapters import repository

logger = logging.getLogger(__name__)

class AbstractUnitOfWork(abc.ABC):
    services: repository.AbstractSocialServicesRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        try:
            self._commit()
        except Exception as e:
            self.rollback()
            raise e

    def collect_new_events(self):
        for service in self.services.seen:
            while service.events:
                yield service.events.pop(0)

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        config.get_sqlite_file_url(),
        isolation_level="SERIALIZABLE",
        pool_size=10
    )
)

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()  # type: Session
        self.services = repository.SqlAlchemySocialServicesRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def rollback(self):
        self.session.rollback()
        logger.info("Rollback performed.")

