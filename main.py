import datetime
import jinja2
import logging
import webapp2


def Render(name, data=None):
  """Return rendered template as str."""
  if not data:
    data = {}
  environment = jinja2.Environment(
      loader=jinja2.FileSystemLoader(['template']))
  environment.globals.update({
      'uri_for': webapp2.uri_for,
      'request': webapp2.get_request()
      })
  template = environment.get_or_select_template(name)
  result = template.render(data)
  return result


class MainHandler(webapp2.RequestHandler):
  """Index page handler."""
  def get(self):
    time_stamp = datetime.datetime.now()
    username = self.request.get('to')
    sender = self.request.get('sender')
    try:
      username = username[0].upper() + username[1:]
      sender = sender[0].upper() + sender[1:]
    except IndexError:
      pass
    data = {'sender': sender, 'username': username}
    result = Render('index.template', data)
    self.response.write(result)
    logging.info('%s, from: %s, to: %s', time_stamp, sender, username)


app = webapp2.WSGIApplication([
    ('/', MainHandler)
    ], debug=True)


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  main()
