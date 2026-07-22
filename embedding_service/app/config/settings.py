from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings) :
    jina_api_key: str
    jina_base_url: str
    jina_model: str

    qdrant_host: str
    qdrant_port: int
    qdrant_collection: str
    
    embedding_dimension: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings = Settings()