from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider

from ioc.db import DatabaseProvider
from ioc.services import ServicesProvider
from ioc.settings import SettingsProvider
from ioc.uow import UoWProvider

container = make_async_container(
    FastapiProvider(),
    SettingsProvider(),
    DatabaseProvider(),
    UoWProvider(),
    ServicesProvider(),
)
