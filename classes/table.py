import itertools

from classes.exceptions import (AmbiguousColumnException,
                                InvalidColumnException,
                                InvalidOperandTypesException,
                                InvalidTableException)
from utils import operator_to_function


class Table:

  def __init__(self, name, columns, data):
    self.name = name
    self.columns = columns
    self.data = data
    self.index_of_column = dict(
      (column[0], i) for i, column in enumerate(self.columns)
    )

  def get_columns_with_table_name_prefix(self):
    prefixed_columns = []
    for column in self.columns:
      prefixed_columns.append(
        ['{}.{}'.format(self.name, column[0]), column[1]]
      )

    return prefixed_columns

  def rename_column(self, current_name, new_name):
    i = self.index_of_column[current_name]
    new_columns = self.columns[:i] + [[new_name, self.columns[i][1]]] + self.columns[i + 1:]
    return Table(self.name, new_columns, self.data)

  def remove_column(self, column):
    if column not in self.index_of_column:
      raise InvalidColumnException(column)

    i = self.index_of_column[column]
    new_table_name = '{table_name}-{column_name}'.format(
      table_name=self.name,
      column_name=column
    )
    new_columns = self.columns[:i] + self.columns[i + 1:]
    new_data = [
      row[:i] + row[i + 1:] for row in self.data
    ]

    return Table(new_table_name, new_columns, new_data)

  def get_column_name(self, table_name, column_name):
    if table_name:
      column = '{}.{}'.format(table_name, column_name)
      if column not in self.index_of_column:
        raise InvalidTableException(table_name)
      return column

    matching_columns = [
      column for column in self.index_of_column.keys() if column.split('.')[-1] == column_name
    ]

    if len(matching_columns) == 0:
      raise InvalidColumnException(column_name)
    elif len(matching_columns) > 1:
      matching_tables = [column.split('.')[0] for column in matching_columns]
      raise AmbiguousColumnException(column_name, matching_tables)

    return matching_columns[0]

  def get_condition_value_and_type(self, row, condition):
    if 'literal' in condition:
      literal = condition['literal']
      return (literal, 'str') if isinstance(literal, (str, unicode)) else (literal, 'int')

    table_name = condition['column']['table']
    column_name = condition['column']['name']
    column = self.get_column_name(table_name, column_name)
    column_index = self.index_of_column[column]
    return row[column_index], self.columns[column_index][1]

  def where(self, conditions):
    filtered_rows = []
    for row in self.data:
      row_meets_all_conditions = True
      for condition in conditions:
        operator_string = condition['op']
        operator = operator_to_function.get(operator_string, None)

        left_value, left_type = self.get_condition_value_and_type(row, condition['left'])
        right_value, right_type = self.get_condition_value_and_type(row, condition['right'])

        if left_type != right_type:
          raise InvalidOperandTypesException(operator_string, left_type, right_type)

        row_meets_all_conditions = (
          row_meets_all_conditions and operator(left_value, right_value)
        )

      if row_meets_all_conditions:
        filtered_rows.append(row)

    return Table(self.name, self.columns, filtered_rows)

  def select(self, columns):
    result = self

    columns_to_remove = set(self.index_of_column.keys())
    for column_dict in columns:
      table_name = column_dict['column']['table']
      column_name = column_dict['column']['name']
      column = self.get_column_name(table_name, column_name)
      result = result.rename_column(column, column_dict['as'])
      columns_to_remove.remove(column)

    for column in columns_to_remove:
      result = result.remove_column(column)

    return result

  def write(self, output_file):
    with open(output_file, 'w') as output:
      output.write(str(self))

  def pretty_print(self):
    output = '\n'
    output += ' '.join([column[0] for column in self.columns])
    for row in self.data:
      output += '\n'
      for item in row:
        output += str(item) + ' '

    return output

  def __str__(self):
    output = '[\n'

    output += '    {},\n'.format([
      [str(item) for item in column] for column in self.columns
    ])

    for i, row in enumerate(self.data):
      output += '    {}'.format([
        str(item) if isinstance(item, unicode) else item for item in row
      ])

      if i < len(self.data) - 1:
        output += ','

      output += '\n'

    output += ']'

    return output.replace("'", '"')

  @staticmethod
  def join_tables(tables):
    flatten = lambda lst: [item for sublist in lst for item in sublist]

    joined_table_name = '.'.join([table.name for table in tables])

    prefixed_columns = flatten([
      table.get_columns_with_table_name_prefix() for table in tables
    ])

    joined_data = [
      flatten(row) for row in itertools.product(*[table.data for table in tables])
    ]

    return Table(joined_table_name, prefixed_columns, joined_data)
