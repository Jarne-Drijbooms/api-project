import datetime as _dt
import sqlalchemy as _sql
import sqlalchemy.orm as _orm

import database as _database

class Player(_database.Base):
    __tablename__ = "players"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    playernumber = _sql.Column(_sql.Integer, unique=True, index=True)
    firstname = _sql.Column(_sql.String)
    lastname = _sql.Column(_sql.String)
    is_active = _sql.Column(_sql.Boolean, default=True)
    posts = _orm.relationship('Post', back_populates="owner")

class Post(_database.Base):
    __tablename__ = "posts"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    currentclub = _sql.Column(_sql.String, index=True)
    age = _sql.Column(_sql.Integer, index=True)
    position = _sql.Column(_sql.String, index=True)
    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey('players.id'))
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    date_last_updated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    owner = _orm.relationship('Player', back_populates="posts")