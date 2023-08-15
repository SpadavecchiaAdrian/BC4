from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import Generator
from .database import SessionLocal, engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# DB Dependency
def get_db() -> Generator:
    """
    DB Session generator, allow dependency injection in each endpoint.
    The session is enable for the endpoint execution, it auto close session
    after execution.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def pointsFromMatch(team_a_goals: int, team_b_goals: int) -> [int, int]:
    """
    This function take the goals from team a and team b, and return a list
    with the points for each team.

    Args:
        team_a_goals (int): The amount of goals in the mach from team a
        team_b_goals (int): The amount of goals in the mach from team b
    Returns:
        list(team_a_points, team_b_points)
    """
    if team_a_goals == team_b_goals:
        return [1, 1]
    elif team_a_goals > team_b_goals:
        return [3, 0]
    else:
        return [0, 3]


def humanReadable(name: str, position: int, points: int) -> str:
    """
    This function take the name of the team, the table position and their
    points and return a readable format

    Args:
        name (str): The name of the team
        position (int): The position of the team in the ranking table
        points (int): the amount of points of the team
    Returns:
        str: human readable string
    """
    if points == 1:
        return f"{position}. {name}, {points} pt"
    else:
        return f"{position}. {name}, {points} pts"


def add_matchs(db: Session):
    db.add(
        models.MatchORM(
            team_a_name="Racing",
            team_a_goals=3,
            team_b_name="Independiente",
            team_b_goals=3,
        )
    )
    db.add(
        models.MatchORM(
            team_a_name="Vélez",
            team_a_goals=1,
            team_b_name="Argentinos Juniors",
            team_b_goals=0,
        )
    )
    db.add(
        models.MatchORM(
            team_a_name="Racing",
            team_a_goals=1,
            team_b_name="Argentinos Juniors",
            team_b_goals=1,
        )
    )
    db.add(
        models.MatchORM(
            team_a_name="Vélez",
            team_a_goals=3,
            team_b_name="Independiente",
            team_b_goals=1,
        )
    )
    db.add(
        models.MatchORM(
            team_a_name="Racing",
            team_a_goals=4,
            team_b_name="Ferro",
            team_b_goals=0,
        )
    )
    db.commit()


@app.get(
    "/ranking",
    tags=["Soccer Ranking"],
    summary="obtain the ranking table position",
)
async def getRanking(db: Session = Depends(get_db)) -> list[models.Rankings]:
    """
    This endpoint calculate and return the ranking of teams in
    a soccer league
    """
    # add_matchs(db)
    # get matches data from DB
    matchs = db.query(models.MatchORM).all()

    # estimate the points for each team
    points = {}
    for game in matchs:
        pointsTeamA, pointsTeamB = pointsFromMatch(
            team_a_goals=game.team_a_goals, team_b_goals=game.team_b_goals
        )
        if game.team_a_name in points:
            points[game.team_a_name] += pointsTeamA
        else:
            points[game.team_a_name] = pointsTeamA

        if game.team_b_name in points:
            points[game.team_b_name] += pointsTeamB
        else:
            points[game.team_b_name] = pointsTeamB

    # trasform point dict to a list of dict in order to be able to sort it
    points = [
        {"name": team, "points": point} for team, point in points.items()
    ]

    # now sort the result by points and name
    points = sorted(
        points, key=lambda points: (-points["points"], points["name"])
    )
    # finally build ranking list with 1224 logic
    ranking = [
        models.Rankings(
            name=points[0]["name"],
            position=1,
            points=points[0]["points"],
            humanReadable=humanReadable(
                points[0]["name"], 1, points[0]["points"]
            ),
        ),
    ]
    for key in range(1, len(points)):
        position = key + 1
        if points[key]["points"] == points[key - 1]["points"]:
            position = ranking[key - 1].position
        ranking.append(
            models.Rankings(
                name=points[key]["name"],
                position=position,
                points=points[key]["points"],
                humanReadable=humanReadable(
                    points[key]["name"], position, points[key]["points"]
                ),
            )
        )
    # delete old ranking
    db.query(models.RankingsORM).delete()
    # save the new ranking list
    for team in ranking:
        db.add(models.RankingsORM(**team.model_dump()))
    db.commit()
    # end returning the ranking list
    return ranking
