from sqlalchemy import create_engine
from models import Base, User, Post, Comment
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
DATABASE_URL = 'sqlite:///socialmedia.db'

class DBInteractor:
    def __init__(self, database_url='sqlite:///socialmedia.db'):
        self.engine = create_engine(database_url)
        self.Session = scoped_session(sessionmaker(bind=self.engine)) # to prevent multiple sessions

    def setup_db(self):
        Base.metadata.create_all(self.engine)

    def is_db_set_up(self):
        session = self.Session()
        try:
            session.query(User).first()
            return True
        except OperationalError:
            return False
        finally:
            session.close()

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

        def delete(self, user):
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

db_interactor = DBInteractor()

if not db_interactor.is_db_set_up():
    db_interactor.setup_db()