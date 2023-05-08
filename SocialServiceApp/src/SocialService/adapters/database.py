from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from SocialService.adapters.orm import start_mappers, metadata


def create_session_factory(database_url: str = "sqlite:///social_services.db"):
    engine = create_engine(database_url)
    create_tables(engine)
    start_mappers()
    return sessionmaker(bind=engine)


def create_tables(engine):
    metadata.create_all(engine)


@contextmanager
def get_session(session_factory):
    session = session_factory()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
