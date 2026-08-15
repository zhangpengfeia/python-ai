from pydantic_settings import BaseSettings


class BaseSettingsWithEnv(BaseSettings):
    model_config = {"env_file": ".env", "extra": "ignore"}


class OpenAISettings(BaseSettingsWithEnv):
    api_key: str = ""
    base_url: str = ""
    default_model: str = ""

    model_config = {"env_prefix": "OPENAI_"}

    print(model_config)


class AnthropicSettings(BaseSettingsWithEnv):
    api_key: str = "1111"
    base_url: str = "222"
    default_model: str = "333"

    model_config = {"env_prefix": "ANTHROPIC_"}
    print(model_config)


class TavilySettings(BaseSettingsWithEnv):
    api_key: str = ""
    model_config = {"env_prefix": "TAVILY_"}


openai_settings = OpenAISettings()
anthropic_settings = AnthropicSettings()
tavily_settings = TavilySettings()
