from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    nom = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), nullable=False)

    filiere = db.Column(db.String(100))

    promotion = db.Column(db.String(20))

    entreprise = db.Column(db.String(100))

    bio = db.Column(db.Text)

    photo = db.Column(db.String(255), nullable=True)


class MentorRequest(db.Model):
    __tablename__ = 'mentor_requests'

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    mentor_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default='en_attente'
    )

    date_creation = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    student = db.relationship(
        'User',
        foreign_keys=[student_id]
    )

    mentor = db.relationship(
        'User',
        foreign_keys=[mentor_id]
    )


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    message = db.Column(
        db.String(255),
        nullable=False
    )

    lu = db.Column(
        db.Boolean,
        default=False
    )

    date_creation = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        'User',
        foreign_keys=[user_id]
    )


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)

    sender_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    receiver_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    contenu = db.Column(
        db.Text,
        nullable=False
    )

    date_envoi = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    sender = db.relationship(
        'User',
        foreign_keys=[sender_id]
    )

    receiver = db.relationship(
        'User',
        foreign_keys=[receiver_id]
    )


class Opportunity(db.Model):
    __tablename__ = 'opportunities'

    id = db.Column(db.Integer, primary_key=True)

    titre = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    type = db.Column(
        db.String(20),
        nullable=False
    )

    entreprise = db.Column(
        db.String(150),
        nullable=False
    )

    lieu = db.Column(
        db.String(150)
    )

    date_publication = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    alumni_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    alumni = db.relationship(
        'User',
        foreign_keys=[alumni_id]
    )



class Recommendation(db.Model):
    __tablename__ = 'recommendations'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    alumni_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

    date_creation = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

