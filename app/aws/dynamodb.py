import aioboto3
import datetime
import boto3

from app.config import settings


async def get_db_tables():
    session = aioboto3.Session()
    async with session.client("dynamodb", region_name=settings.AWS_DEFAULT_REGION,
                              endpoint_url=settings.LOCALSTACK_ENDPOINT_URL) as client:
        return await client.list_tables()


async def get_first_last_inootter_data_record(id, is_first=True):
    session = aioboto3.Session()
    async with session.resource("dynamodb", region_name=settings.AWS_DEFAULT_REGION,
                                endpoint_url=settings.LOCALSTACK_ENDPOINT_URL) as dynamo_resource:
        table = await dynamo_resource.Table(settings.INNOTTER_STATS_TABLE)
        record = await table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('id').eq(id),
            ScanIndexForward=is_first,
            ProjectionExpression='#value',
            ExpressionAttributeNames={
                '#value': 'date'
            },
            Limit=1
        )
        if len(record['Items']):
            return record['Items'][0]['date']

        return None


async def get_innotter_data_by_id(id=None,
                                  start_date: str = str(datetime.date.today()),
                                  end_date: str = str(datetime.date.today())):
    session = aioboto3.Session()
    if not id:
        return None

    async with session.resource("dynamodb", region_name=settings.AWS_DEFAULT_REGION,
                                endpoint_url=settings.LOCALSTACK_ENDPOINT_URL) as dynamo_resource:
        table = await dynamo_resource.Table(settings.INNOTTER_STATS_TABLE)
        result = await table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('id').eq(id) &
                                   boto3.dynamodb.conditions.Key('date').between(start_date, end_date)
        )

        return result


async def get_stats_by_id(id=None, start_date: str = None, end_date: str = None):
    session = aioboto3.Session()

    if not id or not start_date or not end_date:
        return None

    async with session.resource("dynamodb", region_name=settings.AWS_DEFAULT_REGION,
                                endpoint_url=settings.LOCALSTACK_ENDPOINT_URL) as dynamo_resource:
        table = await dynamo_resource.Table(settings.STATS_TABLE)
        result = await table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('id').eq(id) &
                                   boto3.dynamodb.conditions.Key('period').eq(f'{start_date}/{end_date}')
        )
        if not len(result['Items']):
            return

        return result['Items'][0]['data']


async def add_innotter_data_to_db(id: int, data=None, date=str(datetime.date.today())):
    session = aioboto3.Session()
    async with session.resource("dynamodb", region_name=settings.AWS_DEFAULT_REGION,
                                endpoint_url=settings.LOCALSTACK_ENDPOINT_URL) as dynamo_resource:
        table = await dynamo_resource.Table(settings.INNOTTER_STATS_TABLE)
        if data:
            await table.put_item(
                Item={'id': id, 'date': date, 'data': data},
            )


def add_stats_to_db(id: int, data=None, start_date: str = None, end_date: str = None):
    session = boto3.Session()

    result = session.resource("dynamodb", region_name=settings.AWS_DEFAULT_REGION,
                              endpoint_url=settings.LOCALSTACK_ENDPOINT_URL)

    table = result.Table(settings.STATS_TABLE)
    if data:
        table.put_item(
            Item={'id': id, 'period': f'{start_date}/{end_date}', 'data': data},
        )
