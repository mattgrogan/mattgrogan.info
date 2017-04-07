+++
date = "2010-05-12"
title = "Analytic Functions in SQL"
draft = false
tags = ["SQL"]
+++

## Introduction

Analytic, or window, functions are a relatively new addition to the Structured Query Language (SQL) specification. They were first defined in the ANSI 1999 standard and later refined in ANSI 2003. Currently, window functions are available in several major relational database systems, such as Microsoft SQL Server, IBM DB2, Teradata, and Oracle. This paper describes Oracle's implementation.

Where normal aggregate functions return a single row for each group, analytic functions can return multiple rows for each group. This makes it possible to perform complex analytical tasks without the need for complex sub queries or advanced programming.

Examples of analytic functions are:

* Window functions, which allow for cumulative moving averages and sums.
* Lag and lead functions, which can return a value in a row that is a certain number of rows away from the current row.
* Ranking functions, which calculate ranks, percentiles, and so on.

## Examples

Assume we have this dataset:

| EMPNO | ENAME  | JOB       | SAL  |
|-------|--------|-----------|------|
| 7839  | KING   | PRESIDENT | 5000 |
| 7698  | BLAKE  | MANAGER   | 2850 |
| 7782  | CLARK  | MANAGER   | 2450 |
| 7566  | JONES  | MANAGER   | 2975 |
| 7788  | SCOTT  | ANALYST   | 3000 |
| 7902  | FORD   | ANALYST   | 3100 |
| 7369  | SMITH  | CLERK     | 800  |
| 7499  | ALLEN  | SALESMAN  | 1600 |
| 7521  | WARD   | SALESMAN  | 1250 |
| 7654  | MARTIN | SALESMAN  | 1250 |
| 7844  | TURNER | SALESMAN  | 1500 |
| 7876  | ADAMS  | CLERK     | 1100 |
| 7900  | JAMES  | CLERK     | 950  |
| 7934  | MILLER | CLERK     | 1300 |

### Ratio to Report Example

Suppose we wish to create a report listing each employee in order of salary, from highest to lowest and show the percent of overall salary paid to each employee. This is accomplished with either a standard or analytic query.

``` sql
-- Standard Query
select
e.ename, e.job, e.sal,
round(e.sal / t.total, 2) as pct_of_total
from e, (select sum(sal) as total from e) t
order by e.sal desc;

-- Analytic Query
select
  e.ename, e.job, e.sal,
  round( ratio_to_report (e.sal) over (), 2) as pct_of_total
from e
order by e.sal desc;
```

In the standard query, the total salary is obtained from a subquery, joined as a Cartesian product and then current salary is divided by the total salary.

In the analytic example, the function `ratio_to_report()` does all the work. This avoids the Cartesian product and allows the DBMS to optimize the query's performance.


| ENAME  | JOB       | SAL  | PCT_OF_TOTAL |
|--------|-----------|------|--------------|
| KING   | PRESIDENT | 5000 | 0.17         |
| FORD   | ANALYST   | 3100 | 0.11         |
| SCOTT  | ANALYST   | 3000 | 0.10         |
| JONES  | MANAGER   | 2975 | 0.10         |
| BLAKE  | MANAGER   | 2850 | 0.10         |
| CLARK  | MANAGER   | 2450 | 0.08         |
| ALLEN  | SALESMAN  | 1600 | 0.05         |
| TURNER | SALESMAN  | 1500 | 0.05         |
| MILLER | CLERK     | 1300 | 0.04         |
| MARTIN | SALESMAN  | 1250 | 0.04         |
| WARD   | SALESMAN  | 1250 | 0.04         |
| ADAMS  | CLERK     | 1100 | 0.04         |
| JAMES  | CLERK     | 950  | 0.03         |
| SMITH  | CLERK     | 800  | 0.03         |

### Cumulative Running Total

Now management requests that the report show the cumulative running total of salary. This is accomplished using the `sum()` window function.

``` sql
select
  e.ename, e.job, e.sal,
  round( ratio_to_report (e.sal) over (), 2) as pct_of_total,
sum(e.sal) over (order by e.sal desc rows between unbounded preceding and current row)
  as cumulative_total
from e
order by e.sal desc;
```

| ENAME  | JOB       | SAL  | PCT_OF_TOTAL | CUMULATIVE_TOTAL |
|--------|-----------|------|--------------|------------------|
| KING   | PRESIDENT | 5000 | 0.17         | 5000             |
| FORD   | ANALYST   | 3100 | 0.11         | 8100             |
| SCOTT  | ANALYST   | 3000 | 0.10         | 11100            |
| JONES  | MANAGER   | 2975 | 0.10         | 14075            |
| BLAKE  | MANAGER   | 2850 | 0.10         | 16925            |
| CLARK  | MANAGER   | 2450 | 0.08         | 19375            |
| ALLEN  | SALESMAN  | 1600 | 0.05         | 20975            |
| TURNER | SALESMAN  | 1500 | 0.05         | 22475            |
| MILLER | CLERK     | 1300 | 0.04         | 23775            |
| MARTIN | SALESMAN  | 1250 | 0.04         | 25025            |
| WARD   | SALESMAN  | 1250 | 0.04         | 26275            |
| ADAMS  | CLERK     | 1100 | 0.04         | 27375            |
| JAMES  | CLERK     | 950  | 0.03         | 28325            |
| SMITH  | CLERK     | 800  | 0.03         | 29125            |

