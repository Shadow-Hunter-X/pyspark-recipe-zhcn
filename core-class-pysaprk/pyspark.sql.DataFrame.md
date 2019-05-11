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


