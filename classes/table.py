import itertools


class Table:

  def __init__(self, name, columns, data):
    self.name = name
    self.columns = columns
    self.data = data
    self.index_of_column = dict(
      (column[0], i) for i, column in enumerate(self.columns)
    )

  def where(self, conditions):
    filtered_rows = []
    for row in self.data:
      for condition in conditions:
        import pdb; pdb.set_trace()
        pass

      filtered_rows.append(row)

    return Table(self.name, self.columns, filtered_rows)

  def get_columns_with_table_name_prefix(self):
    prefixed_columns = []
    for column in self.columns:
      prefixed_columns.append(
        ['{}.{}'.format(self.name, column[0]), column[1]]
      )

    return prefixed_columns

  def join(self, table):
    joined_columns = self.get_columns_with_table_name_prefix() + table.get_columns_with_table_name_prefix()
    joined_data = [
      self_data + table_data for self_data, table_data in itertools.product(self.data, table.data)
    ]
    return Table('{}.{}'.format(self.name, table.name), joined_columns, joined_data)

  @staticmethod
  def join_tables(tables):
    joined_table = tables[0]

    for table in tables[1:]:
      joined_table = joined_table.join(table)

    return joined_table

  def __str__(self):
    output = '\n'
    output += ' '.join([column[0] for column in self.columns])
    for row in self.data:
      output += '\n'
      for item in row:
        output += str(item) + ' '

    return output
