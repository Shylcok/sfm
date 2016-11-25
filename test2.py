#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: test2.py
@time: 16/11/25 上午11:48
"""


import time
from datetime import timedelta
from tornado import httpclient, gen, ioloop, queues


class AsySpider(object):

    def __init__(self, urls, concurrency):
        self.urls = urls
        self.concurrency = concurrency
        self._q = queues.Queue()
        self._fetching = set()
        self._fetched = set()

    def handle_page(self, url, html):
        """inherit and rewrite your own method to handle page"""
        print(html)

    @gen.coroutine
    def get_page(self, url):
        try:
            response = yield httpclient.AsyncHTTPClient().fetch(url)
            print('######fetched %s' % url)
        except Exception as e:
            print('Exception: %s %s' % (e, url))
            raise gen.Return('')
        raise gen.Return(response.body)

    @gen.coroutine
    def _run(self):

        @gen.coroutine
        def fetch_url():
            current_url = yield self._q.get()
            try:
                if current_url in self._fetching:
                    return

                print('fetching****** %s' % current_url)
                self._fetching.add(current_url)
                html = yield self.get_page(current_url)
                self._fetched.add(current_url)

                self.handle_page(current_url, html)

                for i in range(self.concurrency):
                    if self.urls:
                        yield self._q.put(self.urls.pop())

            finally:
                self._q.task_done()

        @gen.coroutine
        def worker():
            while True:
                yield fetch_url()

        self._q.put(self.urls.pop())

        # Start workers, then wait for the work queue to be empty.
        for _ in range(self.concurrency):
            worker()
        yield self._q.join(timeout=timedelta(seconds=300000))    # set a timeout
        assert self._fetching == self._fetched

    def run(self):
        io_loop = ioloop.IOLoop.current()
        io_loop.run_sync(self._run)


def main():
    urls = []
    for i in range(1, 73000):
        urls.append('http://127.0.0.1/%s.html' % 1)
    s = AsySpider(urls, 10)
    s.run()

if __name__ == '__main__':
    main()
