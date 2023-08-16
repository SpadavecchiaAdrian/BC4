from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database import Base
from app import models
from app.main import pointsFromMatch, humanReadable, app, get_db

# ---- simple unit test ----


def test_pointsFromMatch():
    # Test a tie
    result = pointsFromMatch(4, 4)
    assert result == [1, 1]

    # Test team TeamPositiona win
    result = pointsFromMatch(4, 1)
    assert result == [3, 0]

    # Test team b win
    result = pointsFromMatch(3, 4)
    assert result == [0, 3]


def test_humanReadable():
    # test the human readable text generation with sing and plu 'pt' and 'pts'
    assert (
        humanReadable(name="A Team", position=1, points=0)
        == "1. A Team, 0 pts"
    )
    assert (
        humanReadable(name="A Team", position=1, points=1) == "1. A Team, 1 pt"
    )
    assert (
        humanReadable(name="A Team", position=1, points=6)
        == "1. A Team, 6 pts"
    )


# ---- This correspond to End-to-End testing example ----
# ---- we need to setup a db for the test ----


# start a db for testing endpoints
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# create tables from models
Base.metadata.create_all(bind=engine)


# override db dependency for test db
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# start the app in test mode
client = TestClient(app)


# ---- Now we can test endpoints ----


def test_get_ranking_endpoint():
    db = TestingSessionLocal()
    # Clean old matchs
    db.query(models.MatchORM).delete()
    # add new matchs
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

    response = client.get("/ranking")
    assert response.status_code == 200
    expectedData = [
        {
            "name": "Vélez",
            "position": 1,
            "points": 6,
            "humanReadable": "1. Vélez, 6 pts",
        },
        {
            "name": "Racing",
            "position": 2,
            "points": 5,
            "humanReadable": "2. Racing, 5 pts",
        },
        {
            "name": "Argentinos Juniors",
            "position": 3,
            "points": 1,
            "humanReadable": "3. Argentinos Juniors, 1 pt",
        },
        {
            "name": "Independiente",
            "position": 3,
            "points": 1,
            "humanReadable": "3. Independiente, 1 pt",
        },
        {
            "name": "Ferro",
            "position": 5,
            "points": 0,
            "humanReadable": "5. Ferro, 0 pts",
        },
    ]
    assert response.json() == expectedData
