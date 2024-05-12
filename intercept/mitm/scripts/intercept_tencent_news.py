from mitmproxy import http
from orjson import loads

from handler import articles_handler, comments_handler

class TencentNewsInterceptor:

    async def response(self, flow: http.HTTPFlow):
        if flow.request.host == "r.inews.qq.com":
            match flow.request.path.split("?")[0]:

                case "/getSimpleNews":
                    json_data = loads(flow.response.content.decode("utf8"))
                    client_ip = flow.client_conn.peername[0]
                    await articles_handler(client_ip, json_data)

                case "/getQQNewsComment":
                    comments_data: list[dict] = loads(flow.response.content.decode("utf8"))["comments"]["new"]
                    if comments_data == []: return
                    client_ip = flow.client_conn.peername[0]
                    await comments_handler(client_ip, comments_data)
