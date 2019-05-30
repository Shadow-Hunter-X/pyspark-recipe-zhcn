---
title: 数据操作-Streaming
---

## spark streaming

数据流是连续到达的无界数据序列。流式传输将连续流动的输入数据划分为离散单元以进行进一步处理。流处理是低延迟处理和流数据分析。
实现高吞吐量和容错的实时数据流流处理。数据摄取可以从许多来源完成，如Kafka，Apache Flume，Amazon Kinesis或TCP套接字，可以使用复杂算法完成处理，这些算法用map，reduce，join和window等高级函数表示。最后，处理后的数据可以推送到文件系统，数据库和实时仪表板

通过Spark流接收实时输入数据流并将其分成批次，然后由Spark引擎处理这些批次以批量生成最终结果流。

spark streaming的关键抽象是Apache Spark Discretized Stream，或者简言之，Spark DStream，它表示分成小批量的数据流。DStreams构建于Spark的
核心数据抽象Spark RDD之上。这允许Spark中的Streaming与Spark MLlib和Spark SQL等任何其他Apache Spark组件无缝集成

### 为何要在Spark中引入Streaming

像Apache Hadoop这样的批处理系统具有高延迟，不适合近实时处理要求。如果尚未处理，则Storm保证记录的处理，但这可能导致不一致，因为可能存在重复的记录处理。如果运行Storm的节点出现故障，状态将丢失。在大多数环境中，Hadoop用于批处理，而Storm用于流处理，导致代码大小增加，修复错误的数量，开发工作量，引入学习曲线，并导致其他问题。这创造了大数据Hadoop和Apache Spark之间的区别。

为了解决传统流处理引擎的问题，Spark Streaming使用一种称为Discretized Streams的新架构，该架构直接利用了Spark引擎的丰富库和容错功能。

### Spark Streaming架构和优势

Spark Streaming不是一次处理一条记录的流数据，而是将数据离散化为微小的亚秒级微批次。换句话说，Spark Streaming接收器并行接受数据并将其缓冲在Spark的工作节点的内存中。然后，延迟优化的Spark引擎运行短任务来处理批次并将结果输出到其他系统。
与传统的连续运算符模型不同，传统的连续运算符模型将计算静态分配给节点，Spark任务根据数据位置和可用资源动态分配给工作者。这可实现更好的负载平衡和更快的故障恢复。每批数据都是弹性分布式数据集（RDD）在Spark中，它是Spark中容错数据集的基本抽象。这允许使用任何Spark代码或库处理流数据。

Spark Streaming 具有以下几方面的优势：     
a）动态负载平衡      
b）快速失败和落后者恢复     
c）批量，流媒体和交互式分析       
d）机器学习和交互式SQL等高级分析      
e）性能       

### Spark Streaming如何工作

在Spark Streaming中，将数据流划分为称为DStreams的批处理，其内部是一系列RDD。RDD使用Spark API进行处理，结果分批返回。
Spark Streaming在Scala，Java和Python中提供API 。Spark Streaming维护一个基于流中数据的状态，并将其称为有状态计算。它还允许窗口操作（即，允许开发人员指定时间帧以对在该时间窗口中流动的数据执行操作）。窗口中有一个滑动间隔，即更新窗口的时间间隔。

### Spark Streaming操作

-   Spark Streaming的Transformation操作
    与Spark RDD类似，Spark转换允许修改输入DStream中的数据。DStreams支持许多普通Spark RDD上可用的转换。一些常见的如下。
    map（），flatMap（），filter（），repartition（numPartitions），union（otherStream），count（），reduce（），countByValue（），reduceByKey（func，[numTasks]），join（otherStream，[numTasks] ），cogroup（otherStream，[numTasks]），transform（），updateStateByKey（），Window（）

-   Spark Streaming的输出操作
    DStream的数据使用输出操作推送到外部系统，如数据库或文件系统。由于外部系统使用输出操作允许的转换数据，因此它们会触发所有DStream转换的实际执行。目前，以下输出操作定义为：
    print（），saveAsTextFiles（prefix，[suffix]）“prefix-TIME_IN_MS [.suffix]”，saveAsObjectFiles（prefix，[suffix]），saveAsHadoopFiles（prefix，[suffix]），foreachRDD （func）
    因此，像RDD这样的DStream像输出操作一样懒惰地执行。具体而言，DStream输出操作中的RDD操作会强制处理接收到的数据

### Spark CheckPoint

由于需要Spark Streaming应用，应该是每天24小时运作。因此，系统也应该是容错的。如果丢失了任何数据，则应该快速恢复。Spark checkpoint完成此操作
因此，Checkpointing是截断RDD DAG的过程。它可以及时将应用程序状态保存到可靠存储（HDFS）。当驱动程序重新启动时，将进行恢复

我们在Spark中检查了两种类型的数据：

元数据检查点 -  元数据是指有关数据的数据。它指的是将元数据保存到容错存储（如HDFS）。元数据包括配置，DStream操作和不完整批次。配置是指用于创建流式DStream操作的配置是定义流式应用程序的操作。不完整的批次是在队列中但不完整的批次。

数据检查点 -：它指的是将RDD 保存到可靠的存储，因为它需要在一些有状态转换中出现。在即将到来的RDD取决于先前批次的RDD的情况下。因此，依赖性随着时间的推移而不断增加。因此，为了避免恢复时间的这种增加，将中间RDD周期性地检查点到一些可靠的存储器。结果，它减少了依赖链。