---
title: pyspark.SparkContext
---

## 类pyspark.sql.SQLContext
在Spark 1.x中处理Spark中结构化数据（行和列）的入口点。
从Spark 2.0开始，它被替换为SparkSession。但是，为了向后兼容，我们将此类保留在此处。
SQLContext可用于创建DataFrame，注册DataFrame为表，在表上执行SQL，缓存表和读取parquet文件

### SQLContext(sparkContext, sparkSession=None, jsqlContext=None) 是实例参数

    参数
    sparkContext - SparkContext支持这个SQLContext。
    sparkSession - SparkSession这个SQLContext包含的内容。
    jsqlContext  - 可选的JVM Scala SQLContext。如果设置，不会在JVM中实例化新的SQLContext，而是对这个对象进行所有调用

### SQLContext类函数和属性

-   **cacheTable(tableName)**    
    Caches the specified table in-memory.
    将指定的表缓存在内存中。(版本1.0中的新功能)

-   **clearCache()**    
    Removes all cached tables from the in-memory cache.
    从内存缓存中删除所有缓存的表。

-   **createDataFrame(data, schema=None, samplingRatio=None, verifySchema=True)**   
    DataFrame从a RDD，列表或a 创建pandas.DataFrame。
    当schema是列名列表，将从中推断每列的类型data。
    如果schema是None，它会尝试推断模式（列名和类型）data，这应该是一个RDD Row，或namedtuple，或dict。
    当schema是pyspark.sql.types.DataType或数据类型字符串时，它必须与实际数据匹配，否则将在运行时抛出异常。如果给定的模式不是 pyspark.sql.types.StructType，它将被包装成一个 pyspark.sql.types.StructType唯一的字段，字段名称将是“value”，每个记录也将被包装到一个元组中，以后可以将其转换为行。

    如果需要模式推断，samplingRatio则用于确定用于模式推断的行的比率。如果samplingRatio是，将使用第一行None

-   **createExternalTable(tableName, path=None, source=None, schema=None, **options)**    
    根据数据源中的数据集创建外部表。
    它返回与外部表关联的DataFrame。
    数据源由source一组和一组指定options。如果source未指定，spark.sql.sources.default将使用由其配置的默认数据源 
    可选地，可以提供模式作为返回DataFrame和创建的外部表的模式

-   **dropTempTable(tableName)**    
    从目录中删除临时表。

-   **getConf(key, defaultValue=<no value>)**   
    返回给定键的Spark SQL配置属性的值   

-   **classmethod getOrCreate(sc)**     
    获取现有的SQLContext或使用给定的SparkContext创建一个新的SQLContext。

-   **newSession()**    
    返回一个新的SQLContext作为新会话，它具有单独的SQLConf，已注册的临时视图和UDF，但共享SparkContext和表缓存

-   **range(start, end=None, step=1, numPartitions=None)**   
    创建DataFrame与单个pyspark.sql.types.LongType指定的列 id，包含的范围从元素start至end（不包括）与步长值step

-   **read**
    返回一个DataFrameReader可用于读取数据的DataFrame

-   **readStream**
    返回DataStreamReader可用于将数据流读取为流的数据流DataFrame。

-   **registerDataFrameAsTable(df, tableName)**
    将给定的内容注册DataFrame为目录中的临时表,临时表仅在此实例的生命周期内存在SQLContext

-   **sql(sqlQuery)**
    返回DataFrame表示给定查询结果

-   **streams**   
    返回一个StreamingQueryManager允许管理此上下文中StreamingQuery活动的所有 StreamingQueries的内容

-   **table(tableName)**   
    返回指定的表或视图作为DataFrame。

-   **tableNames(dbName=None)**
    返回数据库中表的名称列表dbName。

-   **tables(dbName=None)**
    返回DataFrame包含给定数据库中表的名称,如果dbName未指定，则将使用当前数据库

    