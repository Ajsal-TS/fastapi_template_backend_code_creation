from datetime import datetime
from typing import Any, Dict, List

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from document_creation_task2.db.models.users import Task
from document_creation_task2.documents.document_schema import TaskDetail


class DocumentDb:
    """Class for documents db methods."""

    def create_task(self, task_data: Any, db: Any, ids: int) -> Dict[str, Any]:
        """
        To create a task.

        :param task_data:Contains the detail to add.
        :param db:The session.
        :param ids:The user id.

        :returns:The status of operation.

        :raises HTTPException:Server error.
        """
        try:
            new_task = Task(
                task_name=task_data.task_name,
                task_date=task_data.task_date,
                task_time=task_data.task_time,
                priority=task_data.priority,
                created_time=datetime.utcnow(),
                user_id=ids,
                is_complete="Not Completed",
            )
            db.add(new_task)
            db.commit()
            return {
                "status": "success",
                "message": "successfully created a document",
                "data": [],
                "error": False,
            }
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create task",
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database Exception: {SQLAlchemyError}",
            )

    def update_func(self, ids: int, db: Any) -> Dict[str, Any]:
        """
        For changing to status completed the task.

        :param ids:The document id.
        :param db:The db session.

        :returns:The status of the operation.
        """
        db.query(Task).filter(Task.id == ids).update(
            {Task.is_complete: "Completed"},
            synchronize_session=False,
        )
        db.commit()
        return {
            "status": "success",
            "message": "successfully updated task completion.",
            "data": [],
            "error": False,
        }

    def tasks_db(self, db: Any, ids: int) -> List[Task]:
        """
        Order the document list.

        :param db:The session.
        :param ids:User id.

        :returns:sorted documents.

        :raises HTTPException:No Content.
        """
        tasks = (
            db.query(Task)
            .filter(Task.user_id == ids)
            .order_by(Task.task_date, Task.task_time)
            .all()
        )
        if not tasks:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
        return tasks

    def update_det(self, task: Any, task_data: Any, db: Any) -> TaskDetail:
        """
        Update the documents.

        :param db:The session.
        :param task:Task model.
        :param task_data:task update details.

        :returns:updated document.

        """
        task.task_name = task_data.task_name
        task.task_date = task_data.task_date
        task.priority = task_data.priority
        db.commit()

        return TaskDetail(
            task_name=task.task_name,
            task_date=task.task_date,
            task_time=task.task_time,
            priority=task.priority,
            is_complete=task.is_complete,
        )

    def delete_rows_db(self, ids: int, db: Any) -> None:
        """
        Delete a row.

        :param ids:The document id.
        :param db:The session.
        :raises HTTPException:The unauthorized user.
        """
        data = db.query(Task).filter(ids == Task.id).first()
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No Content",
            )
        task_to_delete = db.query(Task).filter(Task.id == ids).first()
        if not task_to_delete:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No Content",
            )
        db.delete(task_to_delete)
        db.commit()
