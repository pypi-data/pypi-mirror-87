import json
from collections import OrderedDict

from aiohttp import web
import asyncpg
from marshmallow import EXCLUDE

from .schemas import ibeacon_post_schema, macbeacon_post_schema, tag_patch_schema
from .views import ValidatingView, paginate_query


def tag_schema_dump(row):
    if row['type'] == 'iBeacon':
        return ibeacon_post_schema.dump(row)
    return macbeacon_post_schema.dump(row)


class TagsView(ValidatingView):
    async def get(self):
        async with self.request.app['db_pool'].acquire() as conn:
            query = None
            if 'type' in self.request.query:
                query = ('SELECT * from tags WHERE type = $1',
                         self.request.query['type'])
            elif 'group_id' in self.request.query:
                try:
                    query = ('SELECT * from tags WHERE group_id = $1',
                             int(self.request.query['group_id']))
                except ValueError:
                    raise web.HTTPBadRequest(text='bad group_id')
            else:
                query = ('SELECT * from tags', )
            query = paginate_query(self.request, query)
            try:
                tags = await conn.fetch(*query)
            except asyncpg.exceptions.InvalidTextRepresentationError:
                raise web.HTTPBadRequest(text='Invalid tag type')
            return web.json_response([tag_schema_dump(r) for r in tags if r is not None])

    async def post(self):
        body = await self._valid_json(self.request)

        if 'type' not in body:
            raise web.HTTPBadRequest(reason='Type field is required for post')

        new_t = {}
        if body['type'] in {'iBeacon', 'LocationAnchor'}:
            new_t.update(self._validate(ibeacon_post_schema, body))
        elif body['type'] == 'SmartRelay':
            new_t.update(self._validate(macbeacon_post_schema, body))
        else:
            raise web.HTTPBadRequest(reason=f'Unknown tag type {body["type"]}')

        async with self.request.app['db_pool'].acquire() as conn:
            try:
                await conn.execute('INSERT INTO tags (mac, uuid, major, minor, type, zone_id, name, group_id, attrs) VALUES '
                                   '($1, $2, $3, $4, $5, $6, $7, $8, $9)',
                                   new_t.get('mac', None),
                                   new_t.get('uuid', None),
                                   new_t.get('major', None),
                                   new_t.get('minor', None),
                                   new_t['type'],
                                   new_t.get('zone_id', None),
                                   new_t.get('name', None),
                                   new_t.get('group_id', None),
                                   json.dumps(new_t.get('attrs', {})))
            except asyncpg.exceptions.UniqueViolationError as e:
                raise web.HTTPConflict(reason=str(e.detail))
            except (asyncpg.exceptions.InvalidTextRepresentationError,
                    asyncpg.exceptions.NotNullViolationError,
                    asyncpg.exceptions.ForeignKeyViolationError) as e:
                raise web.HTTPBadRequest(reason=str(e.detail))
        raise web.HTTPCreated


class TagView(ValidatingView):
    async def get(self):
        t_id = int(self.request.match_info['id'])
        async with self.request.app['db_pool'].acquire() as conn:
            l = await conn.fetchrow('SELECT * FROM tags t WHERE id = $1', t_id)
            if not l:
                raise web.HTTPNotFound
            return web.json_response(tag_schema_dump(l))

    async def patch(self):
        t_id = int(self.request.match_info['id'])
        async with self.request.app['db_pool'].acquire() as conn:
            row = await conn.fetchrow('SELECT * FROM tags t WHERE id = $1', t_id)
            if not row:
                raise web.HTTPNotFound
            tag = dict(row.items())
            body = await self._valid_json(self.request)
            updates = self._validate(tag_patch_schema, body)
            if 'type' in updates:
                del body['type']  # Ensure that we are validating against existing type
            tag.update(updates)
            if tag['type'] in {'iBeacon', 'LocationAnchor'}:
                self._validate(ibeacon_post_schema, tag, unknown=EXCLUDE)
            else:
                self._validate(macbeacon_post_schema, tag, unknown=EXCLUDE)
            await conn.execute('UPDATE tags SET name = $1, mac = $2, uuid = $3, major = $4, '
                               'minor = $5, attrs = $6, zone_id = $7, group_id = $8  WHERE id = $9',
                               tag['name'], tag['mac'], tag['uuid'], tag['major'], tag['minor'],
                               json.dumps(tag['attrs']), tag['zone_id'], tag['group_id'], t_id)
        raise web.HTTPNoContent

    async def delete(self):
        t_id = int(self.request.match_info['id'])
        async with self.request.app['db_pool'].acquire() as conn:
            await conn.execute('DELETE from tags where id = $1', t_id)
        raise web.HTTPNoContent
