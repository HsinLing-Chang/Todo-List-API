from flask import Blueprint, request, jsonify
from functools import wraps
import jwt
from datetime import datetime
from schema import Task, select, Session, func
import os
from dotenv import load_dotenv
load_dotenv()
secret = os.getenv("SECRET")

task_bp = Blueprint("task", __name__, url_prefix="/task")


def check_JWT(func):
    @wraps(func)
    def wrapper(*args, **kwarg):
        try:
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return jsonify({"message": 'Token is missing!'}), 403
            # Extract the token from the Authorization header
            token = auth_header.split(" ")[1]
            user_info = jwt.decode(token, secret, algorithms="HS256")
            return func(user_info, *args, **kwarg)
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invaild token!"}), 403
    return wrapper


@task_bp.get("/all")  # for tasting
def get_task():
    try:
        with Session() as session:
            user_statement = select(Task).order_by(Task.id)
            tasks = session.scalars(user_statement).all()
            if not any(tasks):
                return jsonify({"message": "Task not found."}), 404
            return [task.to_dict() for task in tasks]
    except Exception as e:
        return jsonify({"message": f"Unexpected error occured: {e}"})


@task_bp.get("/myTask")
@check_JWT
def get_my_task(user_info):
    try:
        # setting page offset and limit
        page = request.args.get("page", default=1, type=int)
        limit_page = request.args.get("limit", default=10, type=int)
        offset = (page-1)*limit_page
        with Session() as session:
            task_stmt = select(Task).filter_by(
                user_email=user_info.get("email")).order_by(Task.id).offset(offset).limit(limit_page)
            tasks = session.scalars(task_stmt).all()
            print(tasks)
            if not any(tasks):
                return jsonify({"message": "Task not found. Please add new task."}), 404
            # caculate the total number of tasks
            total_count = session.query(func.count(Task.id)).filter_by(
                user_email=user_info.get("email")).scalar()
            page_info = {
                "page": page,
                "limit": limit_page,
                "total": total_count
            }
            result = [task.to_dict() for task in tasks]
            result.append(page_info)
            return result
    except Exception as e:
        return jsonify({"message": f"Unexpected error occured: {e}"})


@task_bp.get("myTask/<status>")
@check_JWT
def get_mytask_by_status(user_info, status):
    try:
        allow_status = {"todo", "in-progress", "done"}
        if status not in allow_status:
            raise ValueError
        page = request.args.get("page", default=1, type=int)
        limit_page = request.args.get("limit", default=10, type=int)
        offset = (page-1)*limit_page

        with Session() as session:
            task_stmt = select(Task).filter_by(
                user_email=user_info.get("email"), status=status).order_by(Task.id).offset(offset).limit(limit_page)
            tasks = session.scalars(task_stmt).all()
            if not any(tasks):
                return jsonify({"message": "Task not found. Please add new task."}), 404
            # caculate the total number of tasks
            total_count = session.query(func.count(Task.id)).filter_by(
                user_email=user_info.get("email"), status=status).scalar()
            page_info = {
                "page": page,
                "limit": limit_page,
                "total": total_count
            }
            result = [task.to_dict() for task in tasks]
            result.append(page_info)
            return result
    except ValueError:
        return jsonify({"Error": "Status must be one of the following: todo, in-progress, done "}), 400
    except Exception as e:
        return jsonify({"message": f"Unexpected error occured: {e}"})


@task_bp.post("/add")
@check_JWT
def add_task(user_info):
    try:
        description = request.form.get("description")
        status = request.form.get("status")

        if not description or not status:
            return jsonify({"message": "Description and status are required."}), 400

        with Session() as session:
            new_task = Task(user_email=user_info.get("email"),
                            description=description, status=status)
            session.add(new_task)
            session.commit()
            return jsonify({"message": "Task added successfully!"})
    except ValueError:
        return jsonify({"Error": "Status must be one of the following: todo, in-progress, done "}), 400
    except Exception as e:
        return f"{e}"


@task_bp.delete("/delete/<id>")
@check_JWT
def delete_task(user_info, id):
    try:
        with Session() as session:
            email = session.scalar(select(Task).filter_by(id=id,
                                                          user_email=user_info.get("email")))
            if not email:
                return jsonify({"message": "Invaild ID entered. Please try again."}), 400
            session.delete(email)
            session.commit()
        return jsonify({"message": f"Task has been deleted: {id}"})
    except Exception as e:
        return jsonify({"message": f"Unexpected error occured: {e}"})


@task_bp.patch("/update/<id>")
@check_JWT
def update_task(user_info, id):
    try:
        status = request.form.get("status")

        with Session() as session:
            task = session.query(Task).filter_by(
                id=id, user_email=user_info.get("email")).first()
            if not task:
                return jsonify({"message": "Task not found. Please try again."})
            task.status = status
            task.updateAt = datetime.now()
            session.commit()
            return jsonify({"message": "Task updated successfully!"})
    except ValueError:
        return jsonify({"Error": "Status must be one of the following: todo, in-progress, done "}), 400
    except Exception as e:
        return jsonify({"message": f"Unexpected error occured: {e}"})
