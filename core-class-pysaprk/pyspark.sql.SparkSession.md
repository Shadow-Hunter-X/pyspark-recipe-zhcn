---
title: pyspark.sql.SparkSession
---

## 类pyspark.sql.SparkSession(sparkContext, jsparkSession=None)
    The entry point to programming Spark with the Dataset and DataFrame API
    使用Dataset和DataFrame API编程Spark的入口点

    A SparkSession can be used create DataFrame, register DataFrame as tables, execute SQL over tables, cache tables, and read parquet files. To create a SparkSession, use the following builder pattern
    SparkSession可用于创建DataFrame，注册DataFrame为表，执行SQL表，缓存表和读取parquet文件。要创建SparkSession，请使用以下构建器模式：

~~~python
>>> spark = SparkSession.builder \
...     .master("local") \
...     .appName("Word Count") \
...     .config("spark.some.config.option", "some-value") \
...     .getOrCreate()
~~~

### SparkSession类示例参数
class pyspark.sql.SparkSession(sparkContext, jsparkSession=None)

### SparkSession类函数和属性

-   **builder**     
    A class attribute having a Builder to construct SparkSession instances
    具有Builder构造SparkSession实例的类属性

-   **class Builder**
    Builder for SparkSession.
    * appName(name)    
    Sets a name for the application, which will be shown in the Spark web UI.If no application name is set, a randomly generated name will be used.
    设置应用程序的名称，该名称将显示在Spark Web UI中,如果未设置应用程序名称，则将使用随机生成的名称

    * config（key=None，value=None，conf=None）   
    Sets a config option. Options set using this method are automatically propagated to both SparkConf and SparkSession’s own configuration
    设置配置选项。使用此方法设置的选项会自动传递到SparkConf和SparkSession它们自己的配置中

    * enableHiveSupport()   
    Enables Hive support, including connectivity to a persistent Hive metastore, support for Hive serdes, and Hive user-defined functions.
    启用Hive支持，包括与持久性Hive Metastore的连接，对Hive serdes的支持以及Hive用户定义的功能

    * getOrCreate()
    Gets an existing SparkSession or, if there is no existing one, creates a new one based on the options set in this builder
    获取现有的，SparkSession或者，如果没有现有的，则根据此构建器中设置的选项创建新的  
    This method first checks whether there is a valid global default SparkSession, and if yes, return that one. If no valid global default SparkSession exists, the method creates a new SparkSession and assigns the newly created SparkSession as the global default

    * master(master)
    Sets the Spark master URL to connect to, such as “local” to run locally, “local[4]” to run locally with 4 cores, or “spark://master:7077” to run on a Spark standalone cluster  
    设置要连接的Spark主URL，例如“本地”以在本地运行，“local [4]”在本地运行4核，或“spark//master:7077”在Spark独立群集上运行

-   **catalog** 
    Interface through which the user may create, drop, alter or query underlying databases, tables, functions etc.
    用户可通过其创建，删除，更改或查询底层数据库，表，函数等的接口

-   **conf**
    Runtime configuration interface for Spark.Spark的运行时配置界面。
    This is the interface through which the user can get and set all Spark and Hadoop configurations that are relevant to Spark SQL. When getting the value of a config, this defaults to the value set in the underlying SparkContext, if any
    这是用户可以通过该接口获取和设置与Spark SQL相关的所有Spark和Hadoop配置。获取配置的值时，默认为基础中设置的值SparkContext,如果有的话

-   **createDataFrame(data, schema=None, samplingRatio=None, verifySchema=True)**  
    Creates a DataFrame from an RDD, a list or a pandas.DataFrame
    DataFrame从RDD，list或a 创建pandas.DataFrame

-   **newSession()**
    Returns a new SparkSession as new session, that has separate SQLConf, registered temporary views and UDFs, but shared SparkContext and table cache
    返回一个新的SparkSession作为新会话，它具有单独的SQLConf，已注册的临时视图和UDF，但共享SparkContext和表缓存
    
-   **range(start, end=None, step=1, numPartitions=None)**  
    Create a DataFrame with single pyspark.sql.types.LongType column named id, containing elements in a range from start to end (exclusive) with step value step
    创建DataFrame与单个pyspark.sql.types.LongType指定的列 id，包含的范围从元素start至end（不包括）与步长值step

-   **read**
    Returns a DataFrameReader that can be used to read data in as a DataFrame  
    返回一个DataFrameReader可用于读取数据的DataFrame  

-   **readStream**
    Returns a DataStreamReader that can be used to read data streams as a streaming DataFrame.
    返回DataStreamReader可用于将数据流读取为流的数据流DataFrame。  

-   **sparkContext**
    Returns the underlying SparkContext.
    返回底层SparkContext

-   **sql(sqlQuery)**
    Returns a DataFrame representing the result of the given query.
    返回DataFrame表示给定查询结果。

~~~python
>>> df.createOrReplaceTempView("table1")
>>> df2 = spark.sql("SELECT field1 AS f1, field2 as f2 from table1")
>>> df2.collect()
[Row(f1=1, f2='row1'), Row(f1=2, f2='row2'), Row(f1=3, f2='row3')]
~~~

-   **stop()**  
    Stop the underlying SparkContext.
    停止SparkContext

-   **streams**
    Returns a StreamingQueryManager that allows managing all the StreamingQuery StreamingQueries active on this context.    
    返回一个StreamingQueryManager允许管理此上下文中StreamingQuery活动的所有 StreamingQueries的内容。

-   **table(tableName)**
    Returns the specified table as a DataFrame.
    返回指定的表作为DataFrame。

-   **udf**
    Returns a UDFRegistration for UDF registration
    返回UDFRegistrationUDF

-   **version**
    The version of Spark on which this application is running.
    运行此应用程序的Spark版本。