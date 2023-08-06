# -*- coding: utf-8 -*-

from __future__ import print_function

import grpc
from . import audio_streaming_pb2
from . import audio_streaming_pb2_grpc
from . import header_manipulator_client_interceptor
import base64
import os
import logging
import datetime
import time
import jwt


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class AsrClient(object):
    """ version modify log,
    from version 1.0.7: change init method, move product_id and enable_flush_data to be must params;
    """

    request = audio_streaming_pb2.InitRequest()

    def __init__(self, server_ip, port, product, enable_flush_data,
                 enable_chunk=True,
                 enable_long_speech=True,
                 sample_point_bytes=2,
                 send_per_seconds=0.16,
                 sleep_ratio=1,
                 app_name='python',
                 log_level=4,
                 service_name="",
                 app_key="",
                 app_secret="",
                 extra_info="",
                 product_id="",
                 sample_rate=0):
        # asr流式服务器的地址，私有化版本请咨询供应商
        self.server_ip = server_ip
        # asr流式服务的端口，私有化版本请咨询供应商
        self.port = port
        self.host = server_ip + ":" + port
        self.request.enable_chunk = enable_chunk
        # 是否允许长音频
        self.request.enable_long_speech = enable_long_speech
        # 是否返回中间翻译结果
        self.request.enable_flush_data = enable_flush_data
        # 服务名称
        self.service_name = service_name
        # app key
        self.app_key = app_key
        # app_secret
        self.app_secret = app_secret
        if product is not None:
            # 兼容使用product的老版本
            self.request.product_id = product.value[1]
            # 每次发送的音频字节数
            self.send_package_size = int(send_per_seconds * product.value[2] * sample_point_bytes)
        elif product_id == "" or sample_rate == 0:
            raise RuntimeError('product id and sample rate must be set in AsrClient')
        elif sample_rate != 8000 and sample_rate != 16000:
            raise RuntimeError('sample rate must be 8000 or 16000')
        else:
            self.request.product_id = product_id
            self.send_package_size = int(send_per_seconds * sample_rate * sample_point_bytes)
        self.request.sample_point_bytes = sample_point_bytes
        # 指定每次发送的音频数据包大小，通常不需要修改
        self.request.send_per_seconds = send_per_seconds
        self.request.sleep_ratio = sleep_ratio
        # asr客户端的名称，为便于后端查错，请设置一个易于辨识的appName
        self.request.app_name = app_name
        # 服务端的日志输出级别
        self.request.log_level = log_level
        self.request.extra_info = extra_info

    def generate_file_stream(self, file_path):
        """
        从音频文件中读取流
        :param file_path: 音频文件路径
        :return: 文件流的迭代
        """
        if not os.path.exists(file_path):
            logging.info("%s file is not exist, please check it!", file_path)
            os._exit(-1)
        file = open(file_path, "rb")
        content = file.read(self.send_package_size)
        while len(content) > 0:
            yield audio_streaming_pb2.AudioFragmentRequest(audio_data=content)
            content = file.read(self.send_package_size)
            # 客户端限流，防止发送过快，0.01为经验值
            time.sleep(0.01)
        file.close()

    def generate_stream_request(self, file_stream):
        """
        通过音频流产生request对象
        :param file_stream: 字节流
        :return: request对象
        """
        return audio_streaming_pb2.AudioFragmentRequest(audio_data=file_stream)

    def get_result(self, file_path):
        """
        通过文件路径获取最终解码结果的迭代器
        :param file_path:
        :return: response的迭代
        """

        header_audio_meta = header_manipulator_client_interceptor.header_adder_interceptor(
            'audio_meta', base64.b64encode(self.request.SerializeToString()))
        header_service_name = header_manipulator_client_interceptor.header_adder_interceptor(
            'service-name', self.service_name)
        payload = {
            "ak": self.app_key,
            "exp": datetime.datetime.now()+datetime.timedelta(minutes=30)
        }

        token = jwt.encode(payload, self.app_secret, algorithm="HS256")

        header_authorization = header_manipulator_client_interceptor.header_adder_interceptor(
            'authorization', token)

        # 添加ca认证
        # with open(
        #         '/path/of/xxx.crt',
        #         'rb') as f:
        #     creds = grpc.ssl_channel_credentials(f.read())
        # with grpc.secure_channel(self.host, creds) as channel:

        with grpc.insecure_channel(target=self.host, options=[('grpc.keepalive_timeout_ms', 1000000), ]) as channel:
            intercept_channel = grpc.intercept_channel(channel,
                                                       header_audio_meta,
                                                       header_service_name,
                                                       header_authorization)
            stub = audio_streaming_pb2_grpc.AsrServiceStub(intercept_channel)
            responses = stub.send(self.generate_file_stream(file_path), timeout=100000)
            for response in responses:
                yield response

            for key, value in responses.trailing_metadata():
                print('Response metadata data : key:%s, value:%s' % (key, value))


    def get_result_by_stream(self, file_steam):
        """
        通过音频流获取解码结果的迭代器
        :param file_steam: 字节流
        :return: response结果的迭代
        """
        header_adder_interceptor = header_manipulator_client_interceptor.header_adder_interceptor(
            'audio_meta', base64.b64encode(self.request.SerializeToString()))
        with grpc.insecure_channel(self.host) as channel:
            intercept_channel = grpc.intercept_channel(channel,
                                                       header_adder_interceptor)
            stub = audio_streaming_pb2_grpc.AsrServiceStub(intercept_channel)
            responses = stub.send(file_steam)
            for response in responses:
                yield response
