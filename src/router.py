from typing import Mapping
from fastapi import APIRouter, Depends
from service import get_activity, get_repos, fill_db


router = APIRouter(prefix='/repos', tags=['Repos'])


# через Depends подтягиваются все необходимые параметры
@router.get('/top100')
async def get_repos(repos: Mapping = Depends(get_repos)):
    return repos


@router.get('/{owner}/{repo}/activity')
async def get_activity(activity: Mapping = Depends(get_activity)):
    return activity


@router.post('/fill_db')
async def fill_db(mes: dict = Depends(fill_db)):
    return mes

