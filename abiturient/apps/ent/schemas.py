from pydantic import BaseModel


class ParseENTSchema(BaseModel):
    start_page: int | None = 0
    end_page: int | None
    year: int | None
