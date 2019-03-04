import json

from classes.table import Table


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
      try:
        table_name = source['source']
        table_filepath = '{}/{}.table.json'.format(table_folder, table_name)
        with open(table_filepath, 'rU') as table_file:
          table = json.load(table_file)
          self.tables.append(Table(name=source['as'], columns=table[0], data=table[1:]))
      except:
        raise

  def evaluate(self):
    joined_table = Table.join_tables(self.tables)
    filtered_table = joined_table.where(self.where)
    import pdb; pdb.set_trace()
    pass
