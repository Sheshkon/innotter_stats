from pydantic import BaseModel, validator
import datetime


class Period(BaseModel):
    start_date: datetime.date = datetime.date.today()
    end_date: datetime.date = datetime.date.today()

    @validator('end_date')
    def check_dates(cls, value, values, **kwargs):
        start_date = values['start_date']
        if value > datetime.date.today():
            raise ValueError('Invalid date: end_date after today.')

        if value < start_date:
            raise ValueError('Invalid date: start_date after end_date.')

        return value


class Stats(BaseModel):
    id: int = None
    username: str = None
    likes_amount: int = None
    likes_growth: int = None
    posts_amount: int = None
    posts_growth: int = None
    pages_likes_amount: int = None
    pages_likes_growth: int = None
    pages_amount: int = None
    followers_amount: int = None
    followers_growth: int = None
    start_date: str = None
    end_date: str = None
    description: str = None


class Info(BaseModel):
    message: str = None
    task_id: str = None
    status: str = None
