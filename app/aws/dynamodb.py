import aioboto3
import datetime
from boto3.dynamodb.conditions import Key

from app.config import settings


async def get_db_tables():
    session = aioboto3.Session()
    async with session.client("dynamodb", region_name=settings.AWS_DEFAULT_REGION,
                              endpoint_url=settings.LOCALSTACK_ENDPOINT_URL) as client:
        return await client.list_tables()


async def get_stats_by_id(id=None):
    session = aioboto3.Session()
    async with session.resource("dynamodb", region_name=settings.AWS_DEFAULT_REGION,
                              endpoint_url=settings.LOCALSTACK_ENDPOINT_URL) as dynamo_resource:
        table = await dynamo_resource.Table(settings.DB_NAME)
        result = await table.query(
            KeyConditionExpression=Key('id').eq(id)
        )

        return result


async def add_stats_to_db(id: int, data={}):
    session = aioboto3.Session()
    async with session.resource("dynamodb", region_name=settings.AWS_DEFAULT_REGION,
                                endpoint_url=settings.LOCALSTACK_ENDPOINT_URL) as dynamo_resource:
        table = await dynamo_resource.Table(settings.DB_NAME)

        result = await table.query(
            KeyConditionExpression=Key('id').eq(id)
        )

        result = result['Items']

        if result:
            await table.update_item(
                Key={"id": id},
                UpdateExpression="SET dates.#date = :data",
                ExpressionAttributeNames={"#date": f'{datetime.date.today()}'},
                ExpressionAttributeValues={":data": data},
            )
        else:
            await table.put_item(
                Item={'id': id, 'dates': {str(datetime.date.today()): data}},
            )
