from dishka import Provider, Scope, provide

from src.config import Settings, settings


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return settings
