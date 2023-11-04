from typing import List
import fastapi as _fastapi
import sqlalchemy.orm as _orm
import services as _services, schema as _schemas
from fastapi.middleware.cors import CORSMiddleware
app = _fastapi.FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
_services.create_databases()

@app.post("/Players/", response_model=_schemas.Player)
def create_player(player: _schemas.PlayerCreate, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    db_player = _services.get_player_by_playernumber(db=db, playernumber=player.playernumber)
    if db_player:
        raise _fastapi.HTTPException(status_code=400, detail="woops the playernumber is in use")
    return _services.create_player(db=db, player=player)

@app.get("/Players/", response_model=List[_schemas.Player])
def read_players(skip: int=0,limit: int=30,db: _orm.Session=_fastapi.Depends(_services.get_db)):
    players= _services.get_players(db=db, skip=skip, limit=limit)
    return players

@app.get("/Players/{player_id}", response_model=_schemas.Player)
def read_player(player_id: int, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    db_player = _services.get_player(db=db, player_id=player_id)
    if db_player is None:
        raise _fastapi.HTTPException(status_code=404, detail="sorry this player does not exist")
    return db_player

@app.post("/Players/{player_id}/posts/", response_model=_schemas.Post)
def create_post(player_id: int, post: _schemas.PostCreate, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    db_player = _services.get_player(db=db, player_id=player_id)
    if db_player is None:
        raise _fastapi.HTTPException(status_code=404, detail="sorry this player does not exist")
    return _services.create_post(db=db, post=post, player_id=player_id)

@app.delete("/players/{player_id}")
def delete_player(player_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    _services.delete_player(db=db, player_id=player_id)
    return {"message": f"successfully deleted player with id: {player_id}"}

@app.get("/posts/", response_model=List[_schemas.Post])
def read_posts(skip: int=0,limit: int=30,db: _orm.Session=_fastapi.Depends(_services.get_db)):
    posts = _services.get_posts(db=db, skip=skip, limit=limit)
    return posts
@app.get("/posts/{post_id}", response_model=_schemas.Post)
def read_post(post_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    post =  _services.get_post(db=db, post_id=post_id)
    if post is None:
        raise _fastapi.HTTPException(status_code=404, detail="sorry this post does not exist")
    return post

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    _services.delete_post(db=db, post_id=post_id)
    return {"message": f"successfully deleted post with id: {post_id}"}

@app.put("/posts/{post_id}", response_model=_schemas.Post)
def update_post(post_id: int, post: _schemas.PostCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return _services.update_post(db=db, post=post, post_id=post_id)