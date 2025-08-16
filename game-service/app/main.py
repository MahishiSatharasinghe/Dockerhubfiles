from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, database

app = FastAPI(
    title="Game Service",
    root_path="/api/games",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

models.Base.metadata.create_all(bind=database.engine)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "FastAPI is live!"}

@app.post("/games/", response_model=schemas.Game)
def create_game(game: schemas.GameCreate, db: Session = Depends(get_db)):
    db_game = models.Game(**game.dict())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

@app.get("/games/", response_model=list[schemas.Game])
def get_games(db: Session = Depends(get_db)):
    return db.query(models.Game).all()

@app.get("/games/{game_id}", response_model=schemas.Game)
def get_game(game_id: int, db: Session = Depends(get_db)):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@app.put("/games/{game_id}", response_model=schemas.Game)
def update_game(game_id: int, game_data: schemas.GameCreate, db: Session = Depends(get_db)):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    for key, value in game_data.dict().items():
        setattr(game, key, value)
    db.commit()
    db.refresh(game)
    return game

@app.delete("/games/{game_id}")
def delete_game(game_id: int, db: Session = Depends(get_db)):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    db.delete(game)
    db.commit()
    return {"message": "Game deleted"}
