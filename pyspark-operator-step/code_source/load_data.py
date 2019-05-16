from pyspark import SparkContext

def test_parallelize(sc):
	"""
	对parallelize使用
	"""
	print('{}{}'.format('parallelize:',sc.parallelize([0, 2, 3, 4, 6], 5).collect()))

def test_textFile(sc):
	"""
	对textFile使用
	"""
	lines=sc.textFile('D:\PySpark-Env\README.md')
	print('{}{}'.format('textFile -> num of doc lines:',lines.count()))
	print('{}{}'.format('textFile -> doc first line:',lines.first()))

def test_wholeTextFiles(sc):
	"""
	对wholeTextFiles使用
	"""
	lines=sc.wholeTextFiles('D:\PySpark-Env\README.md')
	print('{}{}'.format('wholeTextFiles -> num of doc lines:',lines.count()) )
	print('{}{}'.format('wholeTextFiles -> doc first line:',lines.first()) )
	
if __name__=='__main__': 
	sc = SparkContext()
	test_parallelize(sc)
	test_textFile(sc)
	test_wholeTextFiles(sc)