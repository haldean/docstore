#!/usr/bin/env python2

import markdown
import re
import redis
import sys

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class BadPage(Exception): pass
def confirm(cond):
  if not cond:
    raise BadPage()

r = redis.StrictRedis(host='localhost', port=6379, db=0)
class RedisPageHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    page = self.path.strip('/')
    print('Serving %s' % page)

    try:
      confirm(re.match('^[a-z]{1,30}$', page))
      contents = r.get(page)
      confirm(contents)
      views = r.incr('%s_views' % page)

      self.send_response(200)
      self.send_header('Content-type', 'text/html')
      self.end_headers()

      with open('head.html', 'r') as head:
        self.wfile.write(head.read())

      self.wfile.write(markdown.markdown(contents))

      with open('tail.html', 'r') as tail:
        self.wfile.write(tail.read())

    except BadPage:
      self.send_response(404)
      self.send_header('Content-type', 'text/plain')
      self.end_headers()
      self.wfile.write('404: Not found.\nhttp://haldean.org')

if __name__ == '__main__':
  try:
    server = HTTPServer(('', 8000), RedisPageHandler)
    server.serve_forever()
  except:
    server.socket.close()

