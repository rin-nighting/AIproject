from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from . import models, schemas, crud, websocket, database

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

manager = websocket.ConnectionManager()

@app.get("/api/test")
def test_chinese():
    """测试中文编码的接口"""
    return JSONResponse(
        content={"message": "你好世界", "test": "中文测试"},
        media_type="application/json; charset=utf-8"
    )

@app.get("/api/poll", response_model=schemas.PollBase)
def get_poll(db: Session = Depends(get_db)):
    poll = crud.get_poll_with_options(db, 1)
    return JSONResponse(content=schemas.PollBase.model_validate(poll).model_dump(), media_type="application/json; charset=utf-8")

@app.post("/api/poll/vote")
async def vote(vote: schemas.VoteRequest, db: Session = Depends(get_db)):
    option = crud.vote_option(db, vote.poll_id, vote.option_id)
    poll = crud.get_poll_with_options(db, vote.poll_id)
    # 广播最新票数
    await manager.broadcast({
        "poll_id": poll.id,
        "options": [
            {"id": o.id, "option_text": o.option_text, "vote_count": o.vote_count}
            for o in poll.options
        ]
    })
    return {"success": True}

@app.websocket("/ws/poll")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # 保持连接
    except WebSocketDisconnect:
        manager.disconnect(websocket) 