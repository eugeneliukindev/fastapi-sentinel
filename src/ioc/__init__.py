from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider

from src.ioc.db import DatabaseProvider
from src.ioc.services import ServicesProvider
from src.ioc.settings import SettingsProvider
from src.ioc.uow import UoWProvider

container = make_async_container(
    FastapiProvider(),
    SettingsProvider(),
    DatabaseProvider(),
    UoWProvider(),
    ServicesProvider(),
)
