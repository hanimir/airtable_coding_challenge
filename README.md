# Airtable Coding Challenge

The following documents my solution to the Airtable coding challenge.

## Usage

```
$ ./sql_evaluator <table-folder> <sql-json-file> <output-file>
```

Note: `sql_evaluator.py` must be made executable on the machine running it, this can be done by running:
```
chmod +x sql_evaluator.py
```

## Query Evaluation Strategy

My initial solution used the naive cross-product approach. On my second iteration, I decided to implement an optimized query evaluation strategy, which operates as follows:

1. All conditions (which come from the "where" clause of the SQL query) which only affect one table are evaluated, and the corresponding tables are updated.

2. All tables are joined together.

3. The remaining conditions (those which affect multiple tables) are evaluated.

4. The desired columns are selected according to the "select" clause of the SQL query.

The reason why single-table conditions are evaluated first is to reduce the size of the tables that will be joined in step 2. The most expensive operation in the evaluation of a query is the cross-product of the data tables. The cross-product's runtime scales with the number of rows per table, so filtering the tables before step 2 has the potential to significantly improve performance compared to the naive
cross-product approach.

## Test Performance

Using the given `check` script, this solution scores $\frac{9}{9}$ on the provided examples.
