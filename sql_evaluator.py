#!/usr/bin/env python

import json
import sys

from collections import defaultdict

from classes.query import Query


# def get_tables_from_query(table_folder, query):
#   tables = defaultdict(dict)
#   for source in query['from']:
#     try:
#       table_name = source['source']
#       table_filepath = '{}/{}.table.json'.format(table_folder, table_name)
#       with open(table_filepath, 'rU') as table_file:
#         table = json.load(table_file)
#         tables[table_name]['columns'] = table[0]
#         tables[table_name]['data'] = table[1:]
#     except:
#       raise

#   return tables


def evaluate_sql(table_folder, sql_json_file, output_file):
  query = Query.load_from_file(sql_json_file)
  query.load_tables(table_folder)
  query.evaluate()
  import pdb; pdb.set_trace()
  pass


if __name__ == '__main__':
  if len(sys.argv) != 4:
    raise RuntimeError('Not enough arguments!')
  table_folder = sys.argv[1]
  sql_json_file = sys.argv[2]
  output_file = sys.argv[3]
  evaluate_sql(table_folder, sql_json_file, output_file)
