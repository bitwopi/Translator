from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class History(Base):
    __tablename__ = "user_history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer())
    source_lang_code: Mapped[str] = mapped_column(String(2))
    text: Mapped[str] = mapped_column(String(10000))
    target_lang_code: Mapped[str] = mapped_column(String(2))
    translated_text: Mapped[str] = mapped_column(String(10000))

    def __repr__(self):
        return f"({self.source_lang_code}) {self.text} => ({self.target_lang_code}) {self.translated_text}\n"


class CurrentUserLanguage(Base):
    __tablename__ = "current_user_language"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    current_lang_code: Mapped[str] = mapped_column(String(2))

    def __repr__(self):
        return f"user: {self.user_id}, current_language: {self.current_lang_code}"
