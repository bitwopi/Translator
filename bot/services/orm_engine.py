from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from bot.models import History, CurrentUserLanguage

# Initialize db connection
engine = create_engine('sqlite:///translator_db.db?check_same_thread=False')


def save_translation_to_history(user_id: int, src_lang_code: str, text: str, targ_lang_code: str, translated_text: str):
    with Session(engine) as session:
        history_obj = History(user_id=user_id,
                              source_lang_code=src_lang_code,
                              text=text,
                              target_lang_code=targ_lang_code,
                              translated_text=translated_text)
        try:
            session.add(history_obj)
            session.commit()
            return 0
        except Exception as e:
            session.rollback()
            print(e)
            return 1


def save_current_user_lang(user_id: int, current_lang_code: str):
    with Session(engine) as session:
        queryset = session.query(CurrentUserLanguage).filter_by(user_id=user_id).first()
        if queryset:
            queryset.current_lang_code = current_lang_code
        else:
            session.add(CurrentUserLanguage(user_id=user_id, current_lang_code=current_lang_code))
        try:
            session.commit()
            return 0
        except Exception as e:
            session.rollback()
            print(e)
            return 1


def get_user_current_language(user_id: int):
    with Session(engine) as session:
        queryset = session.query(CurrentUserLanguage.current_lang_code).filter_by(user_id=user_id).one()
        return queryset


def get_user_history(user_id: int):
    with Session(engine) as session:
        queryset = session.query(History).filter_by(user_id=user_id).all()
        return queryset


def delete_user_history(user_id: int):
    with Session(engine) as session:
        try:
            session.query(History).filter_by(user_id=user_id).delete()
            session.commit()
            return 0
        except Exception as e:
            session.rollback()
            print(e)
            return 1

