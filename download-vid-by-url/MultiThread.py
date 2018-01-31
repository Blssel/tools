# coding:UTF-8
import Queue
import threading
import youtube_dl
import time

path='failed.txt'
global_num=0
num_thread=0
lock=threading.Lock()
queue=Queue.Queue()

#每个线程的工作就是读取一行ID+URL数据，解析，然后下载
#！！！！！读数据和出队列这个步骤需要加线程锁！！！！！！
#定义新线程的代码
def download():
	global global_num
	global lock
	global queue
	global num_thread
	this_thread_num=0

	#上锁
	lock.acquire()
	try:
		num_thread+=1
		if queue.empty():
			return#如果队列读空，则返回
			
		global_num+=1
		this_thread_num=global_num
		line=queue.get().strip()
		print("Successfully read %dth video" %this_thread_num)
		#解锁
	finally:
		lock.release()
	
	#拆成ID和URL
	list_of_line=line.split('	')
	id_unic=list_of_line[0]
	id=id_unic.encode('unicode-escape').decode('string_escape')
	url_unic=list_of_line[1]
	url=url_unic.encode('unicode-escape').decode('string_escape')

	print("It's going to download video %s" %id)
		
	#根据读取到的内容，下载数据（自动跳过并记录失败的数据）
	ydl_opts={
		'outtmpl':id+'.mp4',
		'format': 'bestvideo+bestaudio/best',
		'verbose': True,
		'proxy': '127.0.0.1:8118',
		'preferredquality': '480',
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		try:
			ydl.extract_info(url,download=True)
			print("%d videos is successfully downloaded" %this_thread_num)
			lock.acquire()
			try:
				num_thread=num_thread-1
			finally:
				lock.release()
		except:
			print("!!!!!!------Download fail.Automatically ignoring and recoding its info------!!!!!!!")
			#上锁
			lock.acquire()
			try:
				num_thread=num_thread-1
				with open('failed2.txt','a') as err:
					err.write(line+'\n')
			#解锁
			finally:
				lock.release()
	

def main(): 
	
	#先获取队列，盛装所有的数据
	with open(path) as f:
		list=f.read().split('\n')
		for line in list:
			queue.put(line)
	
	#启动多个线程下载
	while queue.empty() is False:
		if num_thread<10:
			download_thread=threading.Thread(target=download,name='Download')
			download_thread.start()
		time.sleep(0.05)
		
	print "Mission Committed,Please Check the Result!!!!!!!!"
	return





 
if __name__ == '__main__':  
	#begin  
	main()  
	#end 
