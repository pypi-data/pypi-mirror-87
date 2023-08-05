from DobotRPC import RPCClient
import asyncio
from typing import List, Any

IP = '127.0.0.1'
PORT = '10001'


class RPCAdapter(object):
    def __init__(self, ip, port):
        self.__rpc_client = RPCClient(ip, port)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__rpc_client.wait_for_connected())

    def __getattr__(self, func_name: str) -> Any:
        def send_wrapper(**params) -> Any:
            method = func_name
            fut = self.__rpc_client.send(method, params)
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(fut)

        return send_wrapper


class Pyimageom(object):
    def __init__(self):
        self._r_client = RPCAdapter(ip=IP, port=PORT)

    def image_cut(self, img_base64: str):
        return self._r_client.image_cut(img_base64=img_base64)

    def feature_image_classify(self, img_base64s: List[Any], lables: List[int],
                               class_num: int, flag: int):
        return self._r_client.feature_image_classify(img_base64s=img_base64s,
                                                     lables=lables,
                                                     class_num=class_num,
                                                     flag=flag)

    def feature_image_group(self, img_base64: str):
        return self._r_client.feature_image_group(img_base64=img_base64)

    def find_chessboard_corners(self, img_base64: str):
        return self._r_client.find_chessboard_corners(img_base64=img_base64)

    def color_image_cut(self, img_base64: str):
        return self._r_client.color_image_cut(img_base64=img_base64)

    def color_image_classify(self, img_base64s: List[Any], lables: List[int],
                             class_num: int, flag: int):
        return self._r_client.color_image_classify(img_base64s=img_base64s,
                                                   lables=lables,
                                                   class_num=class_num,
                                                   flag=flag)

    def color_image_group(self, img_base64: str):
        return self._r_client.color_image_group(img_base64=img_base64)

    def set_background(self, img_base64: str):
        return self._r_client.set_background(img_base64=img_base64)