The line `sum(e.sal) over (order by e.sal desc rows between unbounded preceding and current row)` can be translated as "Order salary in descending order and calculate the sum between all preceding rows and the current row." The "rows between" clause is referred to as the _window clause_.

### Cumulative Percent

As a next step, showing the cumulative percent is a simple matter of dividing the cumulative total by the grand total. The function `sum(e.sal) over ()` will return the grand total. The lack of a window clause instructs the function to sum over _all_ rows.

``` sql
select
  e.ename, e.job, e.sal,
  round( ratio_to_report (e.sal) over (), 2) as pct_of_total,
  sum(e.sal) over (order by e.sal desc rows between unbounded preceding and current row) as cumulative_total,
  round ( sum(e.sal) over (order by e.sal desc rows between unbounded preceding and current row) /
    sum(e.sal) over (), 2) as cumulative_percent
from e
order by e.sal desc;
```

| ENAME  | JOB       | SAL  | PCT_OF_TOTAL | CUMULATIVE_TOTAL | CUMULATIVE_PERCENT |
|--------|-----------|------|--------------|------------------|--------------------|
| KING   | PRESIDENT | 5000 | 0.17         | 5000             | 0.17               |
| FORD   | ANALYST   | 3100 | 0.11         | 8100             | 0.28               |
| SCOTT  | ANALYST   | 3000 | 0.10         | 11100            | 0.38               |
| JONES  | MANAGER   | 2975 | 0.10         | 14075            | 0.48               |
| BLAKE  | MANAGER   | 2850 | 0.10         | 16925            | 0.58               |
| CLARK  | MANAGER   | 2450 | 0.08         | 19375            | 0.67               |
| ALLEN  | SALESMAN  | 1600 | 0.05         | 20975            | 0.72               |
| TURNER | SALESMAN  | 1500 | 0.05         | 22475            | 0.77               |
| MILLER | CLERK     | 1300 | 0.04         | 23775            | 0.82               |
| MARTIN | SALESMAN  | 1250 | 0.04         | 25025            | 0.86               |
| WARD   | SALESMAN  | 1250 | 0.04         | 26275            | 0.90               |
| ADAMS  | CLERK     | 1100 | 0.04         | 27375            | 0.94               |
| JAMES  | CLERK     | 950  | 0.03         | 28325            | 0.97               |
| SMITH  | CLERK     | 800  | 0.03         | 29125            | 1.00               |

### Partitioning Rows

Window functions do not always have to be based on the order of rows. For example, suppose we want to compare each employee's salary to the average for all employees in the same job. This is accomplished by specifying a partition in the window clause.

``` sql
select
  e.ename, e.job, e.sal,
  round( ratio_to_report (e.sal) over (), 2) as pct_of_total,
  sum(e.sal) over (order by e.sal desc rows between unbounded preceding and current row) as cumulative_total,
  round ( sum(e.sal) over (order by e.sal desc rows between unbounded preceding and current row) /
    sum(e.sal) over (), 2) as cumulative_percent,
  round( avg(e.sal) over (partition by e.job) , 0) as job_average
from e
order by e.sal desc;
```

The `partition by e.job` clause instructs the database to compute the `avg()` function separately for each distinct job title.

| ENAME  | JOB       | SAL  | PCT_OF_TOTAL | CUMULATIVE_TOTAL | CUMULATIVE_PERCENT | JOB_AVERAGE |
|--------|-----------|------|--------------|------------------|--------------------|-------------|
| KING   | PRESIDENT | 5000 | 0.17         | 5000             | 0.17               | 5000        |
| FORD   | ANALYST   | 3100 | 0.11         | 8100             | 0.28               | 3050        |
| SCOTT  | ANALYST   | 3000 | 0.10         | 11100            | 0.38               | 3050        |
| JONES  | MANAGER   | 2975 | 0.10         | 14075            | 0.48               | 2758        |
| BLAKE  | MANAGER   | 2850 | 0.10         | 16925            | 0.58               | 2758        |
| CLARK  | MANAGER   | 2450 | 0.08         | 19375            | 0.67               | 2758        |
| ALLEN  | SALESMAN  | 1600 | 0.05         | 20975            | 0.72               | 1400        |
| TURNER | SALESMAN  | 1500 | 0.05         | 22475            | 0.77               | 1400        |
| MILLER | CLERK     | 1300 | 0.04         | 23775            | 0.82               | 1038        |
| MARTIN | SALESMAN  | 1250 | 0.04         | 25025            | 0.86               | 1400        |
| WARD   | SALESMAN  | 1250 | 0.04         | 26275            | 0.90               | 1400        |
| ADAMS  | CLERK     | 1100 | 0.04         | 27375            | 0.94               | 1038        |
| JAMES  | CLERK     | 950  | 0.03         | 28325            | 0.97               | 1038        |
| SMITH  | CLERK     | 800  | 0.03         | 29125            | 1.00               | 1038        |

Calculating the ratio of salary to the average salary for each job is an exercise left to the reader ;-)
