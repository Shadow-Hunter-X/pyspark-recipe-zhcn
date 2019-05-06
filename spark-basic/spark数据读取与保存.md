---
title: spark数据读取于保存
---

Spark支持很多种输入输出源。一部分原因是Spark本身是基于Hadoop生态圈而构建，特别是Spark可以通过Hadoop MapReduce所使用的InputFormat和OutputFormat接口访问数据，而大部分常见的文件格式与存储系统（例如 S3、 HDFS、 Cassandra、 HBase 等）都支持这种接口。

Spark 及其生态系统提供了很多可选方案。接下来介绍以下三类常见的数据源:

-   文件格式与文件系统
对于存储在本地文件系统或分布式文件系统（比如 NFS、 HDFS、 Amazon S3 等）中的数据，Spark可以访问很多种不同的文件格式，包括文本文件、JSON、SequenceFile，以及protocol buffer。会展示几种常见格式的用法，以及Spark针对不同文件系统的配置和压缩选项。

-   Spark SQL中的结构化数据源
它针对包括 JSON 和 Apache Hive 在内的结构化数据源，为我们提供了一套更加简洁高效的 API

-   数据库与键值存储   
Spark 自带的库和一些第三方库，它们可以用来连接 Cassandra、 HBase、Elasticsearch 以及 JDBC 源

## File Formats

-   Spark支持的一些常见格式

|格式名称|结构化|备注|
|-----|-----|-----|
|文本文件|否|普通的文本文件，每行一条记录|
|JSON|半结构化|常见的基于文本的格式，半结构化；大多数库都要求每行一条记录|
|CSV|是|非常常见的基于文本的格式，通常在电子表格应用中使用|
|SequenceFiles|是|一种用于键值对数据的常见 Hadoop 文件格式|
|Protocol buffers|是|一种快速、节约空间的跨语言格式|
|对象文件|是|用来将 Spark 作业中的数据存储下来以让共享的代码读取。改变类的时候它会失效，因为它依赖于Java序列化|

-   文本文件



## File Systems

