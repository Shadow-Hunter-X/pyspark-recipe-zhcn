from pyspark.sql import SparkSession
spark=SparkSession.builder.appName('random_forest').getOrCreate()

print('-----------读取用于测得数据,检测数据质量和相关的特征。即相对数据有一定的认识，对后续进行逻辑回归训练做准备------------------')

# 读取数据
df=spark.read.csv('cars.csv',inferSchema=True,header=True)

print((df.count(),len(df.columns)))

df.printSchema()

df.describe().select('summary','地区','驾驶员年龄','驾龄','每年保养次数','汽车类型').show() # 全景数据分析统计，会对各列按 平均值，方差，最小值，最大值 , 函数统计 这几个统计量来进行统计。
df.groupBy('故障').count().show()                                                        # 以故障汇总数据
df.groupBy('地区').count().show()                                                        # 以所在地进行汇总数据 
df.groupBy('汽车类型','故障').count().orderBy('汽车类型','故障','count',ascending=True).show()  

df.groupBy('每年保养次数','故障').count().orderBy('每年保养次数','故障','count',ascending=True).show()

df.groupBy('故障').mean().show()                                                        # 计算均值


print('-----------数据转换，将所有的特征值放到一个特征向量中，预测值分开.划分数据用于模型------------------')

from pyspark.ml.feature import VectorAssembler                                         #一个 导入VerctorAssembler 将多个列合并成向量列的特征转换器,即将表中各列用一个类似list表示，输出预测列为单独一列。

df_assembler = VectorAssembler(inputCols=['地区', '驾驶员年龄', '驾龄', '每年保养次数', '汽车类型'], outputCol="features")
df = df_assembler.transform(df)
df.printSchema()

df.select(['features','故障']).show(10,False)

model_df=df.select(['features','故障'])                                               # 选择用于模型训练的数据
train_df,test_df=model_df.randomSplit([0.75,0.25])                                    # 训练数据和测试数据分为75%和25%

train_df.groupBy('故障').count().show()
test_df.groupBy('故障').count().show()

print('-----------使用随机深林进行数据训练----------------')

from pyspark.ml.classification import RandomForestClassifier

rf_classifier=RandomForestClassifier(labelCol='故障',numTrees=50).fit(train_df)      # numTrees设置随机数的数量为50,还有其他参数：maxDepth 树深;返回的模型类型为：RandomForestClassificationModel

rf_predictions=rf_classifier.transform(test_df)

print('{}{}'.format('评估每个属性的重要性:',rf_classifier.featureImportances))   # featureImportances : 评估每个功能的重要性,

rf_predictions.select(['probability','故障','prediction']).show(10,False)

print("------查阅pyspark api，没有发现有训练准确率的字段，所以还需要计算预测的准确率------")

from pyspark.ml.evaluation import BinaryClassificationEvaluator      # 对二进制分类的评估器,它期望两个输入列:原始预测值和标签
from pyspark.ml.evaluation import MulticlassClassificationEvaluator  # 多类分类的评估器,它期望两个输入列:预测和标签

rf_accuracy=MulticlassClassificationEvaluator(labelCol='故障',metricName='accuracy').evaluate(rf_predictions)
print('MulticlassClassificationEvaluator 随机深林测试的准确性： {0:.0%}'.format(rf_accuracy))

rf_auc=BinaryClassificationEvaluator(labelCol='故障').evaluate(rf_predictions)
print('BinaryClassificationEvaluator 随机深林测试的准确性： {0:.0%}'.format(rf_auc))


print('-----------保持模型，用于下次使用----------------')

rf_classifier.save("RF_model")