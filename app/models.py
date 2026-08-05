from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator

AgentProvider = Literal["claude", "codex", "gemini", "custom"]
TransportProvider = Literal["telegram"]


class TelegramSettings(BaseModel):
    enabled: bool = True
    bot_token: str = ""
    allowed_user_ids: list[int] = Field(default_factory=list)

    @field_validator("bot_token")
    @classmethod
    def validate_token_shape(cls, value: str) -> str:
        value = value.strip()
        if not value:
            return value
        parts = value.split(":", 1)
        if len(parts) != 2 or not parts[0].isdigit() or len(parts[1]) < 20:
            raise ValueError(
                "Telegram bot token must look like '123456789:AA...'. Copy it from @BotFather."
            )
        return value

    @field_validator("allowed_user_ids")
    @classmethod
    def validate_user_ids(cls, values: list[int]) -> list[int]:
        unique: list[int] = []
        for item in values:
            if item <= 0:
                raise ValueError("Telegram user IDs must be positive integers.")
            if item not in unique:
                unique.append(item)
        return unique


class CustomAgentSettings(BaseModel):
    executable: str = ""
    new_session_args: list[str] = Field(default_factory=lambda: ["{prompt}"])
    resume_session_args: list[str] = Field(
        default_factory=lambda: ["--resume", "{session_id}", "{prompt}"]
    )
    version_args: list[str] = Field(default_factory=lambda: ["--version"])
    output_format: Literal["text", "json", "jsonl"] = "text"
    response_json_path: str = ""
    session_id_json_path: str = ""
    environment: dict[str, str] = Field(default_factory=dict)

    @field_validator("executable")
    @classmethod
    def strip_executable(cls, value: str) -> str:
        return value.strip()

    @model_validator(mode="after")
    def require_prompt_placeholder(self) -> "CustomAgentSettings":
        joined = " ".join(self.new_session_args)
        if "{prompt}" not in joined:
            raise ValueError("Custom new-session arguments must contain {prompt}.")
        return self


class AgentSettings(BaseModel):
    provider: AgentProvider = "claude"
    display_name: str = "Claude Code"
    executable: str = ""
    model: str = ""
    default_mode: str = "acceptEdits"
    max_turns: int = Field(default=0, ge=0, le=500)
    max_budget_usd: float = Field(default=0, ge=0, le=10000)
    extra_environment: dict[str, str] = Field(default_factory=dict)
    custom: CustomAgentSettings = Field(default_factory=CustomAgentSettings)
    is_default: bool = False

    @field_validator("display_name")
    @classmethod
    def validate_display_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Agent display name cannot be empty.")
        if len(value) > 60:
            raise ValueError("Agent display name must be 60 characters or fewer.")
        return value


class AppSettings(BaseModel):
    configured: bool = False
    projects_root: str = ""
    transport: TransportProvider = "telegram"
    telegram: TelegramSettings = Field(default_factory=TelegramSettings)
    agents: list[AgentSettings] = Field(default_factory=list)
    folder_page_size: int = Field(default=8, ge=4, le=20)
    session_page_size: int = Field(default=8, ge=4, le=20)
    history_page_size: int = Field(default=6, ge=2, le=20)


class PublicSettings(BaseModel):
    configured: bool
    projects_root: str
    transport: TransportProvider
    telegram_enabled: bool
    bot_token_masked: str
    allowed_user_ids: list[int]
    agents: list[AgentSettings]
    folder_page_size: int
    session_page_size: int
    history_page_size: int


class SettingsPayload(BaseModel):
    projects_root: str
    transport: TransportProvider = "telegram"
    telegram_enabled: bool = True
    bot_token: str = ""
    keep_existing_bot_token: bool = False
    allowed_user_ids: list[int]
    agents: list[AgentSettings]
    folder_page_size: int = Field(default=8, ge=4, le=20)
    session_page_size: int = Field(default=8, ge=4, le=20)
    history_page_size: int = Field(default=6, ge=2, le=20)
