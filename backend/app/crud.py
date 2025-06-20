from sqlalchemy.orm import Session
from . import models

def get_poll(db: Session, poll_id: int):
    return db.query(models.Poll).filter(models.Poll.id == poll_id).first()

def vote_option(db: Session, poll_id: int, option_id: int):
    option = db.query(models.PollOption).filter(
        models.PollOption.poll_id == poll_id,
        models.PollOption.id == option_id
    ).first()
    if option:
        option.vote_count += 1
        db.commit()
        db.refresh(option)
    return option

def get_poll_with_options(db: Session, poll_id: int):
    return db.query(models.Poll).filter(models.Poll.id == poll_id).first() 