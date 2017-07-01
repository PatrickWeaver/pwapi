from app import db

class BaseModel(db.Model):
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

class Post(BaseModel):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True)
    post_title = db.Column(db.String(255))
    post_body = db.Column(db.String(255))
    post_date = db.Column(db.Date)
    created_at = db.Column(db.Date)
