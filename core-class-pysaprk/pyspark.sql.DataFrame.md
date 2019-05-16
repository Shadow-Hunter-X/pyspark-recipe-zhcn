---
title: pyspark.sql.DataFrame
---

## 类 pyspark.sql.DataFrame     
    A distributed collection of data grouped into named columns.
    A DataFrame is equivalent to a relational table in Spark SQL, and can be created using various functions in SparkSession:

    分布在命名列中的分布式数据集合。DataFrame等效于Spark SQL中的关系表，可以使用以下各种函数创建SparkSession
~~~python
people = spark.read.parquet("...")
~~~

一旦创建，它可以使用各种域专用语言（DSL）中定义的函数来处理：DataFrame，Column。要从数据框中选择列，请使用apply方法
~~~python
ageCol = people.age
~~~

~~~python
# To create DataFrame using SparkSession
people = spark.read.parquet("...")
department = spark.read.parquet("...")

people.filter(people.age > 30).join(department, people.deptId == department.id) \
  .groupBy(department.name, "gender").agg({"salary": "avg", "age": "max"})
~~~

### pyspark.sql.DataFrame(jdf, sql_ctx)类函数和属性

-   **agg(*exprs)**   
    Aggregate on the entire DataFrame without groups
    不分组聚合整个DataFrame

~~~python
>>> df.agg({"age": "max"}).collect()
[Row(max(age)=5)]
>>> from pyspark.sql import functions as F
>>> df.agg(F.min(df.age)).collect()
[Row(min(age)=2)]
~~~

-   **alias(alias)**      
    Returns a new DataFrame with an alias set.
    返回DataFrame带有别名集的new

~~~python
>>> from pyspark.sql.functions import *
>>> df_as1 = df.alias("df_as1")
>>> df_as2 = df.alias("df_as2")
>>> joined_df = df_as1.join(df_as2, col("df_as1.name") == col("df_as2.name"), 'inner')
>>> joined_df.select("df_as1.name", "df_as2.name", "df_as2.age").collect()
[Row(name='Bob', name='Bob', age=5), Row(name='Alice', name='Alice', age=2)]
~~~

-   **approxQuantile(col, probabilities, relativeError)**     
    Calculates the approximate quantiles of numerical columns of a DataFrame.
    计算DataFrame的数值列的近似分位数。

-   **cache()**      
    Persists the DataFrame with the default storage level (MEMORY_AND_DISK)
    DataFrame使用默认存储级别（MEMORY_AND_DISK）

-   **checkpoint(eager=True)**  
    Returns a checkpointed version of this Dataset. Checkpointing can be used to truncate the logical plan of this DataFrame, which is especially useful in iterative algorithms where the plan may grow exponentially. It will be saved to files inside the checkpoint directory set with SparkContext.setCheckpointDir()
    返回此数据集的检查点版本。检查点可用于截断此DataFrame的逻辑计划，这在计划可能呈指数级增长的迭代算法中尤其有用。它将保存到设置的检查点目录内的文件中SparkContext.setCheckpointDir()

-   **coalesce(numPartitions)**         
    Returns a new DataFrame that has exactly numPartitions partitions.
    返回DataFrame具有正确numPartitions分区的新内容

-   **colRegex(colName)**
    Selects column based on the column name specified as a regex and returns it as Column.
    根据指定为正则表达式的列名称选择列并将其返回为Column。

-   **collect()**
    Returns all the records as a list of Row.以行列表的形式返回所有记录

~~~python
>>> df.collect()
[Row(age=2, name='Alice'), Row(age=5, name='Bob')]
~~~

-   **columns**    
    Returns all column names as a list.返回所有的列名.

-   **count()**     
    Returns the number of rows in this DataFrame.返回DataFrame中的函数

-   **cov(col1, col2)**     
    Calculate the sample covariance for the given columns, specified by their names, as a double value
    计算给定列的样本协方差, 由它们的名称指定, 作为double值

-   **createGlobalTempView(name)**    
    Creates a global temporary view with this DataFrame.
    The lifetime of this temporary view is tied to this Spark application. throws TempTableAlreadyExistsException, if the view name already exists in the catalog
    使用此数据框架创建全局临时视图,此临时视图的生存期与此Spark应用程序相关联。如果目录中已存在视图名称, 则会引发异常TempTableAlreadyExistsException

~~~python
>>> df.createGlobalTempView("people")
>>> df2 = spark.sql("select * from global_temp.people")
>>> sorted(df.collect()) == sorted(df2.collect())
True
>>> df.createGlobalTempView("people")  # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
...
AnalysisException: u"Temporary table 'people' already exists;"
>>> spark.catalog.dropGlobalTempView("people")
~~~

