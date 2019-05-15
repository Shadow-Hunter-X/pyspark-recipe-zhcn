---
title: pyspark.SparkContext
---

## 类pyspark.SparkContext

A SparkContext represents the connection to a Spark cluster, and can be used to create RDD and broadcast variables on that cluster

Spakcontext 表示与Spark群集的连接,可用于在该群集上创建 RDD 和广播变量。

SparkContext instance is not supported to share across multiple processes out of the box, and PySpark does not guarantee multi-processing execution. Use threads instead for concurrent processing purpose.

SparkContext实例在开箱即用的情况不支持下共享多个进程, PySpark不保证多进程执行,使用线程来应对并发处理。

### SparkContext 类实例参数

class pyspark.SparkContext(master=None, appName=None, sparkHome=None, pyFiles=None, environment=None, batchSize=0, serializer=PickleSerializer(), conf=None, gateway=None, jsc=None, profiler_cls=<class 'pyspark.profiler.BasicProfiler'>)

-   Master - 它是连接到的集群的URL。
-   appName - 工作名称。
-   sparkHome - Spark安装目录。
-   pyFiles - 要发送到集群并添加到PYTHONPATH的.zip或.py文件。
-   environment - 工作节点环境变量。
-   batchSize - 表示为单个Java对象的Python对象的数量。设置1以禁用批处理，设置0以根据对象大小自动选择批处理大小，或设置为-1以使用无限批处理大小。
-   serializer - RDD序列化器。
-   conf - L {SparkConf}的一个对象，用于设置所有Spark属性。
-   gateway- 使用现有网关和JVM，否则初始化新JVM。
-   JSC - JavaSparkContext实例。
-   profiler_cls - 用于进行性能分析的一类自定义Profiler（默认为pyspark.profiler.BasicProfiler）

### SparkContext类函数和属性

-   **accumulator**    
accumulator(value, accum_param=None)
    Create an Accumulator with the given initial value, using a given AccumulatorParam helper object to define how to add values of the data type if provided. Default AccumulatorParams are used for integers and floating-point numbers if you do not provide one. For other types, a custom AccumulatorParam can be used

    创建具有给定初始值的累加器, 使用给定的累积器参数帮助器对象定义如何添加数据类型的值 (如果提供)。如果不提供默认累积参数, 则用于整数和浮点数。对于其他类型, 可以使用自定义的累积参数

-   **broadcast**    
broadcast(value)
    Broadcast a read-only variable to the cluster, returning a L{Broadcast<pyspark.broadcast.Broadcast>} object for reading it in distributed functions. The variable will be sent to each cluster only once.

    将只读变量广播到群集,返回一个L{broadcast<pyspark.broadcast.Broadcast>}对象, 以便在分布式函数中读取该对象。该变量将只发送到每个群集一次。

-   **addFile**   
    Add a file to be downloaded with this Spark job on every node. The path passed can be either a local file, a file in HDFS (or other Hadoop-supported filesystems), or an HTTP, HTTPS or FTP URI。

    在每个节点上添加要使用此Spark作业下载的文件。传递的路径可以是本地文件、HDFS 中的文件 (或其他 hadoop 支持的文件系统), 也可以是 HTTP、HTTPS 或 FTP URI。

~~~python
>>> from pyspark import SparkFiles
>>> path = os.path.join(tempdir, "test.txt")
>>> with open(path, "w") as testFile:
...    _ = testFile.write("100")
>>> sc.addFile(path)
>>> def func(iterator):
...    with open(SparkFiles.get("test.txt")) as testFile:
...        fileVal = int(testFile.readline())
...        return [x * fileVal for x in iterator]
>>> sc.parallelize([1, 2, 3, 4]).mapPartitions(func).collect()
[100, 200, 300, 400]
~~~

-   **addPyFile(path)**   
    Add a .py or .zip dependency for all tasks to be executed on this SparkContext in the future. The path passed can be either a local file, a file in HDFS (or other Hadoop-supported filesystems), or an HTTP, HTTPS or FTP URI

    为将来在此Spark上下文上执行的所有任务添加.py或.zip 依赖项。传递的路径可以是本地文件、HDFS 中的文件 (或其他 hadoop 支持的文件系统), 也可以是 HTTP、HTTPS 或 FTP URI

-   **cancelAllJobs**
    Cancel all jobs that have been scheduled or are running.
    取消已计划或正在运行的所有作业。

-   **defaultParallelism**
    Default min number of partitions for Hadoop RDDs when not given by user
    当用户不给出Hadoop Rdd的分区数时, 默认的最小分区数 

-   **emptyRDD()**
    Create an RDD that has no partitions or elements.
    创建没有分区的空RDD

