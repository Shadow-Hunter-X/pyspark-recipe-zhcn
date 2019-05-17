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

def create_df_from_parquet(parquet):
    pass

def create_df_from_hive(hive):
    pass

# 数据缓存，存放到内存，存放到外部介质    

if __name__=='__main__':
    #create_json_file()
    #create_df_from_rdd() 
    #create_df_from_csv()
    #create_df_from_json()
    #create_df_from_db()
    create_df_from_mysql()
    #create_df_from_pandas()