class AmbiguousColumnException(Exception):

  message = 'ERROR: Column reference "{}" is ambiguous; present in multiple tables: {}.'

  def __init__(self, column, matching_tables):
    pass

  def tables_to_string(self, tables):
    pass

class InvalidColumnException(Exception):

  def __init__(self, message, ):
    pass

class InvalidOperandTypesException(Exception):

  def __init__(self, message, ):
    pass

class InvalidTableException(Exception):

  def __init__(self, message, ):
    pass
