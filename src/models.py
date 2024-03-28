from datetime import datetime
from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, func


metadata = MetaData()

repos = Table(
    'repos',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('repo', String, nullable=False, unique=True),
    Column('owner', String, nullable=False),
    Column('stars', Integer, server_default=str(0), nullable=False),
    Column('position_cur', Integer, server_default=str(0), nullable=False),
    Column('position_prev', Integer, server_default=str(0), nullable=False),
    Column('watchers', Integer, server_default=str(0), nullable=False),
    Column('forks', Integer, server_default=str(0), nullable=False),
    Column('open_issues', Integer, server_default=str(0), nullable=False),
    Column('language', String, nullable=False, server_default='english'),
)

commits = Table(
    'commits',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('author', String, nullable=False),
    Column('date', DateTime(timezone=True), server_default=func.now()),
    Column('repo_id', Integer, ForeignKey('repos.id')),
)

