from datetime import date, time

from pydantic import BaseModel


class TaskCreate(BaseModel):
    """
    Model for creating document.

    :param BaseModel:Pydantic model.
    """

    task_name: str
    task_date: date
    task_time: time
    priority: str


class TaskDetail(BaseModel):
    """
    Model for details of document.

    :param BaseModel:Pydantic model.
    """

    task_name: str
    task_date: date
    task_time: time
    priority: str
    is_complete: str = "Not Completed"


class TaskUpdate(BaseModel):
    """
    Model for updating document.

    :param BaseModel:Pydantic model.
    """

    task_name: str
    task_date: date
    priority: str
