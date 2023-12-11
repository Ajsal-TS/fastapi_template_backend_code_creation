from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship

from document_creation_task2.db.base import Base as Bases


class UserDet(Bases):
    """
    User details model.

    :param Bases:Model base.
    """

    __tablename__ = "user_det"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    email = Column(String)
    tok = relationship("Token", back_populates="user_det")
    tasks = relationship("Task", back_populates="user_dets")


class Token(Bases):
    """
    Token model.

    :param Bases:Model base.
    """

    __tablename__ = "token"
    id = Column(Integer, primary_key=True)
    accesstype = Column(String)
    user_id = Column(Integer, ForeignKey("user_det.id"))
    user_det = relationship("UserDet", back_populates="tok")


class Task(Bases):
    """
    Task model.

    :param Bases:Model base.
    """

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String)
    task_date = Column(Date)
    task_time = Column(Time(timezone=True))
    priority = Column(String)
    created_time = Column(DateTime)
    is_complete = Column(String)
    user_id = Column(Integer, ForeignKey("user_det.id"))
    user_dets = relationship("UserDet", back_populates="tasks")


class RevokedToken(Bases):
    """
    Revoked Token model.

    :param Bases:Model base.
    """

    __tablename__ = "revoked_tokens"
    token = Column(String, primary_key=True)
