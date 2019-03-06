import json
import os

from classes.table import Table
from classes.exceptions import (AmbiguousColumnException,
                                InvalidColumnException,
                                InvalidTableException)


class Query:

  def __init__(self, select, sources, where):
    self.select = select
    self.sources = sources
    self.where = where
    self.tables = []
    self.index_of_table = {}

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
          self.index_of_table[source['as']] = len(self.tables)
          self.tables.append(Table(name=source['as'], columns=table[0], data=table[1:]))
      except IOError:
        raise InvalidTableException(table_name)

  def get_tables_with_column(self, table_name, column_name):
    tables = []
    if table_name:
      if table_name in self.index_of_table:
        tables.append(table_name)
      else:
        raise InvalidTableException(table_name)
    else:
      for table in self.tables:
        try:
          table.get_column_name(table_name, column_name)
        except InvalidColumnException:
          continue
        else:
          tables.append(table.name)

    return tables

  def get_tables_affected_by_condition(self, condition):
    affected_tables = []
    if 'literal' not in condition['left']:
      table_name = condition['left']['column']['table']
      column_name = condition['left']['column']['name']

      tables_affected_by_left = self.get_tables_with_column(table_name, column_name)
      if len(tables_affected_by_left) > 1:
        raise AmbiguousColumnException(column_name, tables_affected_by_left)

      affected_tables.extend(tables_affected_by_left)

    if 'literal' not in condition['right']:
      table_name = condition['right']['column']['table']
      column_name = condition['right']['column']['name']

      tables_affected_by_right = self.get_tables_with_column(table_name, column_name)
      if len(tables_affected_by_right) > 1:
        raise AmbiguousColumnException(column_name, tables_affected_by_right)

      affected_tables.extend(tables_affected_by_right)

    return affected_tables

  def get_conditions_on_one_table(self):
    results = []
    for condition in self.where:
      affected_tables = self.get_tables_affected_by_condition(condition)
      if len(affected_tables) == 1:
        results.append((condition, affected_tables[0]))

    return results

  def evaluate(self):
    conditions_on_one_table = self.get_conditions_on_one_table()
    for condition, table in conditions_on_one_table:
      index_of_table = self.index_of_table[table]
      self.tables[index_of_table] = self.tables[index_of_table].where([condition])

    evaluated_conditions = [condition for condition, _ in conditions_on_one_table]
    conditions_left_to_evaluate = [
      condition for condition in self.where if condition not in evaluated_conditions
    ]

    return Table.join_tables(self.tables)           \
                .where(conditions_left_to_evaluate) \
                .select(self.select)
