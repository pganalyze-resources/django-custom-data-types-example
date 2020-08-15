from django.db import models
from django.db import connection
from psycopg2.extras import register_composite
from psycopg2.extensions import register_adapter, adapt, AsIs

Rgb = register_composite(
  'rgb_color_value',
  connection.cursor().cursor,
  globally=True
).type

def rgb_adapter(value):
  return AsIs("(%s, %s, %s)::rgb_color_value" % (
    adapt(value.red).getquoted(),
    adapt(value.green).getquoted(),
    adapt(value.blue).getquoted()
  ))

register_adapter(Rgb, rgb_adapter)

class Rgb:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

class RgbField(models.Field):
  
  def parse_rgb(self, value):
      return Rgb(value.red, value.green, value.blue)

  def from_db_value(self, value, expression, connection):
      if value is None:
          return value
      return self.parse_rgb(value)

  def to_python():
      if isinstance(value, Rgb):
          return value

      if value is None:
          return value

      return self.parse_rgb(value)

  def get_prep_value(self, value):
      return (value.red, value.green,value.blue)
  
  def db_type(self, connection):
      return 'rgb_color_value'

class StringNoSpaces(models.Field):
    
    def db_type(self, connection):
        return 'string_no_spaces'

class Color(models.Model):
    rgb = RgbField()
    name = StringNoSpaces()
