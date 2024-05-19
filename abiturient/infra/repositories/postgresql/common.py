from datetime import datetime
from itertools import product
from typing import (
    Any,
    TypeVar,
)

from sqlalchemy import (
    Case,
    case,
    delete,
    select,
    update,
)
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import bindparam

T = TypeVar('T')


class CommonRepo:

    def __init__(self, session: AsyncSession):
        self.session = session

    def latest_date(self, entity: T) -> Case[Any]:  # noqa
        return case(
            (entity.updated_at != None, entity.updated_at),  # noqa When condition and value
            else_=entity.created_at  # Default value if no when conditions are true
        )

    async def get(self, entity: T, where):
        query = (
            select(entity)
            .where(where)
        )
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def update(self, entity: T, where, **kwargs):
        query = (
            update(entity)
            .where(where)
            .values(
                updated_at=datetime.now(),
                **kwargs
            )
            .returning(entity)
        )
        result = await self.session.execute(query)
        return result.scalar()

    async def insert(self, instance: object):
        return self.session.add(instance)

    async def insert_many(self, instances: list[object]):
        return self.session.add_all(instances=instances)

    async def insert_without_errors(
        self, entity: T, instances: list[object],
    ):
        stmt = insert(entity).values(instances)

        do_nothing_stmt = stmt.on_conflict_do_nothing()
        await self.session.execute(do_nothing_stmt)

    async def delete(self, entity: T, where, soft: bool = False):
        if soft:
            return await self.update(entity, where, deleted_at=datetime.now())

        query = (
            delete(entity)
            .where(where)
        )
        result = await self.session.execute(query)
        return result.rowcount  # noqa

    async def bulk_create_or_update(
        self,
        entity: T,
        data: list[dict],
        d_key: str,
        upd_values: list,
        e_where,
        pop_data: list = (),
        extension_data: dict = None,
    ):
        """
        This function is designed to update or create objects in the database in
        a large number
        :param entity:
        :param extension_data:
        :param pop_data:
        :param data:
        :param d_key:
        :param upd_values:
        :param e_where:
        :return:
        """
        inserts, updates = [], []
        existing_data = await self.session.execute(select(entity).where(e_where))

        def expand_and_reduce(_data: dict) -> None:
            if existing_data: _data |= extension_data
            for _p in pop_data: _data.pop(_p, None)

        if existing_data := existing_data.scalars().all():
            for e, d in product(existing_data, data):
                expand_and_reduce(_data=d)

                if e.__dict__.get(d_key) == d.get(d_key):
                    d['_id'] = e.id
                    updates.append(d)
                    data.remove(d)
                    continue
        else:
            for d in data: expand_and_reduce(_data=d)
        inserts = data

        if updates:
            stmt = update(entity).where(entity.id == bindparam('_id')).values(
                {v: bindparam(v) for v in upd_values}
            )
            conn = await self.session.connection()
            await conn.execute(stmt, updates)
        if inserts:
            await self.insert_without_errors(entity=entity, instances=inserts)
