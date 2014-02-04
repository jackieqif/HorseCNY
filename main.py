import webapp2
import jinja2
from google.appengine.api import users


def Render(name, data=None):
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
  """Handle index page"""
  def get(self):
    user = users.get_current_user()
    username = user.nickname()
    sender = self.request.get('sender')
    try:
      username = username[0].upper() + username[1:]
      sender = sender[0].upper() + sender[1:]
    except IndexError:
      pass
    data = {'sender': sender, 'username': username}
    result = Render('index.template', data)
    self.response.write(result)


app = webapp2.WSGIApplication([
    ('/', MainHandler)
    ], debug=True)


if __name__ == '__main__':
  main()
