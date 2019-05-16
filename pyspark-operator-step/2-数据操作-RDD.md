---
title : 2-数据操作-RDD
---

## RDD 编程基础 



### 相关概念

**pair RDD**       
Spark为包含键值对类型的RDD提供了一些专有的操作,这些RDD被称为pair RDD。它是很多程序的构成要素，因为它们提供了并行操作各个键或跨节点重新进行数据分组的操作接口。

**transformation操作**     
RDD的两个操作类型之一,transformations操作是返回新RDD的操作。且transformationsRDD是惰性求值的，只有在行动操作中用到这些RDD时才会被计算。许多转化操作都是针对各个元素的，也就是说，这些转化操作每次只会操作RDD中的一个元素。

**action操作**       
RDD的两个操作类型之一,它们会把最终求得的结果返回到驱动器程序，或者写入外部存储系统中。由于行动操作需要生成实际的输出，它们会强制执行那些求值必须用到的RDD的转化操作。

### 创建RDD

* 可以通过在[装载数据](1-装载数据.md)中说明的方法 - parallelize 从集合中创建 ；textFile 从外部文件中创建

* 可以通过现有的RDD基础上创建RDD - 调用transformation函数会返回一个新的RDD

RDD对应的API接口函数 [pyspark.RDD](../core-class-pysaprk/pyspark.RDD.md)

**对于Spark中RDD的操作可以分为以下几大类**    
* transformation操作   
  * 聚合操作
  * 数据分组
  * 连接
  * 数据排序
* action操作

### 针对pair RDD的编程

Spark为包含键值对类型的RDD提供了一些专有的操作,这些RDD被称为pair RDD。它是很多程序的构成要素，因为它们提供了并行操作各个键或跨节点重新进行数据分组的操作接口.

-   Pair RDD的转化操作（以键值对集合{(1, 2), (3, 4), (3, 6)}为例）

|函数|目的|示例|结果|
|-----|-----|-----|------|
|reduceByKey(func)|合并具有相同键的值|rdd.reduceByKey((x, y) => x + y)|{(1,2), (3,10)}|
|groupByKey()|对具有相同键的值进行分组|rdd.groupByKey()|{(1,[2]),(3, [4,6])}|
|combineByKey(createCombiner,mergeValue,mergeCombiners,partitioner)|使用不同的返回类型合并具有相同键的值||
|mapValues(func)|对pair RDD中的每个值应用一个函数而不改变键|rdd.mapValues(x => x+1)|{(1,3), (3,5), (3,7)}|
|flatMapValues(func)|对pairRDD中的每个值应用一个返回迭代器的函数,然后对返回的每个元素都生成一个对应原键的键值对记录,通常用于符号化|rdd.flatMapValues(x => (x to 5))|{(1,2),(1,3),(1,4),(1,5),(3,4),(3,5)}|
|keys()|返回一个仅包含键的RDD|rdd.keys()|{1,3,3}|
|values()|返回一个仅包含值的 RDD|rdd.values()|{2,4,6}
|sortByKey()|返回一个根据键排序的RDD|rdd.sortByKey()|{(1,2),(3,4),(3,6)}|

-   针对两个pair RDD的转化操作（rdd = {(1, 2), (3, 4), (3, 6)}other = {(3, 9)}）

|函数|目的|示例|结果|
|-----|-----|-----|------|
|subtractByKey|删掉RDD中键与other RDD中的键相同的元素|rdd.subtractByKey(other)|{(1, 2)}|
|join|对两个RDD进行内连接|rdd.join(other)|{(3, (4, 9)),(3,(6, 9))}|
|rightOuterJoin|对两个 RDD 进行连接操作，确保第一个RDD的键必须存在（右外连接）|rdd.rightOuterJoin(other)|{(3,(Some(4),9)),(3,(Some(6),9))}|
|leftOuterJoin|对两个RDD进行连接操作，确保第二个RDD的键必须存在（左外连接）|rdd.leftOuterJoin(other)|{(1,(2,None)),(3(4,Some(9))),(3,(6,Some(9)))}|
|cogroup|将两个 RDD 中拥有相同键的数据分组到一起|rdd.cogroup(other)|{(1,([2],[])),(3([4, 6],[9]))}|