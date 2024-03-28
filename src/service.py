import datetime
from numpy.random import randint
from typing import Annotated
from fastapi import Depends
from fastapi.responses import JSONResponse
from schemas import ActivityGet
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from database import get_async_session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

mes = {'mes': 'some error'}


# реализована пагинация для get-методов
def pagination(limit: int = 100, offset: int = 0):
    return {'limit': limit, 'offset': offset}


# через Depends подтягиваются все необходимые параметры
async def get_activity(activity_info: Annotated[ActivityGet, Depends()], pagination_params: dict = Depends(pagination),
                       session: AsyncSession = Depends(get_async_session)):
    try:
        # формируется sql запрос
        activity = await session.execute(text(f"select * from commits where date between '{activity_info.since}' and "
                                              f"'{activity_info.until + datetime.timedelta(days=1)}' and "
                                              f"repo_id in (select id from repos where repo='{activity_info.repo}') "
                                              f"limit {pagination_params['limit']} "
                                              f"offset {pagination_params['offset']}"))
        activity = activity.mappings().all()
        return {'commits': len(activity), 'activity': activity}
    except SQLAlchemyError:
        return JSONResponse(content=mes, status_code=400)


# order может содержать сразу несколько полей сортировки
# общий вид order col1~desc_col2~asc
async def get_repos(order: str = 'stars~desc', pagination_params: dict = Depends(pagination),
                    session: AsyncSession = Depends(get_async_session)):
    # формируется порядок сортировки
    order = ','.join((order.replace('~', ' ')).split('-'))
    try:
        repos = await session.execute(text(f"select * from repos order by {order} limit {pagination_params['limit']} "
                                           f"offset {pagination_params['offset']}"))
        return repos.mappings().all()
    except SQLAlchemyError:
        return JSONResponse(content=mes, status_code=400)


# заполнение бд тестовыми данными
async def fill_db(session: AsyncSession = Depends(get_async_session)):
    for i in range(200):
        try:
            await session.execute(text(f"insert into repos(repo, owner, stars, watchers, forks, open_issues) "
                                       f"values('repo{i}', 'owner{i}', {randint(1000)}, {randint(10)},"
                                       f"{randint(10)}, {randint(10)})"))
            await session.execute(
                text(f"insert into commits( author, repo_id) values('Bob{i + randint(10)}', {i + 1})"))
            await session.execute(
                text(f"insert into commits( author, repo_id) values('Mark{i + randint(10)}', {i + 1})"))
        except IntegrityError:
            await session.rollback()
            return JSONResponse(content={'mes': 'IntegrityError'}, status_code=400)
    try:
        await session.commit()
        return {'mes': 'DB was filled by test data'}
    except SQLAlchemyError:
        await session.rollback()
        return JSONResponse(content=mes, status_code=400)
