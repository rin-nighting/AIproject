from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Poll(Base):
    __tablename__ = "poll"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(255), nullable=False)
    options = relationship("PollOption", back_populates="poll")

class PollOption(Base):
    __tablename__ = "poll_option"
    id = Column(Integer, primary_key=True, index=True)
    poll_id = Column(Integer, ForeignKey("poll.id"), nullable=False)
    option_text = Column(String(100), nullable=False)
    vote_count = Column(Integer, default=0)
    poll = relationship("Poll", back_populates="options") 