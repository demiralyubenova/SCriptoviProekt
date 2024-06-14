from flask import Flask, request, jsonify
from functools import wraps
from db import DBInteractor
from session import Sessions
from flask_cors import CORS
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///socialmedia.db'
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})
app.config['CORS_HEADERS'] = 'Content-Type'
db_interactor = DBInteractor()
sessions = Sessions()

@app.before_request
def check_session():
    # Skip validation for login and register endpoints
    (request.path)
    if request.method == 'OPTIONS':
        # Let the preflight request through
        return jsonify({'status': 'Preflight check'}), 200
    if request.path in ['/login', '/register']:
        return

    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Authorization header is missing"}), 401

    token = token.split("Bearer ")[-1]
    if not sessions.validate_token(token):
        return jsonify({"error": "Invalid or expired token"}), 401

    request.user = sessions.get_token(token)
    print(request.user)
    usr_obj = db_interactor.get_user_repository().get_by_username(request.user.username)
    request.user.user_id = usr_obj.id

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = db_interactor.get_user_repository()
    user = user.create(username, password)
    return jsonify({"id": user.id, "username": user.username}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = db_interactor.get_user_repository()
    user = user.get_by_username(username)
    if user and user.password == password:
        token = sessions.issue_new_token(user.username)
        return jsonify(access_token=token), 200
    return jsonify({"msg": "Bad username or password"}), 401

@app.route('/users', methods=['GET'])
def get_all_users():
    user = db_interactor.get_user_repository()
    users = user.get_all()
    return jsonify([{"id": user.id, "username": user.username} for user in users]), 200

@app.route('/posts', methods=['POST'])
def create_post():
    user_id = request.user.user_id
    print("user",user_id)
    data = request.get_json()
    content = data.get('content')
    post_repo = db_interactor.get_post_repository()
    print("content",content)
    post = post_repo.create(user_id, content)
    return jsonify({"id": post.id, "content": post.content}), 201

@app.route('/posts', methods=['GET','OPTIONS'])
def get_all_posts():
    post_repo = db_interactor.get_post_repository()
    posts = post_repo.get_all()
    return jsonify([{"id": post.id, "content": post.content, "likes": post.likes} for post in posts]), 200

@app.route('/posts/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    post_repo = db_interactor.get_post_repository()
    post = post_repo.get_by_id(post_id)
    if post:
        post_repo.like(post)
        return jsonify({"msg": "Post liked", "likes": post.likes}), 200
    return jsonify({"msg": "Post not found"}), 404

@app.route('/posts/<int:post_id>/comments', methods=['POST'])
def create_comment(post_id):
    user_id = request.user.user_id
    data = request.get_json()
    content = data.get('content')
    comments = db_interactor.get_comments_repository()
    comment = comments.create(user_id, post_id, content)
    return jsonify({"id": comment.id, "content": comment.content}), 201

@app.route('/posts/<int:post_id>', methods=['PATCH'])
def update_post(post_id):
    user_id = request.user.user_id
    data = request.get_json()
    content = data.get('content')
    
    post_repo = db_interactor.get_post_repository()
    post = post_repo.get_by_id(post_id)
    if post and post.user_id == user_id:
        post_repo.update(post_id, content)
        return jsonify({"msg": "Post updated successfully"}), 200
    else:
        return jsonify({"msg": "Post not found or unauthorized"}), 404


@app.route('/posts/<int:post_id>', methods=['PUT'])
def replace_post(post_id):
    user_id = request.user.user_id
    data = request.get_json()
    content = data.get('content')
    
    post_repo = db_interactor.get_post_repository()
    post = post_repo.get_by_id(post_id)
    if post and post.user_id == user_id:
        post_repo.replace(post_id, content)
        return jsonify({"msg": "Post replaced successfully"}), 200
    else:
        return jsonify({"msg": "Post not found or unauthorized"}), 404


@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    user_id = request.user.user_id
    
    post_repo = db_interactor.get_post_repository()
    post = post_repo.get_by_id(post_id)
    if post and post.user_id == user_id:
        post_repo.delete(post)
        return jsonify({"msg": "Post deleted successfully"}), 200
    else:
        return jsonify({"msg": "Post not found or unauthorized"}), 404



@app.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    comments = db_interactor.get_comments_repository()
    comments = comments.get_by_post_id(post_id)
    return jsonify([{"id": comment.id, "content": comment.content} for comment in comments]), 200

if __name__ == "__main__":
    app.run(debug=True)
 