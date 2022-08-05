from app.aws.dynamodb import get_innotter_data_by_id
from app.services import calculate_stats
from app.worker import app


async def create_stats(id, start_date: str, end_date: str) -> None:
    data = await get_innotter_data_by_id(id=id,
                                         start_date=start_date,
                                         end_date=end_date)

    task = build_stats.delay(id=id, data=data, start_date=start_date, end_date=end_date)
    return task.id


@app.task
def build_stats(id: int, data, start_date: str, end_date: str) -> None:
    if not data['Items']:
        return

    calculate_stats(id, data, start_date, end_date)


app.register_task(build_stats)
