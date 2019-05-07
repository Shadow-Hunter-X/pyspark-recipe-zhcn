---
title: spark-支持的文件系统和sparkSql
---

## Spark支持的文件系统
Spark 支持读写很多种文件系统，可以使用任何我们想要的文件格式;
Spark 支持从本地文件系统中读取文件，不过它要求**文件在集群中所有节点的相同路径下都可以找到**

-  从本地文件系统读取一个压缩的文本文件 
~~~python
rdd = sc.textFile("file:///home/happypandas.gz")
~~~

-   Amazon S3 路径写法
~~~
s3n://bucket/my-files/*.txt
~~~

-   HDFS路径写法
~~~
hdfs://master:port/path
~~~

## Spark Sql

Spark SQL是在Spark 1.0中新加入Spark的组件，并快速成为了Spark中较受欢迎的操作结构化和半结构化数据的方式。结构化数据指的是有结构信息的数据——也就是所有的数据记录都具有一致字段结构的集合。
一条SQL查询给Spark SQL让它对一个数据源执行查询（选出一些字段或者对字段使用一些函数），然后得到由Row对象组成的RDD，每个Row对象表示一条记录，
在Python中，可以使用 row[column_number]以及 row.column_name 来访问元素。

### apache Hive

Apache Hive是Hadoop上的一种常见的结构化数据源。Hive可以在HDFS内或者在其他存储系统上存储多种格式的表。Spark SQL可以读取Hive支持的任何表。要把Spark SQL连接到已有的Hive上，需要提供Hive的配置文件。需要将hive-site.xml文件复制到Spark的./conf/目录下。这样做好之后，再创建出 HiveContext 对象，也就是Spark SQL的入口，然后你就可以使用Hive查询语言（HQL）来对你的表进行查询

-   用Python创建HiveContext并查询数据
~~~python
from pyspark.sql import HiveContext
hiveCtx = HiveContext(sc)
rows = hiveCtx.sql("SELECT name, age FROM users")
firstRow = rows.first()
print(firstRow.name)
~~~

### JSON数据

如果记录间结构一致的JSON数据，Spark SQL也可以自动推断出它们的结构信息，并将这些数据读取为记录，这样就可以使得提取字段的操作变得很简单。要读取JSON数据，首先需要和使用Hive一样创建一个HiveContext（不过在这种情况下我们不需要安装好 Hive，也就是说你也不需要hive-site.xml文件）。然后使用 HiveContext.jsonFile方法来从整个文件中获取由Row对象组成的RDD。也可以将RDD数据读取与保存注册为一张表，然后从中选出特定的字段

~~~python
tweets = hiveCtx.jsonFile("tweets.json")
tweets.registerTempTable("tweets")
results = hiveCtx.sql("SELECT user.name, text FROM tweets")
~~~

## 连接读取数据库

通过数据库提供的Hadoop连接器或者自定义的Spark连接器，Spark可以访问一些常用的数据库系统

