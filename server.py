#!/usr/local/bin/python3
# coding: utf-8

# Webhook - server.py
# 2/11/21 08:49
#

__author__ = "Benny <benny.think@gmail.com>"

import os
import logging
import json
import subprocess
import requests
import platform
from http import HTTPStatus

from concurrent.futures import ThreadPoolExecutor
from tornado import web, ioloop, httpserver, gen, options
from tornado.log import enable_pretty_logging

from tornado.concurrent import run_on_executor

enable_pretty_logging()

secret, token, cmd, chat_id = os.getenv("secret"), os.getenv("token"), os.getenv("cmd"), os.getenv("chat_id")


class BaseHandler(web.RequestHandler):

    def data_received(self, chunk):
        pass


class WebhookHandler(BaseHandler):
    executor = ThreadPoolExecutor(10)

    @run_on_executor()
    def send_welcome(self):
        return "What a lovely day!"

    @run_on_executor()
    def process_webhook(self):
        webhook_secret = self.get_query_argument("secret")

        if webhook_secret == secret:
            output = self.execute_command()
            self.tg_notification(platform.node(), output)
        else:
            self.set_status(HTTPStatus.BAD_REQUEST)
            output = "Bad secret."
        return output

    @staticmethod
    def execute_command():
        output = subprocess.check_output(cmd.split())
        logging.info(output)
        return output

    @staticmethod
    def tg_notification(hostname, output):
        if chat_id:
            api = "https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}" \
                  "&text={hostname}\n\n<pre>{output}</pre>" \
                  "&parse_mode=html"
            requests.get(api.format(token=token, hostname=hostname, output=output, chat_id=chat_id))

    @gen.coroutine
    def get(self):
        resp = yield self.send_welcome()
        self.write(resp)

    @gen.coroutine
    def post(self):
        resp = yield self.process_webhook()
        self.write(resp)


class RunServer:
    handlers = [
        (r'/', WebhookHandler),
    ]

    application = web.Application(handlers, xheaders=True)

    @staticmethod
    def run_server(port, host, **kwargs):
        tornado_server = httpserver.HTTPServer(RunServer.application, **kwargs)
        tornado_server.bind(port, host)
        tornado_server.start(1)

        try:
            print('Server is running on http://{}:{}'.format(host, port))
            ioloop.IOLoop.instance().current().start()
        except KeyboardInterrupt:
            ioloop.IOLoop.instance().stop()
            print('"Ctrl+C" received, exiting.\n')


if __name__ == "__main__":
    options.define("p", default=17928, help="running port", type=int)
    options.define("h", default='0.0.0.0', help="listen address", type=str)
    options.parse_command_line()
    p = options.options.p
    h = options.options.h
    RunServer.run_server(port=p, host=h)
