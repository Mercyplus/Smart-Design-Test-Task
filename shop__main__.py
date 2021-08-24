from aiohttp import web
from bson import json_util, objectid
from loguru import logger
from database_client import SingletonClient
import json

routes = web.RouteTableDef()


@routes.post('/api/create_item')
async def create_item(request: web.Request):
    parameters = await request.json()
    logger.info(parameters)
    if not parameters.get('title') and parameters.get('description'):
        return web.json_response({'Ошибка': 'Название или описание не указаны'}, status=422)

    db = SingletonClient.get_data_base()
    result = await db.items.insert_one(dict(parameters))
    if result:
        return web.json_response({'Статус': 'Выполнено'}, status=200)


@routes.post('/api/get_items')
async def get_items(request: web.Request):
    try:
        parameters = await request.json()
    except json.decoder.JSONDecodeError:
        parameters = {}
    logger.info(parameters)
    db = SingletonClient.get_data_base()
    cursor = db.items.find()

    if parameters.get('sort'):
        cursor = cursor.sort(parameters.get('sort'))

    items_list = await cursor.to_list(length=await db.items.count_documents({}))
    jsn = json_util.dumps({'items': items_list})

    return web.Response(text=jsn, headers={'Content-Type': 'application / json'}, status=200)


@routes.post('/api/get_item')
async def get_item(request: web.Request):
    parameters = await request.json()
    logger.info(parameters)

    db = SingletonClient.get_data_base()
    try:
        _id = parameters['_id']
        try:
            _id = objectid.ObjectId(_id)
        except TypeError:
            pass

        result = await db.items.find_one({'_id': _id})
        if not result:
            return web.json_response({'Ошибка': 'Предмет не найден'}, status=404)

        jsn = json_util.dumps({'item': result})
        return web.Response(text=jsn, headers={'Content-Type': 'application / json'}, status=200)
    except KeyError:
        return web.json_response({'Ошибка': '_id не указан'})


@routes.post('/api/get_items_titles')
async def get_items_titles(request: web.Request):
    try:
        parameters = await request.json()
    except json.decoder.JSONDecodeError:
        parameters = {}
    logger.info(parameters)

    db = SingletonClient.get_data_base()
    try:
        key = list(parameters.keys())[0]
        cursor = db.items.find({key: parameters.get(key)})
    except IndexError:
        cursor = db.items.find({})

    list_items = await cursor.to_list(length=await db.items.count_documents({}))
    logger.info(list_items)
    if not list_items:
        return web.json_response({'Ошибка': 'Предмет не найден'}, status=404)

    list_items = [item['title'] for item in list_items]

    jsn = json_util.dumps({'titles': list_items})
    return web.Response(text=jsn, headers={'Content-Type': 'application / json'}, status=200)


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app)