# -*-coding:utf-8-*-
from baidu_acu_asr.asr_client import AsrClient
import os
import time
import logging
import baidu_acu_asr.audio_streaming_pb2
from baidu_acu_asr.asr_product import AsrProduct
from multiprocessing import Pool


class AudioHandler:

    def __init__(self):
        pass

    logging.basicConfig(filename="asr_result.log")

    url = ""
    port = ""
    ak = ""
    sk = ""
    service_name = ""

    log_level = 0
    product_id = "888"
    sample_rate = 16000
    product = AsrProduct.SPEECH_SERVICE
    enable_flush_data = False
    handler = None

    def write_file(self, file_path, file_content):
        with open(file_path, "w") as file:
            file.write(file_content.encode("UTF-8"))

    def run(self, file_path):
        for i in range(5):
            client = AsrClient(self.url, self.port, None, self.enable_flush_data,
                               log_level=self.log_level,
                               product_id=self.product_id,
                               sample_rate=self.sample_rate,
                               service_name=self.service_name,
                               app_key=self.ak,
                               app_secret=self.sk)
            responses = client.get_result(file_path)
            file_content = ""
            try:
                for response in responses:
                    if response.type == baidu_acu_asr.audio_streaming_pb2.FRAGMENT_DATA:
                        file_content += response.audio_fragment.result
                        logging.info(file_content)
                    else:
                        logging.warning("type is: %d", response.type)
                self.write_file(file_path + ".txt", file_content)
                logging.info("file %s write complete!", file_path)
                break
            except Exception as ex:
                # 如果出现异常，此处需要重试当前音频
                logging.error("encounter an error: %s, will create a new channel and retry audio!", ex.message)
                time.sleep(0.5)


def go(audio_path):
    """
    一个被pickle的函数，作为代理，防止在python2.7版本下出现pickle异常
    """
    handler = AudioHandler()
    handler.run(audio_path)

def get_audio_files(path):
    audio_names = os.listdir(path)
    audio_paths = []
    for audio_name in audio_names:
        if audio_name.endswith(".wav") or audio_name.endswith(".pcm"):
            logging.info(os.path.join(path, audio_name))
            audio_paths.append(os.path.join(path, audio_name))
    return audio_paths

if __name__ == '__main__':
    start_time = time.time()

    audio_path = "..\\testaudio"
    audio_files = get_audio_files(audio_path)

    pool = Pool(5)
    pool.map(go, audio_files)
    pool.close()
    pool.join()
    logging.info("complete! use time: %s", str(time.time() - start_time))


