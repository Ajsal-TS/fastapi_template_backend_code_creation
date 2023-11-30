from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from document_creation_task2.authentication.authenticate import token_authenticate
from document_creation_task2.db.DAO.dao_documents import DocumentDb
from document_creation_task2.db.dependencies import get_db_session as get_db
from document_creation_task2.db.models.users import Task
from document_creation_task2.documents.document_schema import (
    TaskCreate,
    TaskDetail,
    TaskUpdate,
)
from document_creation_task2.services.document_service import delete_rows, sort_tasks

document_func = APIRouter()


@document_func.put("/task/create_task")
async def create_tasks(
    request: TaskCreate,
    ids: int = Depends(token_authenticate),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """
    Create documents for the current authorized user.

    :param request: Document schema.
    :param ids: ID of the current user.
    :param db: Session of the database.
    :return: Status of the response.
    :raises HTTPException: Thrown exception if user is not authorized.
    """
    if not ids:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    documentdbs = DocumentDb()
    return documentdbs.create_task(request, db, ids)


@document_func.get("/task/access_task", response_model=None)
async def access_document(
    id_value: int,
    db: Session = Depends(get_db),
    ids: int = Depends(token_authenticate),
) -> List[Task]:
    """
    Return documents of a given user.

    :param id_value: User ID.
    :param db: Database session. From Depends(get_db).
    :param ids: User ID obtained from token authentication.
    :return: The data of the user with the given task ID.

    :raises HTTPException:Unauthorized if authentication fails.
    """
    if not ids:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    data = (
        db.query(Task)
        .filter(
            Task.user_id == ids,
            Task.id == id_value,
        )
        .all()
    )
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Documents for user with ID {id_value} not found",
        )
    return data


@document_func.get("/task/sorting")
async def access_task(
    db: Session = Depends(get_db),
    ids: int = Depends(token_authenticate),
) -> List[Dict[str, Any]]:
    """
    Return sorted tasks for a given user.

    :param db: Database session. From Depends(get_db).
    :param ids: User ID obtained from token authentication.
    :return: Sorted tasks for the specified user.
    :raises HTTPException: 401 Unauthorized if authentication fails.
    """
    if not ids:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return sort_tasks(db, ids)


@document_func.put("/task/update_completion/{id}")
async def updated_value(
    id_values: int,
    db: Session = Depends(get_db),
    ids: int = Depends(token_authenticate),
) -> Dict[str, Any]:
    """
    Update the status of a task to complete.

    :param id_values: Task ID.
    :param db: Database session. Defaults to Depends(get_db).
    :param ids: User ID obtained from token authentication.
    :returns: Status of the update operation.
    :raises HTTPException: If the user is not authenticated.
    """
    if not ids:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    data = db.query(Task).filter(Task.id == id_values).all()
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Documents for user with ID {id_values} not found",
        )
    documentdbs = DocumentDb()
    return documentdbs.update_func(id_values, db)


@document_func.put("/tasks/update/{task_id}", response_model=TaskDetail)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    ids: int = Depends(token_authenticate),
) -> TaskDetail:
    """
    Update task details.

    :param task_id: Task ID.
    :param task_data: Task data to be updated.
    :param db: Database session. From Depends(get_db).
    :param ids: User ID obtained from token authentication.
    :return: Updated task details.
    :raises HTTPException: If the user is not authenticated.
    """
    if not ids:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    documentdbs = DocumentDb()
    return documentdbs.update_det(task, task_data, db)


@document_func.delete("/Documents/delete/{id}")
async def delete_row(
    id_value: int,
    db: Session = Depends(get_db),
    ids: int = Depends(token_authenticate),
) -> Dict[str, Any]:
    """
    Delete a specific document.

    :param id_value: Document ID.
    :param db: Database session.
    :param ids: User ID obtained from API key authentication.

    :returns:Result message indicating the success of the delete operation.
    :raises HTTPException: If the API key is incorrect (status code 401).
    """
    if not ids:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return delete_rows(id_value, db)


@document_func.delete("/tasks/clear")
async def clear_all_tasks(
    db: Session = Depends(get_db),
    ids: int = Depends(token_authenticate),
) -> Dict[str, Any]:
    """To delete all the task.

    :param db:Session.
    :param ids: Id of user.Default to Depends.
    :returns:The status message.
    :raises HTTPException: Unauthorized User.
    """
    if not ids:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    tasks_to_delete = db.query(Task).all()
    if not tasks_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tasks to clear",
        )
    for task in tasks_to_delete:
        db.delete(task)
    db.commit()
    return {"message": "All tasks cleared successfully"}
