from .views import *

urls = [
  ('/registration', ['POST'], registration),
  ('/test', ['GET'], test)
]