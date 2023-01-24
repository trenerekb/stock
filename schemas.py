import datetime

from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class ValidIdSchema(BaseModel):
    id: UUID


class ArtSchema(BaseModel):
    id: Optional[UUID]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    name: str
    full_name: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode = True


class CategorySchema(BaseModel):
    id: Optional[UUID]
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True


class GroupSchema(BaseModel):
    id: Optional[UUID]
    name: str
    category_id: Optional[UUID]
    description: Optional[str]

    class Config:
        orm_mode = True


class SpecificationSchema(BaseModel):
    id: Optional[UUID]
    name: str
    type: str
    group_id: Optional[UUID]
    default_value: Optional[dict]
    is_required: bool
    order_number: int

    class Config:
        orm_mode = True


class ArtSpecSchema(BaseModel):
    id: Optional[UUID]
    article_id: Optional[UUID]
    specification_id: Optional[UUID]
    value: Optional[dict]

    class Config:
        orm_mode = True


class CatArtSchema(BaseModel):
    id: Optional[UUID]
    article_id: Optional[UUID]
    specification_id: Optional[UUID]
    value: Optional[dict]

    class Config:
        orm_mode = True
