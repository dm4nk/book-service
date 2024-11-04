import uuid

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    customer_id = db.Column(db.String(36), nullable=True)
