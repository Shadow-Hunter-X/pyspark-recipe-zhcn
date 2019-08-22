from pyspark.sql import SparkSession
import pyspark

from pyspark.sql.functions import * 
from pyspark.sql.types import *
from pyspark.sql.functions import rand, randn
from pyspark.ml.clustering import KMeans

spark = SparkSession.builder.appName('k_means').getOrCreate()  # 创建SparkSession对象

print("------------------读取数据-----------------")

df=spark.read.csv('iris_dataset.csv',inferSchema=True,header=True)  # 读取数据

print("------------------查看分析数据-----------------")

print((df.count(),len(df.columns)))         # 查看数据规模

# 查看列信息
df.printSchema()
df.columns            

df.orderBy(rand()).show(10,False)           # 查看数据，随机的方式

df.groupBy('species').count().orderBy('count',ascending=False).show(10,False) # 汇总查看数据

print("-----------------数据转换-------------------")

from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler    # 导入VerctorAssembler 将多个列合并成向量列的特征转换器,即将表中各列用一个类似list表示，输出预测列为单独一列。


input_cols=['sepal_length', 'sepal_width', 'petal_length', 'petal_width']

# 将所有的属性转换为转化为一个vector
vec_assembler = VectorAssembler(inputCols = input_cols, outputCol='features')
final_data = vec_assembler.transform(df)

print("------------设定不同的K值，进行分类,计算平方误差之和------------")

errors=[]

for k in range(2,10):
    kmeans = KMeans(featuresCol='features',k=k)
    model = kmeans.fit(final_data)
    intra_distance = model.computeCost(final_data)
    errors.append(intra_distance)
    print("With K={}".format(k))
    print("Within Set Sum of Squared Errors = " + str(errors))
    print('--'*30)

print("-----------使用mathplot计算，汇总不同K值-----------------")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

cluster_number = range(2,10)
plt.scatter(cluster_number,errors)
plt.xlabel('Number of Clusters (K)')
plt.ylabel('SSE')
plt.show()

# 通过图形，查看k=4时较为合适
kmeans = KMeans(featuresCol='features',k=4,)
model = kmeans.fit(final_data)

predictions=model.transform(final_data)

predictions.groupBy('species','prediction').count().show()      # 查看分类的数据

print("---------将数据转换为panda结构，并查看空间3d图心-----------")

pandas_df = predictions.toPandas()
pandas_df.sample(5)

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

cluster_vis = plt.figure(figsize=(15,10)).gca(projection='3d')
cluster_vis.scatter(pandas_df.sepal_length, pandas_df.sepal_width, pandas_df.petal_length, c=pandas_df.prediction,depthshade=False)
plt.show()