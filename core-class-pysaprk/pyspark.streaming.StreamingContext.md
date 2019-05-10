---
title: pyspark.streaming.StreamingContext
---

## 类pyspark.streaming.StreamingContext
Main entry point for Spark Streaming functionality. A StreamingContext represents the connection to a Spark cluster, and can be used to create DStream various input sources. It can be from an existing SparkContext. After creating and transforming DStreams, the streaming computation can be started and stopped using context.start() and context.stop(), respectively. context.awaitTermination() allows the current thread to wait for the termination of the context by stop() or by an exception

Spark Streaming的主要入口点。StreamingContext表示与Spark群集的连接,可用于创建各种输入源。它可以来自现有的SparkContext。创建和转换DStreams后,可以分别使用context.start和context.stop()启动和停止流计算。context.awaitTermination()允许当前线程等待或异常终止。

### pyspark.streaming.StreamingContext类实例参数

pyspark.streaming.StreamingContext(sparkContext, batchDuration=None, jssc=None)


### StreamingContext类函数和属性

-   **addStreamingListener(streamingListener)**
    Add a [[org.apache.spark.streaming.scheduler.StreamingListener]] object for receiving system events related to streaming
    添加一个[org.apache.spark.streaming.scheduler.StreamingListener]对象用于接收和流相关的系统事件消息。

-   **awaitTermination(timeout=None)**
    Wait for the execution to stop 等待停止执行，timeout为超时设置

-   **awaitTerminationOrTimeout(timeout)**
    Wait for the execution to stop. Return true if it’s stopped; or throw the reported error during the execution; or false if the waiting time elapsed before returning from the method
    等待执行停止。如果停止或在执行过程中抛出报告的错误返,返回true; 如果等待的时间过去之前从方法返回,则返回false

-   **binaryRecordsStream(directory, recordLength)**
    Create an input stream that monitors a Hadoop-compatible file system for new files and reads them as flat binary files with records of fixed length. Files must be written to the monitored directory by “moving” them from another location within the same file system. File names starting with are ignored .

    创建一个输入流,用于监视与hadoop兼容的文件系统中的新文件, 并将其读取为具有固定长度记录的平面二进制文件。必须通过从同一文件系统中的其他位置"移动"文件,将文件写入受监视的目录。以“.”开始的文件名将会被忽略

-   **checkpoint(directory)**
    Sets the context to periodically checkpoint the DStream operations for master fault-tolerance. The graph will be checkpointed every batch interval
    将上下文设置为定期检查主容错的DStream操作。每个批处理间隔都会检查该图

-   **classmethod getActive()**
    Return either the currently active StreamingContext 返回当前正在执行的活动的StreamingContext

-   **classmethod getActiveOrCreate(checkpointPath, setupFunc)**
    Either return the active StreamingContext (i.e. currently started but not stopped), or recreate a StreamingContext from checkpoint data or create a new StreamingContext using the provided setupFunc function. If the checkpointPath is None or does not contain valid checkpoint data, then setupFunc will be called to create a new context and setup DStreams

    返回一个活动的StreamingContext，或从checkpoint中重新创建StreamingContext，亦或是创建一个全新的StreamingContext，通过提供的setupFunc函数。如果checkpointPath为空或不存在一个有效的checkpoint，那么将调用setFunc函数进行创建一个新的context和安装DStreams 

-   **classmethod getOrCreate(checkpointPath, setupFunc)**  
    Either recreate a StreamingContext from checkpoint data or create a new StreamingContext. If checkpoint data exists in the provided checkpointPath, then StreamingContext will be recreated from the checkpoint data. If the data does not exist, then the provided setupFunc will be used to create a new context

    从checkpoint中重新创建StreamingContext，亦或是创建一个全新的StreamingContext，通过提供的setupFunc函数。如果checkpointPath为空或不存在一个有效的checkpoint，那么将调用setFunc函数进行创建一个新的context和安装DStreams 

-   **queueStream(rdds, oneAtATime=True, default=None)**
    Create an input stream from a queue of RDDs or list. In each batch, it will process either one or all of the RDDs returned by the queue
    从Rdd或list队列中创建输入流。在每个批处理中,它将处理队列返回的一个或所有Rdd

-   **remember(duration)**
    Set each DStreams in this context to remember RDDs it generated in the last given duration. DStreams remember RDDs only for a limited duration of time and releases them for garbage collection. This method allows the developer to specify how long to remember the RDDs (if the developer wishes to query old data outside the DStream computation).

    在此上下文中设置每个DStream, 以记住它在上次给定持续时间内生成的Rdd。DStream只在有限的时间内记住Rdd,并将其释放以进行垃圾回收。此方法允许开发人员指定记住Rdd的时间 (如果开发人员希望查询 DStream 计算之外的旧数据)。

-   **socketTextStream(hostname, port, storageLevel=StorageLevel(True, True, False, False, 2))**
    Create an input from TCP source hostname:port. Data is received using a TCP socket and receive byte is interpreted as UTF8 encoded \n delimited lines.
    从TCP源主机名(端口)创建输入。数据是使用TCP套接字接收的,接收字节被解释为UTF8编码的\n分隔的行。

-   **sparkContext**
    Return SparkContext which is associated with this StreamingContext. 返回和StreamingContext关联的SparkContext

-   **start()**
    Start the execution of the streams. 开始执行流

-   **stop(stopSparkContext=True, stopGraceFully=False)**
    Stop the execution of the streams, with option of ensuring all received data has been processed.
    停止流执行，并提供确保已处理所有接收到的数据的选项

-   **textFileStream(directory)**
    Create an input stream that monitors a Hadoop-compatible file system for new files and reads them as text files. Files must be wrriten to the monitored directory by “moving” them from another location within the same file system. File names starting with . are ignored    
    创建一个输入流,用于监视与hadoop兼容的文件系统中的新文件, 并将其读取为具有固定长度记录的平面二进制文件。必须通过从同一文件系统中的其他位置"移动"文件,将文件写入受监视的目录。以“.”开始的文件名将会被忽略

-   **transform(dstreams, transformFunc)**
    Create a new DStream in which each RDD is generated by applying a function on RDDs of the DStreams. The order of the JavaRDDs in the transform function parameter will be the same as the order of corresponding DStreams in the list
    创建一个新的 DStream, 其中每个RDD都是通过在Dstream的Rdd上应用函数生成的。转换函数参数中Javasrdd的顺序将与列表中相应Dstrem的顺序相同。

-   **union(*dstreams)**
    Create a unified DStream from multiple DStreams of the same type and same slide duration.
    从多个不同的DStreams中创建一样的类型和时间间隔的DStream。    