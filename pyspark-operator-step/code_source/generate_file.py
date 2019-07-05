import time
import datetime
import random
import string

def generate_file():
    t = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime())
    newfile = t + '.txt' 
    f = open(newfile ,'w')
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(32)]
    f.write( newfile + """ this is text data , Hello World : """ + ''.join(str_list) )

    f.close()
    print(newfile)

if __name__ == '__main__':
    x = 1 
    while(x<=1):
        time.sleep(3)
        generate_file()
        x += 1

    
