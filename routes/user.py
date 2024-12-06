from flask import jsonify, Blueprint, request
from schema import Session, select, User, func
import jwt
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv
load_dotenv()

user_bp = Blueprint("user", __name__, url_prefix="/user")
secret = os.getenv("SECRET")


@user_bp.get("/")  # get all user info
def user_list():
    try:
        # setting page offset and limit
        page = request.args.get("page", 1, type=int)
        limit_page = request.args.get("limit", 10, type=int)
        offset = (page-1) * limit_page

        with Session() as session:
            user_stmt = select(User).order_by(
                User.id).offset(offset).limit(limit_page)
            all_users = session.scalars(user_stmt).all()
            # check if user is empty
            if not any(all_users):
                return jsonify({"message": "No users found."}), 404
            # calculate the total number of users
            count_stmt = select(func.count()).select_from(User)
            total_count = session.execute(count_stmt).scalar_one()
            page_info = {
                "page": page,
                "limit": limit_page,
                "total": total_count
            }
            # add page info to the result
            result = [user.to_dict() for user in all_users]
            result.append(page_info)
            return result
    except Exception as e:
        return jsonify({"Unexpected error occured": e}), 500


@user_bp.post("/register")  # register new user
def sign_up():
    try:
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        if not username or not email or not password:
            return jsonify({"message": "Username, email, and password are required."}), 400
        with Session() as session:
            find_user = session.scalar(select(User).filter_by(email=email))
            if find_user:
                return jsonify({"message": "The mail has already been registered. Please try another one."})
            new_user = User(username=username,
                            email=email, password=password)
            session.add(new_user)
            session.commit()
            return jsonify({"message": "User created successfully. "}), 201
    except ValueError:
        return jsonify({"Invalid email": f" {email}"}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error occured: {e}"}), 500


@user_bp.post('/login')  # login
def login():
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        if not email or not password:
            return jsonify({"message": "Email and password cannot be empty."})
        with Session() as session:
            user_statement = select(User).filter_by(email=email)
            user = session.scalar(user_statement)
            if user and user.unhash_value(password, user.password):
                payload = {
                    "username": user.username,
                    "email": user.email,
                    "iat": datetime.now(tz=timezone.utc),  # issue time
                    "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=60),
                }
                token = jwt.encode(payload, secret, algorithm="HS256")
                return jsonify({"message": f"{user.username} login successfully!", "token": "Bearer "+token})
            else:
                return jsonify({"message": "The mail has already been registered. Please try another one."}), 400
    except Exception as e:
        return jsonify({"Unexpected error occured": e})
