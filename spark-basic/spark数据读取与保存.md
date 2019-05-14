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

-   **Spark支持的一些常见格式**

|格式名称|结构化|备注|
|-----|-----|-----|
|文本文件|否|普通的文本文件，每行一条记录|
|JSON|半结构化|常见的基于文本的格式，半结构化；大多数库都要求每行一条记录|
|CSV|是|非常常见的基于文本的格式，通常在电子表格应用中使用|
|SequenceFiles|是|一种用于键值对数据的常见 Hadoop 文件格式|
|Protocol buffers|是|一种快速、节约空间的跨语言格式|
|对象文件|是|用来将 Spark 作业中的数据存储下来以让共享的代码读取。改变类的时候它会失效，因为它依赖于Java序列化|

-   **文本文件**

在Spark中读写文本文件很容易。当我们将一个文本文件读取为RDD 时，输入的每一行都会成为 RDD 的一个元素。也可以将多个完整的文本文件一次性读取为一个 pair RDD，其中键是文件名，值是文件内容。只需要使用文件路径作为参数调用SparkContext中的textFile()函数，就可以读取一个文本文件。

读取文件
~~~python
input = sc.textFile("file:///home/spark/README.md")
~~~

保存文件 
~~~ python
result.saveAsTextFile(outputFile)
~~~
saveAsTextFile()方法接收一个路径，并将RDD中的内容都输入到路径对应的文件中。Spark将传入的路径作为目录对待，会在那个目录下输出多个文件。这样Spark就可以从多个节点上并行输出了。

**Spark 支持从本地文件系统中读取文件，不过它要求文件在集群中所有节点的相同路径下都可以找到**

-   **JSON文件**

将数据作为文本文件读取， 然后对JSON数据进行解析，这样的方法可以在所有支持的编程语言中使用。这种方法假设文件中的每一行都是一条JSON记录。如果你有跨行的JSON 数据，就只能读入整个文件，然后对每个文件进行解析。

读取json文件，使用python中的原生json库
~~~python
from pyspark import SparkContext
import sys
import json
sc = SparkContext(master, "LoadJson")
input = sc.textFile(inputFile)
data = input.map(lambda x: json.loads(x))
~~~
保存json文件
~~~python
(data.filter(lambda x: x['lovesPandas']).map(lambda x: json.dumps(x)).saveAsTextFile(outputFile))
sc.stop()
~~~

-   **逗号分隔值与制表符分隔值-CSV&TSV**
逗号分隔值（CSV）文件每行都有固定数目的字段，字段间用逗号隔开（在制表符分隔值文件，即TSV文件中用制表符隔开）。记录通常是一行一条，不过也不总是这样有时也可以跨行。 CSV 文件和 TSV 文件有时支持的标准并不一致，主要是在处理换行符、转义字符、非 ASCII 字符、非整数值等方面。

使用Python自带的csv库
~~~python
from pyspark import SparkContext
import csv
import sys
import StringIO

def loadRecord(line):
    input = StringIO.StringIO(line)
    reader = csv.DictReader(input, fieldnames=["name", "favouriteAnimal"])
    return reader.next()

if __name__ == "__main__":
    input = sc.textFile(inputFile)
    data = input.map(loadRecord)
    pandaLovers = data.filter(lambda x: x['favouriteAnimal'] == "panda")
    pandaLovers.mapPartitions(writeRecords).saveAsTextFile(outputFile)
    fullFileData = sc.wholeTextFiles(inputFile).flatMap(loadRecords)
    fullFilePandaLovers = fullFileData.filter(lambda x: x['favouriteAnimal'] == "panda")
    fullFilePandaLovers.mapPartitions(writeRecords).saveAsTextFile(outputFile + "fullfile")
    sc.stop()
~~~

-   **SequenceFile**
SequenceFile是由没有相对关系结构的**键值对**文件组成的常用Hadoop格式。SequenceFile文件有同步标记，Spark可以用它来定位到文件中的某个点，然后再与记录的边界对齐。这可以让Spark使用多个节点高效地并行读取 SequenceFile 文件

Spark有专门用来读取SequenceFile 的接口。在SparkContext 中，可以调用 sequenceFile(path,keyClass, valueClass, minPartitions)。SequenceFile 使用 Writable 类，因此 keyClass和valueClass 参数都必须使用正确的Writable类

~~~python
data=sc.sequenceFile(inFile,"org.apache.hadoop.io.Text", "org.apache.hadoop.io.IntWritable")
data.saveAsSequenceFile("file_name")
~~~

