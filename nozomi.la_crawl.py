import os
import sys
from pathlib import Path
from nozomi import api

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

def crawling(p_tag, n_tag, directory):
    print(":::PROCESSING:::")
    print("It takes a while, do not shut off the program")
    positive_tags = p_tag
    negative_tags = n_tag
    for i, post in enumerate(api.get_posts(positive_tags, negative_tags)):
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
    crawling(p_tag, n_tag, directory)

if __name__ == "__main__":
    main()