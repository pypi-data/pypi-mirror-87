#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import json
import requests
import threading


class Token():
    def __init__(self):
        self._ip = os.getenv('APPMAN_HOST_IP', default='localhost')
        self._port = os.getenv('APPMAN_HOST_PORT', default=59000)
        self._prefix = os.getenv('MX_API_VER', default='api/v1/')

        with open("/var/run/mx-api-token") as f:
            token = f.readline()
            self._headers = {"Content-Type": "application/json", "mx-api-token": token.strip()}


class Listener(Token):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.__config = Configuration()
        self.__tag_url = "http://{}:{}/{}tags/monitor".format(self._ip, self._port, self._prefix)
        self.__event_url = "http://{}:{}/{}events".format(self._ip, self._port, self._prefix)

    def __get_tag_endpoint(self):
        urls = []
        tag_list = self.__config.data_driven_tags()
        for provider, sources in tag_list.items():
            for source, tags in sources.items():
                sep = ','
                url = "{}/{}/{}?tags={}&onChanged".format(self.__tag_url, provider, source, sep.join(tags))
                urls.append(url)
        return urls

    def __get_event_endpoint(self):
        sep = ','
        names = []
        categories = []
        event_list = self.__config.data_driven_events()
        for category, ns in event_list.items():
            categories.append(category)
            names = names + ns
        if not (len(categories) and len(names)):
            return ''
        return "{}?categories={}&eventNames={}&event=true".format(self.__event_url, sep.join(categories), sep.join(names))

    def __start_monitoring(self, url):
        while True:
            try:
                    r = requests.get(url, headers=self._headers, stream=True)

                    if r.encoding is None:
                        r.encoding = 'utf-8'

                    for line in r.iter_lines(decode_unicode=True):
                        if line:
                            data = json.loads(line[5:])
                            if hasattr(self, 'callback'):
                                self.callback(data)

            except Exception as e:
                print(e)
            time.sleep(1)

    def listen(self):
        """ subscribe function (streaming) """
        urls = self.__get_tag_endpoint()
        event_url = self.__get_event_endpoint()
        if event_url != '':
            urls.append(event_url)
        for url in urls:
            threading.Thread(target=self.__start_monitoring, args=(url, ), daemon=True).start()


class Configuration():
    def __init__(self):
        self.__load_configuration()
        self.__load_trigger_data()

    def __load_configuration(self):
        try:
            cwd = os.getcwd()
            config = os.getenv('CONFIG')
            config = (cwd + '/package.json') if config is None else config
            with open(config, "r") as f:
                self._db  = json.load(f)
        except Exception as e:
            self.__load_default()

    def __load_default(self):
        self._db = {}
        self._db['executable'] = {}
        self._db['trigger'] = {}
        self._db['expose'] = {}
        self._db['params'] = {}

    def __load_trigger_data(self):
        data = os.getenv('DATA')
        if data is None:
            self._data = ""
            return

        mode = self._db['trigger'].get('mode', None)
        if mode == 'data':
            self._data = data[5:].strip()

    def data_driven_tags(self):
        trigger = self._db['trigger'].get('dataDriven', None)
        if trigger is None:
            return {}
        return trigger.get('tags', {})

    def data_driven_events(self):
        trigger = self._db['trigger'].get('dataDriven', None)
        if trigger is None:
            return {}
        return trigger.get('events', {})

    def name(self):
        return self._db.get('name', '')

    def expose_tags(self):
        return self._db['expose'].get('tags', [])

    def parameters(self):
        return self._db.get('params', {})

    def trigger_data(self):
        try:
            return json.loads(self._data)
        except Exception as e:
            return ""
