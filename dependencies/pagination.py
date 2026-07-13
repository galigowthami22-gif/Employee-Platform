from fastapi import Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: int = 1
    size: int = 10

    class Config:
        from_attributes = True


def pagination_params(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100)):
    return {"page": page, "size": size}