-   **getLocalProperty(key)**
    Get a local property set in this thread, or null if it is missing. See setLocalProperty
    获取此线程中设置的本地属性, 如果缺少该属性,则为null。

-   **parallelize(c, numSlices=None)**
    Distribute a local Python collection to form an RDD. Using xrange is recommended if the input represents a range for performance.
    分发本地 Python 集合以形成 RDD。如果输入表示性能范围, 则建议使用 xrange。

-   **range(start, end=None, step=1, numSlices=None)**
    Create a new RDD of int containing elements from start to end (exclusive), increased by step every element. Can be called the same way as python’s built-in range() function. If called with a single argument, the argument is interpreted as end, and start is set to 0。
    创建一个新的RDD int包含从开始到结束的元素(独占),逐步增加每个元素。可以用与巨蟒的内置范围()函数相同的方式来调用。如果用单个参数调用,则该参数被解释为结束, 开始设置为0

-   **runJob(rdd, partitionFunc, partitions=None, allowLocal=False)**
    Executes the given partitionFunc on the specified set of partitions, returning the result as an array of elements
    在指定的分区集上执行给定的分区Func, 并将结果作为元素数组返回

~~~python
>>> myRDD = sc.parallelize(range(6), 3)
>>> sc.runJob(myRDD, lambda part: [x * x for x in part])
[0, 1, 4, 9, 16, 25]
~~~

-   **sequenceFile**
    Read a Hadoop SequenceFile with arbitrary key and value Writable class from HDFS, a local file system (available on all nodes), or any Hadoop-supported file system URI. The mechanism is as follows
    从 HDFS、本地文件系统 (在所有节点上都可用) 或任何 Hadoop 支持的文件系统uri中使用任意键和值写入类设置目录读取Hadoop序列文件。这种机制是如下所示的, 在这个机制下, 将对Rdd进行检查。如果在群集上运行, 则该目录必须是HDFS路径
    
-   **setCheckpointDir(dirname)**
    Set the directory under which RDDs are going to be checkpointed. The directory must be a HDFS path if running on a cluster
    设置要检查Rdd的目录。如果在群集上运行, 则该目录必须是HDFS路径

-   **setJobDescription(value)**
    Set a human readable description of the current job.
    设置当前作业的可读说明。

-   **setLocalProperty** 
    Set a local property that affects jobs submitted from this thread, such as the Spark fair scheduler pool
    设置影响从此线程提交的作业的本地属性, 例如对Spark公平计划程序池

-   **setLogLevel**     
    Control our logLevel. This overrides any user-defined log settings. Valid log levels include: ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN
    控制日志级别。这将覆盖任何用户定义的日志设置。有效的日志级别包括: ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN

-   **show_profiles** 

-   **sparkUser()**
    执行SparkContext的用户

-   **startTime**
    spark context 开始时间

-   **applicationId**   
    A unique identifier for the Spark application. Its format depends on the scheduler implementation。

    Spark应用程序的唯一标识符。其格式取决于计划程序实现.在本地环境中的格式类似为： local-1433865536131;在YARN上的格式类似为：application_1433865536131_34483

-   **statusTracker**
    返回statusTracker对象，用于作业执行的状态追踪。

-   **stop()**
    关闭SparkContext

-   **textFile**
    Read a text file from HDFS, a local file system (available on all nodes), or any Hadoop-supported file system URI, and return it as an RDD of Strings。
    从 HDFS、本地文件系统(在所有节点上可用) 或任何hadoop支持的文件系统 URI 读取文本文件, 并将其作为字符串的RDD返回
~~~python
>>> path = os.path.join(tempdir, "sample-text.txt")
>>> with open(path, "w") as testFile:
...    _ = testFile.write("Hello world!")
>>> textFile = sc.textFile(path)
>>> textFile.collect()
['Hello world!']
~~~

-   **union**
    对RDD进行UNION操作
~~~python
>>> path = os.path.join(tempdir, "union-text.txt")
>>> with open(path, "w") as testFile:
...    _ = testFile.write("Hello")
>>> textFile = sc.textFile(path)
>>> textFile.collect()
['Hello']
>>> parallelized = sc.parallelize(["World!"])
>>> sorted(sc.union([textFile, parallelized]).collect())
['Hello', 'World!']
~~~

-   **wholeTextFiles(path, minPartitions=None, use_unicode=True)**
    Read a directory of text files from HDFS, a local file system (available on all nodes), or any Hadoop-supported file system URI. Each file is read as a single record and returned in a key-value pair, where the key is the path of each file, the value is the content of each file

    从 HDFS、本地文件系统 (在所有节点上可用)或任何hadoop支持的文件系统 URI读取文本文件目录。每个文件都作为单个记录读取, 并以键值对返回,其中键是每个文件的路径, 该值是每个文件的内容。

-   **version 查看当前指的spark的版本**