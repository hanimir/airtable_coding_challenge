#!/usr/bin/env python

import json
import sys

from collections import defaultdict

from classes.query import Query


def evaluate_sql(table_folder, sql_json_file, output_file):
  query = Query.load_from_file(sql_json_file)
  query.load_tables(table_folder)
  result = query.evaluate()
  result.write(output_file)


if __name__ == '__main__':
  if len(sys.argv) < 4:
    raise RuntimeError('Not enough arguments!')
  elif len(sys.argv) > 4:
    raise RuntimeError('Too many arguments!')

  table_folder = sys.argv[1]
  sql_json_file = sys.argv[2]
  output_file = sys.argv[3]
  evaluate_sql(table_folder, sql_json_file, output_file)
