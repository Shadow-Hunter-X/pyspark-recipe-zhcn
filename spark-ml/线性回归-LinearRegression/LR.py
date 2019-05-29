# 1-创建Sparksession对象
from pyspark.sql import SparkSession
spark=SparkSession.builder.appName('lin_reg').getOrCreate()

# 2-读取数据
from pyspark.ml.regression import LinearRegression
df=spark.read.csv('线性回归-LinearRegression/Linear_regression_dataset.csv',inferSchema=True,header=True)

# 3-探索分析数据
print((df.count(), len(df.columns)))   # 查看数据规模
df.printSchema()  # 查看数据结构类型
df.describe().show(5,False)  # 查看数据集的统计数据,包括平均值，标准差，数量统计等。
from pyspark.sql.functions import corr
df.select(corr('var_1','output')).show()  # 计算数据方差

# 4-构建数据特征
from pyspark.ml.linalg import Vector
from pyspark.ml.feature import VectorAssembler  #  导入库VectorAssembler

vec_assmebler=VectorAssembler(inputCols=['var_1', 'var_2', 'var_3', 'var_4', 'var_5'],outputCol='features')
features_df=vec_assmebler.transform(df)   #  transform函数，是从org.apache.spark.ml.Transformer继承来的

features_df.printSchema() # 查看变换后的结构。

model_df=features_df.select('features','output')  # 构建用于线性回归的数据模型

# 5-将数据划分为 训练数据和预测数据
train_df,test_df=model_df.randomSplit([0.7,0.3])   # 训练数据和预测数据的比例为 7比3

print((train_df.count(), len(train_df.columns)))
print((test_df.count(), len(test_df.columns)))

# 6-构建线性回归模型

from pyspark.ml.regression import LinearRegression   # 导入线性回顾库

lin_Reg=LinearRegression(labelCol='output')   # labelCol,相对于featrues列，表示要进行预测的列

lr_model=lin_Reg.fit(train_df)   # 训练数据 ，fit返回一个 fitted model，即LineRegressionModel对象

lr_model.intercept   # intercept 线性方程的截距。

print(lr_model.coefficients)   #  回归方程中的，变量参数 ,这里分别对应var_1,var_2,var_3,var_4,var_5

training_predictions=lr_model.evaluate(train_df)   # 查看预测数据

training_predictions.meanSquaredError    # 误差值差值平方   

training_predictions.r2  # r2 判定系数,用来判定，构建的模型是否能够准确的预测。

# 7-预测数据
test_predictions=lr_model.evaluate(test_df)    # evaluate的返回类型LinearRegressionSummary,以DataFrame格式返回
print(test_results.r2)
print(test_results.meanSquaredError)