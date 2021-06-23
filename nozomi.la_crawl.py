import os
import threading
from pathlib import Path
from typing import Iterable
from nozomi import api
import multiprocessing

class LockedIterator(object):
    def __init__(self, it):
        self.lock = threading.Lock()
        self.it = it.__iter__()
        self.count = 0

    def __iter__(self): return self

    def next(self):
        self.lock.acquire()
        try:
            self.count = self.count+1
            print("Processing No." + str(self.count) + " file.\r", end=" ")
            return next(self.it)
        finally:
            self.lock.release()

class Administrator():
    def __init__(self, postList: Iterable):
        self.thread_count = multiprocessing.cpu_count()
        self.postList = LockedIterator(postList)
    
    def controlledThreading(self, directory: str):
        thread_list=[]
        #print("DEV:::POST ITER COUNTER = "+ str(len(postIter)))
        for i in range(self.thread_count):
            thread_list.append(Worker(directory, self.postList))
        for i in range(self.thread_count):
            thread_list[i].start()

class Worker(threading.Thread):
    def __init__(self, directory: str, postList):
        super().__init__()
        self.directory = directory
        self.postList = postList

    def run(self):
        while(True):
            try:
                post = self.postList.next()
            except StopIteration:
                break
            if post==None:
                break
            else:
                api.download_media(post, Path(self.directory))

def directoryCreation(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("ERROR")
    return

def removeAllFile(filePath):
    if os.path.exists(filePath):
        for file in os.scandir(filePath):
            os.remove(file.path)
        print("Initiation Complete")
        return
    else:
        print("No Such Directory")
        return

def t_crawling(p_tag, n_tag, directory):
    print(":::PROCESSING:::")
    print("It takes a while, do not shut off the program")
    positive_tags = p_tag
    negative_tags = n_tag
    posts = api.get_posts(positive_tags, negative_tags)
    adm = Administrator(posts)
    adm.controlledThreading(directory)

def crawling(p_tag, n_tag, directory):
    print(":::PROCESSING:::")
    print("It takes a while, do not shut off the program")
    positive_tags = p_tag
    negative_tags = n_tag
    for post in api.get_posts(positive_tags, negative_tags):
        api.download_media(post, Path(directory))

def main():
    print(":::NOZOMI.LA DOWNLOADER:::")
    print("--------------------------")
    while(True):
        print("★Input Tag You Want (Distinguish tag between space bar) : ")
        raw_p_tag = input()
        if raw_p_tag!='':
            break
        else:
            print("▲Tag is Necessary, if you want to exit the program press ctrl+c")
    print("--------------------------------------------------------------------------")
    print("★Input Tag You Don't Want To Crawl (Distinguish tag between space bar) : ")
    raw_n_tag = input()
    print("--------------------------------------------------------------------------")
    p_tag = raw_p_tag.split(' ')
    n_tag=[]
    if raw_n_tag=='':
        n_tag=None
    else:
        n_tag = raw_n_tag.split(' ')
    directoryName = ''.join(p_tag)
    directory = os.path.join(Path.cwd(), directoryName)
    directoryCreation(directory)
    #removeAllFile(directory)
    #crawling(p_tag, n_tag, directory)
    t_crawling(p_tag, n_tag, directory)

if __name__ == "__main__":
    main()