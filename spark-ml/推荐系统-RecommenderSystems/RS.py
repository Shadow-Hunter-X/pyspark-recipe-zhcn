from pyspark.sql import SparkSession 
spark=SparkSession.builder.appName('rs').getOrCreate()

from pyspark.sql.functions import *

print('-------------查看数据情况，检测数据质量和相关的特征。即相对数据有一定的认识，对后续进行训练做准备--------------------')

df_ratings=spark.read.csv('ml-latest-small/ratings.csv',inferSchema=True,header=True)   # 读取电影评分数据
df_ratings.createOrReplaceTempView("ratings")   # 构建临时表评分表
df_movie=spark.read.csv('ml-latest-small/movies.csv',inferSchema=True,header=True)   # 读取电影数据
df_movie.createOrReplaceTempView("movies")         # 构建临时电影表，这两张表通过sql关联，得到具体电影的评分

spark.sql("SELECT ratings.movieId , movies.title , movies.genres , ratings.rating  FROM ratings   \
          LEFT JOIN movies ON ratings.movieId = movies.movieId ").show(100)

"""

print((df.count(),len(df.columns)))             # 查看数据规模

df.printSchema()                                # 数据列信息

df.orderBy(rand()).show(10,False)               # 查看数据

print('-------------- 进行数据转换,主要将类别数据，转换为可通过数值来度量------------------')

from pyspark.ml.feature import StringIndexer,IndexToString              # StringIndexer可以把字符串的列按照出现频率进行排序，将字符串转化为可度量的

stringIndexer = StringIndexer(inputCol="title", outputCol="title_new")  # 构建StringIndexer对象，设定输入列和输出列

model = stringIndexer.fit(df)                                           # 构建model模型

indexed = model.transform(df)                                           # 使用模型转换数据

indexed.show(10)

indexed.groupBy('title_new').count().orderBy('count',ascending=False).show(10,False)    # 查看分类的数据样式

train,test=indexed.randomSplit([0.75,0.25])                             # 划分训练数据和测试数据

print('--------------- 使用推荐模型相关的库 ------------------------')

from pyspark.ml.recommendation import ALS

"""