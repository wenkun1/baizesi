from sqlalchemy import *

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class SessionRe0cord(Base):

    __tablename__ = "ai_session"

    id = Column(
        BigInteger,
        primary_key=True
    )

    user_id = Column(String(50))

    intent = Column(String(100))

    slot_data = Column(JSON)

    status = Column(String(20))

    current_question = Column(String(100))


class FormRecord(Base):

    __tablename__ = "form_record"

    id = Column(
        BigInteger,
        primary_key=True
    )

    user_id = Column(String(50))

    intent = Column(String(100))

    slot_data = Column(JSON)