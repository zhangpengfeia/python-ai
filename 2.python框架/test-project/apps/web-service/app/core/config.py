from pydantic_settings import BaseSettings


class BaseSettingsWithEnv(BaseSettings):
    model_config = {"env_file": ".env", "extra": "ignore"}


class CommonSettings(BaseSettingsWithEnv):
    environment: str = "development"


class WebSettings(BaseSettingsWithEnv):
    app_name: str = "Web Service API"  # 实际读取 WEB_APP_NAME
    cors_origins: str = ""  # 实际读取 WEB_CORS_ORIGINS，多个来源用逗号分隔
    cors_expose_headers: str = ""  # 实际读取 WEB_CORS_EXPOSE_HEADERS
    jwt_secret_key: str = ""

    model_config = {"env_prefix": "WEB_"}


class DBSettings(BaseSettingsWithEnv):
    host: str = "152.136.228.231"
    port: str = "5432"
    name: str = "duyi_db"
    user: str = "admin"
    password: str = "admin"

    model_config = {"env_prefix": "DB_"}


class LogSettings(BaseSettingsWithEnv):
    level: str = "INFO"  # DEBUG / INFO / WARNING / ERROR
    slow_query_threshold: float = 200  # 毫秒

    model_config = {"env_prefix": "LOG_"}


common_settings = CommonSettings()
web_settings = WebSettings()
db_settings = DBSettings()
log_settings = LogSettings()
