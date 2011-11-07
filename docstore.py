#!/usr/bin/env python2

port = 8000
enable_toc = True
ignore_h1_in_toc = True

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import jinja2
import markdown2
import re
import redis
import sys

if enable_toc:
  import BeautifulSoup

class BadPage(Exception): pass
def confirm(cond):
  if not cond:
    raise BadPage()

r = redis.StrictRedis(host='localhost', port=6379, db=0)

jenv = jinja2.Environment(loader=jinja2.FileSystemLoader('templates/'))
index_page = jenv.get_template('index.html')
doc_page = jenv.get_template('content.html')

def gen_toc(html):
  if ignore_h1_in_toc:
    first_level = 2
  else:
    first_level = 1

  soup = BeautifulSoup.BeautifulSoup(html)
  headers = soup.findAll(re.compile('^h[%d-6]' % first_level))
  output = []
  for header in headers:
    hid = header.get('id')
    title = header.text
    level = int(header.name[-1])
    output.append('%s<a href="#%s">%s</a>' % (
          (level - first_level) * 4 * '&nbsp;', hid, title))
  return '<br/>\n'.join(output)

class RedisPageHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    if self.path == '/':
      self.serve_homepage()
    else:
      self.serve_page(self.path.split('/')[-1])

  def serve_homepage(self):
    print "serve homepage"
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()
    slugs = list(r.smembers('pages'))
    slugs.sort()
    self.wfile.write(index_page.render(slugs=slugs))

  def serve_page(self, page):
    try:
      confirm(re.match('^[a-z]{1,30}$', page))
      contents = r.get(page)
      confirm(contents)
      views = r.incr('%s_views' % page)

      self.send_response(200)
      self.send_header('Content-type', 'text/html')
      self.end_headers()

      output = markdown2.markdown(contents, extras=['footnotes','smarty-pants'])
      if enable_toc:
        output = output.replace('toc-here', gen_toc(output))
      else:
        output = output.replace('toc-here', '')
      self.wfile.write(doc_page.render(title=page, content=output))

    except BadPage:
      self.send_response(404)
      self.send_header('Content-type', 'text/plain')
      self.end_headers()
      self.wfile.write('404: Not found.\nhttp://haldean.org')

if __name__ == '__main__':
  try:
    server = HTTPServer(('', port), RedisPageHandler)
    server.serve_forever()
  except:
    server.socket.close()

