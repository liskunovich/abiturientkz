from pydantic import (
    BaseModel,
    Field,
    model_validator
)


class BasicPagination(BaseModel):
    limit: int | None = None
    offset: int | None = Field(alias='page')

    @classmethod
    def calculate_the_page(  # noqa
        cls, limit: int | None, offset: int | None
    ) -> int | None:
        if limit and offset:
            return limit * offset

    @model_validator(mode='before')
    def validate_paginate(cls, values):  # noqa
        limit = values.get('limit', None)
        offset = cls.calculate_the_page(
            limit=limit, offset=values.get('page', None),
        )
        values['page'] = offset
        return values

    @classmethod
    def convert_string_to_list(cls, value):
        if value:
            value = list(map(lambda x: x.strip(), value.split(',')))
        return value
