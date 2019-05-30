from pyspark.sql import SparkSession 
from pyspark.sql import Row
from pyspark.sql.types import StructType, StructField, LongType, StringType

# 创建SparkSession 对象
spark=SparkSession.builder.appName('my_app_name').getOrCreate()

# json - sql 
def read_json_sql():
    print("----------------read json sql-----------------")
    # 构造用于测试的Json数据
    stringJSONRDD = spark.sparkContext.parallelize((
    """{"id": "123","name": "Katie","age": 19,"eyeColor": "brown"}""",
    """{"id": "234","name": "Michael","age": 22,"eyeColor": "green"}""", 
    """{"id": "345","name": "Simone","age": 23,"eyeColor": "blue"}""")
    )

    # 创建DataFrame
    swimmersJSON = spark.read.json(stringJSONRDD)
    # DataFrame 注册为临时表 swimmersJSON
    swimmersJSON.createOrReplaceTempView("swimmersJSON")
    # DataFrame API 查看数据
    swimmersJSON.show()

    # 使用SQL查询
    data=spark.sql("select * from swimmersJSON").collect()  # sql函数返回的 DataFrame对象
    for i in data:             # 对于data中的每行是 Row类型,数据内容像键值对。
        print(i['eyeColor'])
    swimmersJSON.printSchema() # 查看模型树 

# 指定dataframe中的schema
def specify_schema():
    print("----------------specify schema-----------------")
    stringCSVRDD = spark.sparkContext.parallelize([(123, 'Katie', 19, 'brown'), (234, 'Michael', 22, 'green'), (345, 'Simone', 23, 'blue')])
    schema = StructType([
        StructField("id", LongType(), True),    
        StructField("name", StringType(), True),
        StructField("age", LongType(), True),
        StructField("eyeColor", StringType(), True)
    ])

    swimmers = spark.createDataFrame(stringCSVRDD, schema)  # 创建 DataFrame，并指定schema
    swimmers.createOrReplaceTempView("swimmers")    # 构建临时表swimmers
    spark.sql("SELECT id , age , eyecolor FROM swimmers")   # 选择对应的列
    spark.sql("select count(*) cnt from swimmers")   # 使用聚合函数 
    spark.sql("select id, age from swimmers where age = 22").show()  # 使用where子句
    spark.sql("select name, eyeColor from swimmers where eyeColor like 'b%' ").show()  # 使用like子句
    # --------------- 和spark sql 同样效果的 DataFrame API ------------------
    swimmers.show()
    swimmers.count()
    swimmers.select("id","age").filter("age=22").show()
    swimmers.select("name", "eyeColor").filter("eyeColor like 'b%'").show()

# 多表操作
def multi_table_query():
    print("----------------multi table query-----------------")
    # 构建航班信息表，从文件airport-codes-na.txt文件中
    airportsFilePath = "airport-codes-na.txt"
    airports = spark.read.csv(airportsFilePath, header='true', inferSchema='true', sep='\t')
    airports.createOrReplaceTempView("airports") 

    # 构建航班延误表，从文件departuredelays.txt文件中
    flightPerfFilePath = "departuredelays.csv"
    flightPerf = spark.read.csv(flightPerfFilePath, header='true')
    flightPerf.createOrReplaceTempView("FlightPerformance")
    flightPerf.cache()

    spark.sql("select a.City, f.origin, sum(f.delay) as Delays from FlightPerformance f  \
               join airports a on a.IATA = f.origin  \
               where a.State = 'WA' group by a.City, f.origin order by sum(f.delay) desc").show()

    spark.sql("select a.State, sum(f.delay) as Delays from FlightPerformance f  \
              join airports a on a.IATA = f.origin  \
              where a.Country = 'USA' group by a.State ").show()

if __name__ == "__main__":
    read_json_sql()
    specify_schema()
    multi_table_query()

