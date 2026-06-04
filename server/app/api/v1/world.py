from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.infrastructure.database.models import CityModel, JobModel, WorldStateModel
from app.schemas.world import CityResponse, JobResponse, WorldStateResponse

router = APIRouter(prefix="/world", tags=["world"])


@router.get("/state", response_model=WorldStateResponse)
async def get_world_state(db: Session = Depends(get_db)):
    state = db.query(WorldStateModel).order_by(WorldStateModel.year.desc()).first()
    if not state:
        return WorldStateResponse(year=2000, era="信息时代", gdp_index=0.5, tech_level=5)
    return WorldStateResponse(
        year=state.year,
        era=state.era,
        gdp_index=state.gdp_index,
        tech_level=state.tech_level,
        major_events=state.major_events,
    )


@router.get("/cities", response_model=list[CityResponse])
async def get_cities(db: Session = Depends(get_db)):
    cities = db.query(CityModel).all()
    return [
        CityResponse(
            id=c.id, name=c.name, region=c.region,
            population=c.population, development_index=c.development_index,
            cost_of_living=c.cost_of_living,
        )
        for c in cities
    ]


@router.get("/jobs", response_model=list[JobResponse])
async def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(JobModel).all()
    return [
        JobResponse(
            id=j.id, name=j.name, category=j.category,
            min_intelligence=j.min_intelligence, min_charisma=j.min_charisma,
            salary_range=j.salary_range, stress_level=j.stress_level,
            health_impact=j.health_impact,
        )
        for j in jobs
    ]
