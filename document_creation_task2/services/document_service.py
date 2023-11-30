from typing import Any, Dict, List

from document_creation_task2.db.DAO.dao_documents import DocumentDb


def delete_rows(ids: int, db: Any) -> Dict[str, Any]:
    """Delete rows.

    :param ids:id of the document
    :param db:The session
    :returns:The status of the operation.
    """
    documentdb = DocumentDb()
    documentdb.delete_rows_db(ids, db)
    return {
        "status": "success",
        "message": "successfully deleted these rows",
        "data": "deleted",
        "error": False,
    }


def sort_tasks(db: Any, ids: Any) -> List[Dict[str, Any]]:
    """Sort documents.

    :param db:The session
    :param ids:The id of the user.
    :returns:The sorted documents.
    """
    documentdbs = DocumentDb()
    tasks = documentdbs.tasks_db(db, ids)
    sorted_tasks = []
    for task in tasks:
        sorted_tasks.append(
            {
                "task_name": task.task_name,
                "task_date": task.task_date,
                "task_time": task.task_time,
                "priority": task.priority,
                "created_time": task.created_time,
                "is_complete": task.is_complete,
            },
        )
    return sorted_tasks
