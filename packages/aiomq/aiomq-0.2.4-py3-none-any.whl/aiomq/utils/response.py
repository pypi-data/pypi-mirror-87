from aiohttp import web
import json


class JsonStdDump(json.JSONEncoder):
    def iterencode(self, o, _one_shot=False):
        try:
            return super(JsonStdDump, self).iterencode(o, _one_shot=_one_shot)
        except TypeError:
            print(o)
            raise


class JsonResponse(web.Response):
    def __init__(self, data, *args, **kwargs):
        super().__init__(text=json.dumps({
            "msg": "处理成功",
            "code": "SUCCESS",
            "data": data
        }, cls=JsonStdDump), content_type='application/json', *args, **kwargs)


class CustomJsonResponse(web.Response):
    def __init__(self, data, *args, **kwargs):
        super().__init__(text=json.dumps(data, cls=JsonStdDump), content_type='application/json', *args, **kwargs)
