import pyspark
from pyspark.sql import SQLContext
from pyspark import SparkContext     
from pyspark.sql.window import Window
from pyspark.sql import SparkSession 
import pyspark.sql.functions as sf
from pyspark.sql.types import StructType, StructField, LongType, StringType
from pyspark.sql import Row
from pyspark.sql import Column
import pandas as pd
import numpy as np

## 在 Spark 1 中使用SQLContext来创建 DataFrame
sc = SparkContext(appName="test")
spark_sc = SQLContext(sc)

def load_data():
    stringCSVRDD = sc.parallelize([
                    (123, "Katie", 19, "brown"),
                    (456, "Michael", 22, "green"),
                    (789, "Simone", 23, "blue")])
    # 设置dataFrame将要使用的数据模型，定义列名，类型和是否为能为空
    schema = StructType([StructField("id", LongType(), True),
                        StructField("name", StringType(), True),
                        StructField("age", LongType(), True),
                        StructField("eyeColor", StringType(), True)])
    # 创建DataFrame
    swimmers = spark_sc.createDataFrame(stringCSVRDD,schema)
    # 注册为临时表
    swimmers.registerTempTable("swimmers")
    # 使用Sql语句
    data=spark_sc.sql("select * from swimmers")
    # 将数据转换List，这样就可以查看dataframe的数据元素的样式
    print(data.collect())
    # 以表格形式展示数据
    data.show()
    print("{}{}".format("swimmer numbers : ",swimmers.count()) )

def read_from_json():
    df = spark_sc.read.json('pandainfo.json')
    df.show()

def read_from_csv():
    df=spark_sc.read.csv('random.csv',header=True, inferSchema=True)
    df.show()

def read_from_postgresql():
    df=spark_sc.read.format('jdbc').options(
        url='jdbc:postgresql://localhost:5432/northwind',
        dbtable='public.orders',
        user='postgres',
        password='iamroot'
    ).load()
    df.show()

def read_from_mysql():
    df=spark_sc.read.format('jdbc').options(
        url='jdbc:mysql://localhost:3306?useUnicode=true&characterEncoding=utf8&serverTimezone=UTC',
        dbtable='mysql.db',
        user='root',
        password='iamneo'
        ).load()
    df.show()

def read_from_hive():
    #from pyspark import SparkContext
    #from pyspark.sql import HiveContext

    sc = SparkContext("local", "pySpark Hive JDBC Demo App")
    # Create a Hive Context
    hive_context = HiveContext(sc)
    crime = hive_context.table("default.crime")
    crime.registerTempTable("crime_temp")
    pettythefts = hive_context.sql('SELECT * FROM crime_temp WHERE Primary_Type = "THEFT" AND Description = "$500 AND UNDER"')

    pettythefts_table_df = pettythefts.select("id", "case_number", "primary_type", "description", "location_description", "beat", "district", "ward", "community_area")

    mode = 'overwrite'
    url = 'jdbc:postgresql://<database server IP address>:5432/postgres?searchpath=public'
    properties = {"user": "<username>", "password": "<password>", "driver": "org.postgresql.Driver"}
    table = 'public.pettytheft'

    pettythefts_table_df.write.jdbc(url=url, table=table, mode=mode, properties=properties)


if __name__ == '__main__':
    load_data()
    read_from_json()
    read_from_csv()
    read_from_postgresql()
    read_from_mysql()