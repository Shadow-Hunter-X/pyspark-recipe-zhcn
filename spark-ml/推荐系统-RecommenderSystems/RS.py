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

final_recommendations.show(10,False)





















