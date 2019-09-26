import threading
import requests
import time
import os


class Mythread(threading.Thread):
    def __init__(self, url, startpos, endpos, f):
        super(Mythread, self).__init__()
        self.url = url
        self.startpos = startpos
        self.endpos = endpos
        self.fd = f

    def download(self):
        print('start thread:%s at %s' % (self.getName(), time.time()))
        headers = {'Range': 'bytes=%s-%s' % (self.startpos, self.endpos)}
        res = requests.get(self.url, headers=headers)
        self.fd.seek(self.startpos)
        self.fd.write(res.content)
        print('Stop thread:%s at%s' % (self.getName(), time.time()))
        self.fd.close()

    def run(self):
        self.download()


if __name__ == "__main__":
    url = 'http://www.wendangxiazai.com/word/b-cfbdc77931b765ce050814a9-1.doc'
    filename = url.split('/')[-1]
    filesize = int(requests.head(url).headers['Content-Length'])
    print('%s filesize:%s' % (filename, filesize))

    threadnum = 3
    threading.BoundedSemaphore(threadnum)  # 允许线程个数
    step = filesize // threadnum
    mtd_list = []
    start = 0
    end = -1

    tempf = open('./' + filename, 'w')
    tempf.close()
    mtd_list = []
    with open('./' + filename, 'rb+')as f:
        # 获得文件句柄
        fileno = f.fileno()  # 返回一个整型的文件描述符，可用于底层操作系统的 I/O 操作
        while end < filesize - 1:
            start = end + 1
            end = start + step - 1
            if end > filesize:
                end = filesize
            print('Start:%s,end:%s' % (start, end))
            dup = os.dup(fileno)  # 复制文件句柄
            fd = os.fdopen(dup, 'rb+', -1)
            t = Mythread(url, start, end, fd)
            t.start()
            mtd_list.append(t)
        for i in mtd_list:
            i.join()
    f.close()