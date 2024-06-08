from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Post, Comment

DATABASE_URL = 'sqlite:///socialmedia.db'

class DBInteractor:
    def __init__(self, database_url=DATABASE_URL):
        self.engine = create_engine(database_url)
        
        self.Session = sessionmaker(bind=self.engine)


    def setup_db(self): # run only if the db is not init-ed
        Base.metadata.create_all(self.engine)

    class UserRepository:
        def __init__(self, session):
            self.session = session

        def get_all(self):
            return self.session.query(User).all()

        def get_by_username(self, username):
            return self.session.query(User).filter_by(username=username).first()

        def create(self, username, password):
            new_user = User(username=username, password=password)
            self.session.add(new_user)
            self.session.commit()
            return new_user

        
        def update(self, user, username=None, password=None):
            if username:
                user.username = username
            if password:
                user.password = password
            self.session.commit()
            return user

        def delete(self, user):  # ask if it should query the object here or delete the object directly
            self.session.delete(user)
            self.session.commit()

    class PostRepository:
        def __init__(self, session):
            self.session = session

        def get_all(self):
            return self.session.query(Post).all()

        def get_by_id(self, post_id):
            return self.session.query(Post).get(post_id)

        def create(self, user_id, content):
            new_post = Post(user_id=user_id, content=content)
            self.session.add(new_post)
            self.session.commit()
            return new_post

        def update(self, post, content=None):
            if content:
                post.content = content
            self.session.commit()
            return post

        def delete(self, post):
            self.session.delete(post)
            self.session.commit()

        def like(self, post):
            post.likes += 1
            self.session.commit()
            return post

    class CommentRepository:
        def __init__(self, session):
            self.session = session

        def get_by_post_id(self, post_id):
            return self.session.query(Comment).filter_by(post_id=post_id).all()

        def create(self, user_id, post_id, content):
            new_comment = Comment(user_id=user_id, post_id=post_id, content=content)
            self.session.add(new_comment)
            self.session.commit()
            return new_comment

        def update(self, comment, content=None):
            if content:
                comment.content = content
            self.session.commit()
            return comment

        def delete(self, comment):
            self.session.delete(comment)
            self.session.commit()

    def get_user_repository(self):
        session = self.Session()
        return self.UserRepository(session)

    def get_post_repository(self):
        session = self.Session()
        return self.PostRepository(session)

    def get_comment_repository(self):
        session = self.Session()
        return self.CommentRepository(session)
"to do -> make a function which chrcks if the db is set up"
is_db__set_up = False
db_interactor = DBInteractor()

if is_db__set_up :
    db_interactor.setup_db()
