from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext

def read_file_stream():
    sc = SparkContext.getOrCreate()
    ssc = StreamingContext(sc, 1)

    stream_data = ssc.textFileStream("D:\Developing\data")
    #stream_data = ssc.textFileStream("D:\Developing\data").map(lambda x: len(x))
    stream_data.pprint()
    ssc.start()
    ssc.awaitTermination()

def save_stream_rdd():
    sc = SparkContext.getOrCreate()
    spark = SparkSession(sc)
    ssc = StreamingContext(sc, 1)
    stream_data = ssc.textFileStream("D:\Developing\data")   
    value = stream_data.countByValue()
    #print(value)
    ssc.start()
    ssc.awaitTermination()

if __name__=="__main__":
    read_file_stream()
    #save_stream_rdd()