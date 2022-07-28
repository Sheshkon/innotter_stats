import asyncio

from fastapi import FastAPI, Request

from app.aws.dynamodb import get_stats_by_id
from app.rpc.consumer import consume
from app.auth.auth_middleware import AuthorizeMiddleware


app = FastAPI()
app.add_middleware(AuthorizeMiddleware)


@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(consume(loop))


@app.get("/")
async def root():
    return {'Innoter stats'}


@app.get("/stats")
async def root(request: Request):
    return {"Innotter stats": await get_stats_by_id(request.state.user_id)}
