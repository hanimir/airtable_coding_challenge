class SQLEvaluationException(Exception):

  def __init__(self, message):
    super(SQLEvaluationException, self).__init__(message)


class AmbiguousColumnException(SQLEvaluationException):

  message = 'ERROR: Column reference "{}" is ambiguous; present in multiple tables: {}.'

  def __init__(self, column, matching_tables):
    matching_tables_string = ', '.join(['"{}"'.format(table) for table in matching_tables])
    super(AmbiguousColumnException, self).__init__(self.message.format(column, matching_tables_string))


class InvalidColumnException(SQLEvaluationException):

  message = 'ERROR: Column reference "{}" does not exist.'

  def __init__(self, column):
    super(InvalidColumnException, self).__init__(self.message.format(column))


class InvalidOperandTypesException(SQLEvaluationException):

  message = 'ERROR: Incompatible types to "{}": {} and {}.'

  def __init__(self, operator, left_type, right_type):
    super(InvalidOperandTypesException, self).__init__(
      self.message.format(operator, left_type, right_type))


class InvalidTableException(SQLEvaluationException):

  message = 'ERROR: Unknown table name "{}".'

  def __init__(self, table):
    super(InvalidTableException, self).__init__(self.message.format(table))
