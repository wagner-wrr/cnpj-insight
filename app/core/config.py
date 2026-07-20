
from datetime import timedelta, timezone
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação."""

    app_name: str = "CNPJ Insight"
    app_version: str = "0.1.0"

    api_url: str = "https://publica.cnpj.ws/cnpj"
     
    database_url: str = "sqlite:///./cnpj_insight.db"

    debug: bool = True

    TIMEZONE_OFFSET:int =-3 #Horas em relação ao UTC (-3 = Brasília)

    @property
    def tz(self) ->timezone:
        """Retorna o fuso horário configurado como objeto timezone"""
        return timezone(timedelta(hours=self.TIMEZONE_OFFSET))
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )


@lru_cache
def get_settings() -> Settings:
    """Retorna as configurações da aplicação."""
    return Settings()


settings = get_settings()