from project import db
from datetime import datetime


class Message(db.Model):

    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',
                                                  ondelete='CASCADE'))
    likes = db.relationship('Like', backref = 'message', lazy='dynamic')

    def __init__(self, text, user_id, timestamp=datetime.utcnow()):
        self.text = text
        self.user_id = user_id
        self.timestamp = timestamp


class Like(db.Model):

    __tablename__='likes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',
                                                  ondelete='CASCADE'))
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id',
                                                  ondelete='CASCADE'))

    def __init__(self, user_id, message_id):
        self.user_id = user_id
        self.message_id = message_id
        