import time
import datetime

def generate_file():
    t = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime())
    newfile = t + '.txt' 
    f = open(newfile ,'w')
    f.write(newfile + """ this is text data , Hello World.\nA StreamingContext represents the connection to a Spark cluster, 
and can be used to create DStream various input sources. It can be from an existing SparkContext. 
After creating and transforming DStreams, the streaming computation can be started and 
stopped using context.start() and context.stop(), respectively. context.awaitTermination() 
allows the current thread to wait for the termination of the context by stop() or by an exception """) 

    f.close()
    print(newfile)

if __name__ == '__main__':
    x = 1 
    while(x<=1):
        time.sleep(2)
        generate_file()
        x += 1
