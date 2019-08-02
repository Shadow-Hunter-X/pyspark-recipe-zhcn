---
title : 推荐系统-RecommenderSystem
---

## 推荐系统 

自动推荐内容或产品以个性化的方式向适当的用户提供,以增强整体体验。推荐系统在术语上非常强大使用海量的数据,学会理解偏好。

对于PySpark中的“推荐系统”模块 **pyspark.ml.recommendation module**        
[官方文档链接：api/python/pyspark.ml.html#module-pyspark.ml.recommendation](http://spark.apache.org/docs/latest/api/python/pyspark.ml.html#module-pyspark.ml.recommendation)

## spark 推荐系统的ALS 算法

* 交替最小平方 (ALS) 矩阵分解:                  
ALS 尝试将评级矩阵 R 估计为两个较低级别矩阵(X 和 Y,即 X = Yt = R)的乘积。一般方法是迭代。在每次迭代期间,一个因子矩阵保持不变,而另一个因子矩阵使用最小二乘求解。然后,在求解另一个因子矩阵时,新求解的因子矩阵保持不变。


* 现实场景到推荐系统模型的转换 ; 构建模型 中的转换关系
  * 划分出推荐系统中参与的对象,如在线购物网站中，参与的主要对象是购物者和相关的商品。
  * 将这些对象的按维度属性进行划分，通过这些维度属性可以有效的表示这个对象。如购物者可以通过 年龄，性别，所住城市等这些属性进行表示。
  * 将对象通过对应的属性维度构建好后。假设每个对象可以通过一个函数表示,如: ax1 + bx2 + cx3 + dx4 = y 。为每个对象，依据分配的属性维度个数，构建有相同元的函数。
  * 通过不同对象个体的属性维度值构建矩阵,构建好不同对象的矩阵后，进行矩阵相乘。得到的新矩阵可以认为是每个购物者对相关物品的关联程度。
  * 由于对象的函数表示，是通过假设的，所以需要获取最优函数的办法，即通过使用最小二乘法来获取最佳函数。

* 关于最小二乘法：   
    它通过最小化误差的平方和寻找数据的最佳函数匹配。利用最小二乘法可以简便地求得未知的数据，并使得这些求得的数据与实际数据之间误差的平方和为最小。
最小二乘法还可用于曲线拟合。其他一些优化问题也可通过最小化能量或最大化熵用最小二乘法来表达。

    通俗的说：在平面(也可再高维度空间种)上有若干点，需要使用一个函数来表示这些点；如何确定这个函数是最优的；通过在坐标系上，每个点到这个函数对应的图形的距离的和最小，
由于拟合函数可以有很多种，但是求两点的具体方法：坐标值差的平方的和，后再开方。 把这些值都加起来后求最小情况，就是最小二乘法。

使用最小二乘法的，不同拟合曲线：
![不同函数的拟合曲线](推荐系统-RecommenderSystems/fitted.png)


## 推荐系统的分类

**基于内容推荐**       
    基于内容的推荐（Content-based Recommendation）是信息过滤技术的延续与发展，它是建立在项目的内容信息上作出推荐的，而不需要依据用户对项目的评价意见，更多地需要用机 器学习的方法从关于内容的特征描述的事例中得到用户的兴趣资料

**协同过滤推荐**      
    协同过滤推荐（Collaborative Filtering Recommendation）技术是推荐系统中应用最早和最为成功的技术之一。它一般采用最近邻技术，利用用户的历史喜好信息计算用户之间的距离，然后 利用目标用户的最近邻居用户对商品评价的加权评价值来预测目标用户对特定商品的喜好程度，系统从而根据这一喜好程度来对目标用户进行推荐

**基于关联规则推荐** 
    基于关联规则的推荐（Association Rule-based Recommendation）是以关联规则为基础，把已购商品作为规则头，规则体为推荐对象。关联规则挖掘可以发现不同商品在销售过程中的相关性，在零 售业中已经得到了成功的应用

**基于知识推荐** 
    基于知识的推荐（Knowledge-based Recommendation）在某种程度是可以看成是一种推理（Inference）技术，它不是建立在用户需要和偏好基础上推荐的。基于知识的方法因 它们所用的功能知识不同而有明显区别

**组合推荐**
    由于各种推荐方法都有优缺点，所以在实际中，组合推荐（Hybrid Recommendation）经常被采用。研究和应用最多的是内容推荐和协同过滤推荐的组合。最简单的做法就是分别用基于内容的方法和协同过滤推荐方法 去产生一个推荐预测结果，然后用某方法组合其结果

**基于效用推荐**
    基于效用的推荐（Utility-based Recommendation）是建立在对用户使用项目的效用情况上计算的，其核心问题是怎么样为每一个用户去创建一个效用函数，因此，用户资料模型很大 程度上是由系统所采用的效用函数决定的。基于效用推荐的好处是它能把非产品的属性，如提供商的可靠性（Vendor Reliability）和产品的可得性（Product Availability）等考虑到效用计算中

![wiki上关于推荐系统](推荐系统-RecommenderSystems/Collaborative_filtering.gif)

### 示例代码

* 测试数据-用户电影评分MovieLens, MovieLens 是历史最悠久的推荐系统。它由美国 Minnesota 大学计算机科学与工程学院的 GroupLens 项目组创办，是一个非商业性质的、以研究为目的的实验性站点。MovieLens 主要使用 Collaborative Filtering 和 Association Rules 相结合的技术，向用户推荐他们感兴趣的电影

[MovieLens https://grouplens.org/datasets/movielens/](https://grouplens.org/datasets/movielens/)

[完整数据下载](http://files.grouplens.org/datasets/movielens/ml-latest.zip)                             
[数据样例下载](http://files.grouplens.org/datasets/movielens/ml-latest-small.zip)

在成功获取数据，对文件内容进行说明介绍：

* ratings.csv - 电影评分数据集 
  userId,movieId,rating,timestamp 为其数据列：表示每个用户对每部电影在什么时候的评分。

* movies.csv - 对电影的分类数据集
  movieId,title,genres 为其数据列：表示了每部电影的名字和分类

* tags.csv - 标签文件 
  userId,movieId,tag,timestamp 为其数据列：表示每个用户对电影的分类

* links.csv - 
  movieId,imdbId,tmdbId 为其数据列： 每个电影的 imdb(网路电影资料库),tmdb(电影数据库)的关联编号
  
~~~python
from pyspark.sql import SparkSession 
spark=SparkSession.builder.appName('rs').getOrCreate()

from pyspark.sql.functions import *

print('-------------查看数据情况，检测数据质量和相关的特征。即相对数据有一定的认识，对后续进行训练做准备--------------------')

df_ratings=spark.read.csv('ml-latest-small/ratings.csv',inferSchema=True,header=True)   # 读取电影评分数据
df_ratings.createOrReplaceTempView("ratings")   	# 构建临时表评分表
df_movie=spark.read.csv('ml-latest-small/movies.csv',inferSchema=True,header=True)      # 读取电影数据
df_movie.createOrReplaceTempView("movies")          # 构建临时电影表，这两张表通过sql关联，得到具体电影的评分信息

df_details = spark.sql("SELECT ratings.userId , ratings.movieId , movies.title , movies.genres , ratings.rating  FROM ratings   \
          LEFT JOIN movies ON ratings.movieId = movies.movieId ")		# 两表关联，获取具体的信息
		  
df_details.select('userId','title','rating').where('rating=4').show(10)

print((df_details.count(),len(df_details.columns)))             		# 查看数据规模

df_details.printSchema()                                	    		# 数据列信息

df_details.orderBy(rand()).show(10,False)                       		# 查看数据

print('-------------- 进行数据转换,主要将类别数据，转换为可通过数值来度量------------------')

from pyspark.ml.feature import StringIndexer,IndexToString              # StringIndexer可以把字符串的列按照出现频率进行排序，将字符串转化为可度量的

stringIndexer = StringIndexer(inputCol="title", outputCol="title_new")  # 构建StringIndexer对象，设定输入列和输出列

model = stringIndexer.fit(df_details)                                   # 构建model模型

indexed = model.transform(df_details)                                   # 使用模型转换数据，讲电影名转换为数值，可以进行度量

indexed.show(10)

indexed.groupBy('title_new').count().orderBy('count',ascending=False).show(10,False)    # 查看分类的数据样式

train,test=indexed.randomSplit([0.75,0.25])                             				# 划分训练数据和测试数据

print('--------------- 使用推荐模型ALS算计 ------------------------')

from pyspark.ml.recommendation import ALS

'''
关于 ALS 的参数：maxIter 最大迭代次数  ;  regParam 表示最小二乘法中lambda值的大小 ; userCol ，itemCol 用于表征对象的标识，通过指出这两列后可以，通过它们构建起关系，通过ratingCol表示它们间的关系。构建成评分矩阵
再本例子中：useCol 是 用户ID ，itemCol 是电影名 ，ratingCol 是用户对电影的评分。
'''
rec=ALS(maxIter=10,regParam=0.01,userCol='userId',itemCol='title_new',ratingCol='rating',nonnegative=True,coldStartStrategy="drop")   

rec_model=rec.fit(train)					 # 使用模型训练数据

predicted_ratings=rec_model.transform(test)  # 应用于测试数据

predicted_ratings.printSchema()

predicted_ratings.orderBy(rand()).show(10)	 # 参看应用模型预测的数据

print('------------- 引入回归评估器来度量 推荐系统 --------------')

from pyspark.ml.evaluation import RegressionEvaluator        # RegressionEvaluator 回归评估器，它期望两个输入列:预测和标签。

evaluator=RegressionEvaluator(metricName='rmse',predictionCol='prediction',labelCol='rating')   # 构建回归评估器，评估准确性

rmse=evaluator.evaluate(predicted_ratings)

print('{}{}'.format("标准误差：",rmse))						# 查看使用推荐系统后的预测的标准误差，若标准误差不是很大的话，可以进行下一步操作。

unique_movies=indexed.select('title_new').distinct()    	# 筛选出所有电影，使用distinct
unique_movies.count()

all = unique_movies.alias('all')							# 所有电影df，重命名为 all

watched_movies=indexed.filter(indexed['userId'] == 46).select('title_new').distinct()	# 查看85号用户，看过的所有电影

watched_movies.count()

no_46=watched_movies.alias('no_46')     # 46号用户看过的电影df，重命名为no_46

total_movies = all.join(no_46, all.title_new == no_46.title_new,how='left')		# 关联得出用户46没有观看评分的电影。

total_movies.show(10,False)    	

remaining_movies=total_movies.where(col("no_46.title_new").isNull()).select(all.title_new).distinct()   # 46号用户，没看过电影的df

remaining_movies=remaining_movies.withColumn("userId",lit(46))   		# 添加一列      

recommendations=rec_model.transform(remaining_movies).orderBy('prediction',ascending=False)	

recommendations.show(5,False)	

movie_title = IndexToString(inputCol="title_new", outputCol="title",labels=model.labels)

final_recommendations=movie_title.transform(recommendations)

final_recommendations.show(10,False)            # 但是最后推荐给用户的预估评分都超过了5分，这是个问题

~~~
![part1](推荐系统-RecommenderSystems/part1.png)
![part2](推荐系统-RecommenderSystems/part2.png)
![part3](推荐系统-RecommenderSystems/part3.png)