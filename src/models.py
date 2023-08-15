from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, ConfigDict

from .database import Base


class MatchORM(Base):
    """ORM sqlalchemy representation"""

    __tablename__ = "match"

    match_id = Column(Integer, primary_key=True, index=True)
    team_a_name = Column(String, nullable=False)
    team_a_goals = Column(
        Integer,
        nullable=False,
    )
    team_b_name = Column(String, nullable=False)
    team_b_goals = Column(
        Integer,
        nullable=False,
    )


class Match(BaseModel):
    """pydantic representation"""

    model_config = ConfigDict(from_attributes=True)
    match_id: int

    team_a_name: str
    team_a_goals: int
    team_b_name: str
    team_b_goals: int


class RankingsORM(Base):
    """ORM sqlalchemy representation"""

    __tablename__ = "rankings"

    name = Column(String, primary_key=True, index=True)
    position = Column(Integer, nullable=False)
    points = Column(Integer, nullable=False)
    humanReadable = Column(String, nullable=False)


class Rankings(BaseModel):
    """pydantic representation"""

    model_config = ConfigDict(from_attributes=True)

    name: str
    position: int
    points: int
    humanReadable: str
