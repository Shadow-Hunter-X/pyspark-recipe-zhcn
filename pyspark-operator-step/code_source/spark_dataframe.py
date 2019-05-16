from pyspark import SparkContext     
from pyspark.sql import SparkSession 
from pyspark.sql.types import StructType, StructField, LongType, StringType
from pyspark.sql import Row
from pyspark.sql import Column
import pandas as pd
import numpy as np

# 连接到Spark 集群
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
    #create_json_file()
    #create_df_from_rdd() 
    create_df_from_csv()
    create_df_from_json()