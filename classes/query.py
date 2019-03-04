import json
import os

from classes.table import Table
from classes.exceptions import InvalidTableException


class Query:

  def __init__(self, select, sources, where):
    self.select = select
    self.sources = sources
    self.where = where
    self.tables = []

  @classmethod
  def load_from_file(cls, filename):
    with open(filename, 'rU') as json_query_file:
      query = json.load(json_query_file)
      return cls(query['select'], query['from'], query['where'])

  def load_tables(self, table_folder):
    for source in self.sources:
      table_name = source['source']
      table_filepath = os.path.join(table_folder, '{}.table.json'.format(table_name))
      try:
        with open(table_filepath, 'rU') as table_file:
          table = json.load(table_file)
          self.tables.append(Table(name=source['as'], columns=table[0], data=table[1:]))
      except IOError:
        raise InvalidTableException(table_name)

  def evaluate(self):
    return Table.join_tables(self.tables) \
                .where(self.where)        \
                .select(self.select)
