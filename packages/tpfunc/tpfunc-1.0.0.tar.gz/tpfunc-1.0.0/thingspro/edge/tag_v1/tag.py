#!/usr/bin/python

import os
import json
import queue
import requests
import requests_unixsocket
import threading


class Token():
    def __init__(self):
        self._ip = os.getenv('APPMAN_HOST_IP', default='localhost')
        self._port = os.getenv('APPMAN_HOST_PORT', default=59000)
        self._prefix = os.getenv('MX_API_VER', default='api/v1/')

        with open("/var/run/mx-api-token") as f:
            token = f.readline()
            self._headers = {"Content-Type": "application/json", "mx-api-token": token.strip()}

class Access(Token):
    def __init__(self):
        super().__init__()
        self.__read_tag_url = "http://{}:{}/{}tags/access".format(self._ip, self._port, self._prefix)
        self.__write_tag_url = "http://{}:{}/{}tags/access".format(self._ip, self._port, self._prefix)

    def read(self, provider, source, tag):
        """ direct-read tag function """
        url = "{}/{}/{}/{}".format(self.__read_tag_url, provider, source, tag)
        r = requests.get(url, headers=self._headers, timeout=3)
        if r.status_code is 200:
            return r.status_code, r.json()
        else:
            return r.status_code, {}

    def write(self, provider, source, tag, data_type, data_value):
        """ direct-write tag function """
        url = "{}/{}/{}/{}".format(self.__write_tag_url, provider, source, tag)
        r = requests.put(url, headers=self._headers, json={"dataType": data_type, "dataValue": data_value}, timeout=3)
        if r.status_code is 200:
            return r.status_code, r.json()
        else:
            return r.status_code, {}

class Publisher(Token):
    def __init__(self):
        super().__init__()
        self._session = requests_unixsocket.Session()
        self.__pub_url = "http+unix://%2Frun%2Ftaghub%2Fhttp.sock/tags/publish"

    def publish(self, data):
        """ tag publish function """
        self._session.post(url=self.__pub_url, data=json.dumps(data))


class Subscriber(Token):
    def __init__(self):
        super().__init__()
        self._threads = {}
        self._session = requests_unixsocket.Session()
        self.__pub_url = "http+unix://%2Frun%2Ftaghub%2Fhttp.sock/tags/monitor"

    def __has_subscribed(self, provider, source):
        key = "{}/{}".format(provider, source)
        if self._threads.get(key, None) is not None:
            return True, key
        else:
            return False, ""

    def __get_endpoint(self, provider, source, tags):
        sep = ","
        url = "{}/{}/{}?tags={}&onChanged".format(self.__sub_url, provider, source, sep.join(tags))
        return url

    def __tag_monitoring(self, url):
        try:
            r = self._session.get(url=url, headers=self._headers, stream=True)

            if r.encoding is None:
                r.encoding = 'utf-8'

            for line in r.iter_lines(decode_unicode=True):
                if line:
                    data = json.loads(line[5:])
                    if hasattr(self, 'callback'):
                        self.callback(data)
        except Exception as e:
            print(e)

    def subscribe_callback(self, callback):
        self.callback = callback

    def subscribe(self, provider, source, tags):
        """ tag subscribe function (streaming) """
        if provider == "" or source == "" or not isinstance(tags, list):
            raise ValueError

        if len(tags) == 0:
            raise ValueError

        subscribed, topic = self.__has_subscribed(provider, source)
        if subscribed:
            return

        url = self.__get_endpoint(provider, source, tags)
        self._threads[topic] = threading.Thread(target=self.__tag_monitoring, args=(url, ), daemon=True).start()

    def unsubscribe(self, provider, source):
        if hasattr(self, '_threads'):
            subscribed, topic = self.__has_subscribed(provider, source)
            if not subscribed:
                return

            thread = self._threads.get(topic, None)
            if thread is not None:
                thread.stop()
                self._threads.pop(topic, None)

