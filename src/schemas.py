from datetime import date
from pydantic import BaseModel


# схема для хранения параметров запроса
class ActivityGet(BaseModel):
    owner: str
    repo: str
    since: date
    until: date
