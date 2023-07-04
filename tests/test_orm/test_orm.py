import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bot.models import History, Base, CurrentUserLanguage


@pytest.fixture(scope="session")
def sqlalchemy_connect_url():
    # Use SQLite in memory
    connect_url = "sqlite:///:memory:"
    return connect_url


@pytest.fixture
def dbsession(sqlalchemy_connect_url):
    engine = create_engine(sqlalchemy_connect_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create tables
    Base.metadata.create_all(bind=engine)

    yield session

    # Delete tables
    Base.metadata.drop_all(bind=engine)
    session.close()


def test_save_history(dbsession):
    test_history = History(user_id=1,
                           source_lang_code='en',
                           text='text',
                           target_lang_code='ru',
                           translated_text='текст')
    dbsession.add(test_history)
    dbsession.commit()
    queryset = dbsession.query(History).filter_by(user_id=1).one()
    assert queryset == test_history


def test_save_current_lang(dbsession):
    test_current_lang = CurrentUserLanguage(user_id=1, current_lang_code='ru')
    dbsession.add(test_current_lang)
    dbsession.commit()
    queryset = dbsession.query(CurrentUserLanguage).filter_by(user_id=1).one()
    assert queryset == test_current_lang
