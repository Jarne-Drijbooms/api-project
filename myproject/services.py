import datetime as _dt
import sqlalchemy.orm as _orm
import database as _database, models as _models, schema as _schemas

def create_databases():
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_player_by_playernumber(db: _orm.Session, playernumber: int):
    return db.query(_models.Player).filter(_models.Player.playernumber == playernumber).first()

def create_player(db: _orm.Session, player: _schemas.PlayerCreate):
    db_player = _models.Player(playernumber=player.playernumber, firstname=player.firstname, lastname=player.lastname)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def get_players(db: _orm.Session, skip:int, limit:int):
    return db.query(_models.Player).offset(skip).limit(limit).all()

def get_player(db: _orm.Session, player_id: int):
    return db.query(_models.Player).filter(_models.Player.id == player_id).first()

def delete_player(db: _orm.Session,player_id: int):
    db.query(_models.Player).filter(_models.Player.id== player_id).delete()
    db.commit()

def create_post(db:_orm.Session, post: _schemas.PostCreate, player_id: int):
    post = _models.Post(**post.dict(), owner_id=player_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_posts(db: _orm.Session, skip: int, limit: int):
    return db.query(_models.Post).offset(skip).limit(limit).all()

def get_post(db: _orm.Session, post_id: int):
    return db.query(_models.Post).filter(_models.Post.id == post_id).first()

def delete_post(db: _orm.Session,post_id: int):
    db.query(_models.Post).filter(_models.Post.id == post_id).delete()
    db.commit()

def update_post(db: _orm.Session, post: _schemas.PostCreate, post_id: int):
    db_post = get_post(db=db, post_id=post_id)
    db_post.currentclub = post.currentclub
    db_post.age = post.age
    db_post.position = post.position
    db_post.date_last_updated = _dt.datetime.utcnow()
    db.commit()
    db.refresh(db_post)
    return db_post

