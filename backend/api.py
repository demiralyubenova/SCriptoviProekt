import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
from db import DBInteractor
from session import Sessions

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///socialmedia.db'

# Allow CORS for all domains
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

db_interactor = DBInteractor()
sessions = Sessions()

@app.before_request
def check_session():
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH',
            'Access-Control-Allow-Headers': 'Authorization, Content-Type',
        }
        return ('', 204, headers)  # Handle preflight requests with 204 status

    if request.path in ['/login', '/register']:
        return  # Skip session check for these endpoints

    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Authorization header is missing"}), 401

    token = token.split("Bearer ")[-1]
    if not sessions.validate_token(token):
        return jsonify({"error": "Invalid or expired token"}), 401

    request.user = sessions.get_token(token)
    usr_obj = db_interactor.get_user_repository().get_by_username(request.user.username)
    request.user.user_id = usr_obj.id

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if len(password) < 6:
            return jsonify({"err": "Password must have a length of at least 6 characters"}), 400
        user = db_interactor.get_user_repository().create(username, password)
        return jsonify({"id": user.id, "username": user.username}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user = db_interactor.get_user_repository().get_by_username(username)
        if user and user.password == password:
            token = sessions.issue_new_token(user.username)
            return jsonify(access_token=token), 200
        return jsonify({"msg": "Bad username or password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = db_interactor.get_user_repository().get_all()
        return jsonify([{"id": user.id, "username": user.username} for user in users]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/posts', methods=['POST'])
def create_post():
    try:
        user_id = request.user.user_id
        data = request.get_json()
        print("ffff",data)

        content = data.get('content')
        post = db_interactor.get_post_repository().create(user_id, content)
        return jsonify({"id": post.id, "content": post.content}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/posts', methods=['GET', 'OPTIONS'])
def get_all_posts():
    try:
        posts = db_interactor.get_post_repository().get_all()
        return jsonify([{"id": post.id, "content": post.content, "likes": post.likes} for post in posts]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/posts/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    try:
        post_repo = db_interactor.get_post_repository()
        post = post_repo.get_by_id(post_id)
        if post:
            post_repo.like(post)
            return jsonify({"msg": "Post liked", "likes": post.likes}), 200
        return jsonify({"msg": "Post not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/posts/<int:post_id>/comments', methods=['POST'])
def create_comment(post_id):
    try:
        user_id = request.user.user_id
        data = request.get_json()
        content = data.get('content')
        comment = db_interactor.get_comments_repository().create(user_id, post_id, content)
        return jsonify({"id": comment.id, "content": comment.content}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/posts/<int:post_id>', methods=['PATCH'])
def update_post(post_id):
    try:
        user_id = request.user.user_id
        data = request.get_json()
        print(data)
        content = data.get('content')
        print("popo",content)
        
        post_repo = db_interactor.get_post_repository()
        post = post_repo.get_by_id(post_id)
        if post:
            print(post.user_id)
            print(request.user.user_id)
            if post.user_id == request.user.user_id:
                post_repo.update(post, content)
                return jsonify({"msg": "Post updated successfully"}), 200
            return jsonify({"msg": "Unauthorized"}), 403
        return jsonify({"msg": "Post not found"}), 404
    except Exception as e:
        print(e)
        traceback.print_exc()  
        return jsonify({"error": str(e)}), 500

@app.route('/posts/<int:post_id>', methods=['PUT'])
def replace_post(post_id):
    try:
        user_id = request.user.user_id
        data = request.get_json()
        content = data.get('content')
        post_repo = db_interactor.get_post_repository()
        post = post_repo.get_by_id(post_id)
        if post:
            if post.user_id == user_id:
                post_repo.replace(post_id, content)
                return jsonify({"msg": "Post replaced successfully"}), 200
            return jsonify({"msg": "Unauthorized"}), 403
        return jsonify({"msg": "Post not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    try:
        user_id = request.user.user_id
        post_repo = db_interactor.get_post_repository()
        post = post_repo.get_by_id(post_id)
        if post:
            if post.user_id == user_id:
                post_repo.delete(post)
                return '', 204
            return jsonify({"msg": "Unauthorized"}), 403
        return jsonify({"msg": "Post not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    try:
        comments = db_interactor.get_comments_repository().get_by_post_id(post_id)
        return jsonify([{"id": comment.id, "content": comment.content} for comment in comments]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