-   **createOrReplaceGlobalTempView(name)**     
    Creates or replaces a global temporary view using the given name.The lifetime of this temporary view is tied to this Spark application.      
    使用给定的名称创建或替换全局临时视图。此临时视图的生存期与此Spark应用程序相关联。  

~~~python
>>> df.createOrReplaceGlobalTempView("people")
>>> df2 = df.filter(df.age > 3)
>>> df2.createOrReplaceGlobalTempView("people")
>>> df3 = spark.sql("select * from global_temp.people")
>>> sorted(df3.collect()) == sorted(df2.collect())
True
>>> spark.catalog.dropGlobalTempView("people")
~~~

-   **createOrReplaceTempView(name)**    
    Creates or replaces a local temporary view with this DataFrame.
    The lifetime of this temporary table is tied to the SparkSession that was used to create this DataFrame.
    使用此数据框架创建或替换本地临时视图。此临时表的生存期与用于创建此数据框架的 SparkSession 相关联。

-   **createTempView(name)**
    Creates a local temporary view with this DataFrame,The lifetime of this temporary table is tied to the SparkSession that was used to create this DataFrame. throws TempTableAlreadyExistsException, if the view name already exists in the catalog
    使用此数据框架创建本地临时视图, 此临时表的生存期与用于创建此数据框架的 SparkSession 相关联。如果目录中已存在视图名称, 则会引发异常TempTableAlreadyExistsException

~~~python
>>> df.createTempView("people")
>>> df2 = spark.sql("select * from people")
>>> sorted(df.collect()) == sorted(df2.collect())
True
>>> df.createTempView("people")  # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
...
AnalysisException: u"Temporary table 'people' already exists;"
>>> spark.catalog.dropTempView("people")
~~~

-   **cube(*cols)**     
    Create a multi-dimensional cube for the current DataFrame using the specified columns, so we can run aggregation on them
    使用指定的列为当前Datframe创建多维多维数据集,以便我们可以对其运行聚合.

~~~python
>>> df.cube("name", df.age).count().orderBy("name", "age").show()
~~~

-   **describe(*cols)**     
    Computes basic statistics for numeric and string columns.This include count, mean, stddev, min, and max. If no columns are given, this function computes statistics for all numerical or string columns
    计算数字列和字符串列的基本统计信息。这包括计数、平均值、stddev、最小值和最大值。如果没有给出列, 此函数将计算所有数字列或字符串列的统计信息

~~~python
>>> df.describe(['age']).show()
+-------+------------------+
|summary|               age|
+-------+------------------+
|  count|                 2|
|   mean|               3.5|
| stddev|2.1213203435596424|
|    min|                 2|
|    max|                 5|
+-------+------------------+
>>> df.describe().show()
+-------+------------------+-----+
|summary|               age| name|
+-------+------------------+-----+
|  count|                 2|    2|
|   mean|               3.5| null|
| stddev|2.1213203435596424| null|
|    min|                 2|Alice|
|    max|                 5|  Bob|
+-------+------------------+-----+
~~~

-   **distinct()**
    Returns a new DataFrame containing the distinct rows in this DataFrame   
    返回包含此数据框架中的distinct操作后的新数据框架   

-   **drop(*cols)**    
    Returns a new DataFrame that drops the specified column. This is a no-op if schema doesn’t contain the given column name(s)
    返回删除指定列的新DataFrame。如果架构不包含给定的列名, 则无操作的

-   **dtypes**
    Returns all column names and their data types as a list。返回所有的列和它们的类型

~~~python
>>> df.dtypes
[('age', 'int'), ('name', 'string')]
~~~

-   **exceptAll(other)**
    返回一个新的数据框架, 其中包含此数据框架中的行, 但不返回另一个数据框架中的行, 同时保留重复项。

-   **explain(extended=False)**
    将 (逻辑和物理) 计划打印到控制台以进行调试

-   **fillna(value, subset=None)**
    Replace null values, alias for na.fill(). DataFrame.fillna() and DataFrameNaFunctions.fill() are aliases of each other.
    替换空值, 为 na.fill() 的别名。DataFrame.fillna()和DataFrameNaFunctions.fill()是彼此的别名

-   **filter(condition)**
    Filters rows using the given condition

-   **foreach(f)**
    Applies the f function to all Row of this DataFrame.对DataFrame中的每一行经过f函数处理。
  
-   **foreachPartition(f)**
    Applies the f function to each partition of this DataFrame.对分区中的DataFrame中的每一行经过f函数处理。

-   **printSchema()**

-   **schema**
    Returns the schema of this DataFrame as a pyspark.sql.types.StructType
    schemas是pyspark.sql.types.StructType类型，如果在参数中传递不是StructType类型，则会被转化为StructType类型。

-   **select(*cols)**
    Projects a set of expressions and returns a new DataFrame. 