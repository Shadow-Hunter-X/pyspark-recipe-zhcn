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
from pyspark.sql import Row
from pyspark.sql import Column

# 连接到Spark 集群
spark=SparkSession \
.builder \
.appName('my_app_name') \
.getOrCreate()

# 创建DataFrame,可以从不同的数据创建，以下进行对个数据源读取创建说明

def create_df_from_rdd():
    # 从集合中创建新的RDD
    stringCSVRDD = spark.sparkContext.parallelize([
                    (123, "Katie", 19, "brown"),
                    (456, "Michael", 22, "green"),
                    (789, "Simone", 23, "blue")])

    # 设置dataFrame将要使用的数据模型，定义列名，类型和是否为空
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
    df = spark.read.json('pandainfo.json')
    df.show()

def create_df_from_csv():
    df=spark.read.csv('random.csv',header=True, inferSchema=True)
    df.show()

def create_df_from_json(json):
    pass

def create_df_from_csv(csv):
    pass

def create_df_from_db(db):
    pass

def create_df_from_pandas(pandas):
    pass

def create_df_from_parquet(parquet):
    pass

def create_df_from_hive(hive):
    pass

# 数据缓存，存放到内存，存放到外部介质    

if __name__=='__main__':
    create_df_from_rdd()
    create_df_from_csv()
    create_df_from_json()

~~~