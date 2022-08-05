import asyncio

from fastapi import FastAPI, Request

from celery.result import AsyncResult

from app.models import Stats, Period, Info
from app.rpc.consumer import consume
from app.auth.auth_middleware import AuthorizeMiddleware
from app.tasks import create_stats
from app.tasks import app as celery_app
from app.aws.dynamodb import get_stats_by_id, get_first_last_inootter_data_record


app = FastAPI()
app.add_middleware(AuthorizeMiddleware)


@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(consume(loop))


@app.post("/get_stats", response_model=Stats, response_model_exclude_unset=True)
async def get_stats(request: Request, period: Period):
    stats = await get_stats_by_id(request.state.user_id, str(period.start_date), str(period.end_date))
    if stats:
        return stats

    return Stats(description='no stats')


@app.get('/get_period', response_model=Period)
async def get_period(request: Request):
    period = Period(
        start_date=await get_first_last_inootter_data_record(id=request.state.user_id),
        end_date=await get_first_last_inootter_data_record(id=request.state.user_id, is_first=False)
    )
    return period


@app.post("/create_stats", response_model=Info, response_model_exclude_unset=True)
async def start_creating_stats(request: Request, period: Period):
    stats = await get_stats_by_id(request.state.user_id, str(period.start_date), str(period.end_date))
    if stats:
        return Info(message='requested stats already exist')

    task_id = await create_stats(request.state.user_id, str(period.start_date), str(period.end_date))

    return Info(message='your stats started creating', task_id=task_id)


@app.get("/get_stats_status", response_model=Info, response_model_exclude_unset=True)
async def get_stats_status(task_id: str):
    task_result = AsyncResult(f'{task_id}', app=celery_app)

    return Info(status=task_result.state)
