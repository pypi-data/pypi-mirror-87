"""Collection of schemas."""
from typing import List, Optional

from pydantic import BaseModel, Field


class ADFHExtraType(BaseModel):
    """Schema for ADFH extra."""

    type: str
    name: str
    value: str
    tags: Optional[List[str]]


class ADFHFieldsType(BaseModel):
    """Schema for ADFH fields."""

    id: str
    name: str
    type: str
    mandatory: str = "no"
    options: Optional[List[str]]
    text: Optional[str]


class ADFHModelsPropertiesType(BaseModel):
    """Schema for ADFH models properties."""

    model: str
    assign: str


class ADFHModelsType(BaseModel):
    """Schema for ADFH models."""

    id: str
    name: str
    properties: List[ADFHModelsPropertiesType]
    text: Optional[str]


class ADFHActionsInputType(BaseModel):
    """Schema for ADFH action input."""

    action: str
    assign: str


class ADFHActionsType(BaseModel):
    """Schema for ADFH action."""

    id: str
    name: str
    type: str
    model: str
    input: Optional[List[ADFHActionsInputType]]
    subject: Optional[str]
    text: Optional[str]
    tags: Optional[List[str]]


class ADFHType(BaseModel):
    """Schema for ADFH."""

    version: str
    extra: Optional[List[ADFHExtraType]]
    fields_list: List[ADFHFieldsType] = Field(..., alias="fields")
    models: List[ADFHModelsType]
    actions: Optional[List[ADFHActionsType]]


class IhsanType(BaseModel):
    """Schema for Ihsan."""

    adfh: ADFHType
