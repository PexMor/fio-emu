"""Configuration management for FIO emulator."""
import os
import pathlib
from typing import Optional

import tomli
import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Application configuration."""

    model_config = SettingsConfigDict(
        env_prefix="FIOEMU_",
        case_sensitive=False,
        extra="ignore",
    )

    # Server settings
    host: str = Field(default="127.0.0.1", description="Host to bind to")
    port: int = Field(default=8000, description="Port to bind to")

    # Config file paths
    config_dir: Optional[str] = Field(
        default=None, description="Config directory (defaults to ~/.config/fioemu)"
    )
    examples_dir: Optional[str] = Field(
        default=None, description="Examples directory (defaults to config_dir/examples)"
    )

    # API settings
    cors_origins: list[str] = Field(
        default_factory=lambda: ["*"], description="CORS allowed origins"
    )
    cors_allow_credentials: bool = Field(
        default=True, description="CORS allow credentials"
    )
    cors_allow_methods: list[str] = Field(
        default_factory=lambda: ["*"], description="CORS allowed methods"
    )
    cors_allow_headers: list[str] = Field(
        default_factory=lambda: ["*"], description="CORS allowed headers"
    )

    @property
    def config_directory(self) -> pathlib.Path:
        """Get the config directory path."""
        if self.config_dir:
            return pathlib.Path(self.config_dir)
        return pathlib.Path.home() / ".config" / "fioemu"

    @property
    def examples_directory(self) -> pathlib.Path:
        """Get the examples directory path."""
        if self.examples_dir:
            return pathlib.Path(self.examples_dir)
        return self.config_directory / "examples"

    @classmethod
    def load(cls, **kwargs) -> "Config":
        """Load configuration from files and environment."""
        config_dir = kwargs.get("config_dir")
        if not config_dir:
            config_dir = pathlib.Path.home() / ".config" / "fioemu"
        else:
            config_dir = pathlib.Path(config_dir)

        config_dir = pathlib.Path(config_dir)

        # Try to load from YAML first, then TOML
        config_data = {}
        yaml_config = config_dir / "config.yaml"
        toml_config = config_dir / "config.toml"

        if yaml_config.exists():
            with open(yaml_config, "r", encoding="utf-8") as f:
                config_data = yaml.safe_load(f) or {}

        elif toml_config.exists():
            with open(toml_config, "rb") as f:
                config_data = tomli.load(f) or {}

        # Merge config file data with kwargs
        merged_config = {**config_data, **kwargs}

        # Create config instance (environment variables are loaded automatically)
        return cls(**merged_config)

    def ensure_directories(self) -> None:
        """Ensure config and examples directories exist."""
        self.config_directory.mkdir(parents=True, exist_ok=True)
        self.examples_directory.mkdir(parents=True, exist_ok=True)

