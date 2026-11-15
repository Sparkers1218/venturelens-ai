from __future__ import annotations

from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ProjectInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=2, max_length=120)
    problem_statement: str = Field(default="", max_length=4000)
    proposed_solution: str = Field(default="", max_length=4000)
    target_customers: str = Field(default="", max_length=2000)
    industry: str = Field(default="", max_length=120)
    geography: str = Field(default="", max_length=160)
    business_model: str = Field(default="", max_length=2000)


class CompetitorInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=160)
    description: str = Field(default="", max_length=2000)
    source_url: str = Field(default="", max_length=2048)
    target_audience: str = Field(default="", max_length=1000)
    pricing: str = Field(default="", max_length=1000)
    differentiation_notes: str = Field(default="", max_length=2000)

    @field_validator("source_url")
    @classmethod
    def validate_source_url(cls, value: str) -> str:
        if value:
            parsed = urlparse(value)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                raise ValueError("Source URL must be an absolute http or https URL.")
        return value


class ResearchSourceInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=200)
    publisher: str = Field(default="", max_length=200)
    source_url: str = Field(default="", max_length=2048)
    summary: str = Field(default="", max_length=4000)

    @field_validator("source_url")
    @classmethod
    def validate_source_url(cls, value: str) -> str:
        if value:
            parsed = urlparse(value)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                raise ValueError("Source URL must be an absolute http or https URL.")
        return value

    @model_validator(mode="after")
    def require_source_details(self) -> ResearchSourceInput:
        if not self.source_url and not self.summary:
            raise ValueError("Enter a source URL or a research note.")
        return self
