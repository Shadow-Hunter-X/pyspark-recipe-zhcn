---
title: 4-数据操作-DataFrame
---

## 关于DataFrame

DataFrame出现在Spark版本1.3中。可以将DataFrame称为数据集，将其组织为命名列。DataFrame类似于R/Python中的关系数据库或数据框架中的表。它可以说是一个具有良好优化技术的关系表。**DataFrame背后的想法是允许处理大量结构化数据**。DataFrame包含具有Schema模型的行。

DataFrame优于RDD，但也包含RDD的功能。RDD和DataFrame的共同特性是不可变性，在内存中，弹性，分布式计算能力。它允许用户将结构强加到分布式数据集合上,从而提供更高级别的抽象。

可以从不同的数据源构建DataFrame。对于示例结构化数据文件，Hive中的表，外部数据库或现有RDD。DataFrame的应用程序编程接口（API）有多种语言版本。

-   选择DataFrame的原因

DataFrame比RDD领先。因为它提供了内存管理和优化的执行计划;相对的RDD它没有任何内置的优化引擎,没有规定处理结构化数据
由于这样的需求，产生DataFrame，其主要的功能：
    DataFrame是在命名列中组织的分布式数据集合,它等同于RDBMS中的表它可以处理结构化和非结构化数据格式。例如Avro，CSV，弹性搜索和Cassandra.

## 创建DataFrame

对于Spark 2.0来说,所有的功能都可以以类SparkSession类作为切入点。要创建SparkSession，只需要使用**SparkSession.builder()**

使用Spark Session，应用程序可以从现有的RDD，Hive表或Spark数据源创建DataFrame,Spark SQL可以使用DataFrame接口在各种数据源上运行。使用Spark SQL DataFrame，我们可以创建一个临时视图。在DataFrame的临时视图中，可以对数据运行SQL查询。

>>> Spark SQL DataFrame API没有提供编译时类型安全性。因此，如果结构未知，就无法操纵数据,一旦我们将域对象转换为数据帧，就不可能重新生成域对象

>>> Spark SQL中的DataFrame API提高了Spark的性能和可伸缩性。它避免了为数据集中的每一行构造单个对象的垃圾收集成本


~~~python

from pyspark import SparkContext     
from pyspark.sql import SparkSession 
from pyspark.sql.types import StructType, StructField, LongType, StringType
from pyspark.sql import Row
from pyspark.sql import Column
import pandas as pd
import numpy as np

# 创建SparkSession连接到Spark集群-SparkSession.builder.appName('name').getOrCreate()
spark=SparkSession \
.builder \
.appName('my_app_name') \
.getOrCreate()

# 创建DataFrame,可以从不同的数据创建，以下进行对个数据源读取创建说明

def create_json_file():
    df=pd.DataFrame(np.random.rand(5,5),columns=['a','b','c','d','e']).applymap(lambda x: int(x*10))
    file=r"random.csv"
    df.to_csv(file,index=False)

def create_df_from_rdd():
    # 从集合中创建新的RDD
    stringCSVRDD = spark.sparkContext.parallelize([
                    (123, "Katie", 19, "brown"),
                    (456, "Michael", 22, "green"),
                    (789, "Simone", 23, "blue")])

    # 设置dataFrame将要使用的数据模型，定义列名，类型和是否为能为空
    schema = StructType([StructField("id", LongType(), True),
                        StructField("name", StringType(), True),
                        StructField("age", LongType(), True),
                        StructField("eyeColor", StringType(), True)])
    # 创建DataFrame
    swimmers = spark.createDataFrame(stringCSVRDD,schema)
    # 注册为临时表
    swimmers.registerTempTable("swimmers")
    # 使用Sql语句
    data=spark.sql("select * from swimmers")
    # 将数据转换List，这样就可以查看dataframe的数据元素的样式
    print(data.collect())
    # 以表格形式展示数据
    data.show()
    
    print("{}{}".format("swimmer numbers : ",swimmers.count()) )

def create_df_from_json():
    '''
    read的类型是DataFrameReader
    '''
    df = spark.read.json('pandainfo.json')
    df.show()

def create_df_from_csv():
    df=spark.read.csv('random.csv',header=True, inferSchema=True)
    df.show()

def create_df_from_postgres():
    """
    format : 指定数据源格式 - 如 jdbc ， json ， csv等
    options: 为数据源添加相关特性选项
    """
    df=spark.read.format('jdbc').options(
        url='jdbc:postgresql://localhost:5432/northwind',
        dbtable='public.orders',
        user='postgres',
        password='iamroot'
    ).load()

    df.show()

def create_df_from_mysql():
    """
    """
    df=spark.read.format('jdbc').options(
        url='jdbc:mysql://localhost:3306',
        dbtable='mysql.db',
        user='root',
        password='iamneo'
        ).load()

    df.show()

def create_df_from_pandas():
    """
    从Python pandas获取数据
    """
    df = pd.DataFrame(np.random.random((4,4)))
    spark_df = spark.createDataFrame (df,schema=['a','b','c','d'])
    spark_df.show()

def create_df_from_hive(hive):
    # 创建支持Hive的Spark Session
    appName = "PySpark Hive Example"
    master = "local"

    spark = SparkSession.builder \
    .appName(appName) \
    .master(master) \
    .enableHiveSupport() \
    .getOrCreate()

    df = spark.sql("select * from test_db.test_table")
    df.show()

    # 将数据保存到Hive新表
    df.write.mode("overwrite").saveAsTable("test_db.test_table2")
    # 查看数据
    spark.sql("select * from test_db.test_table2").show()


if __name__=='__main__':
    create_json_file()
    create_df_from_rdd() 
    create_df_from_csv()
    create_df_from_json()
    create_df_from_db()
    create_df_from_mysql()
    create_df_from_pandas()

~~~