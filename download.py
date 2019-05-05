#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
import requests
import json
import os
import time
import sys, getopt

class Downloader():

    def download_file(self, opts):
        '''
        opts.video_url : video url
        opts.file_name : dest file name.
        opts.referer: referer url
        '''
        headers = {
            "Referer":opts["referer"],
            "Accept-Encoding":"identity;q=1, *;q=0",
            "Range":"bytes=0-",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"
        }
            
        with requests.get(opts["video_url"], headers = headers, stream=True) as r:
            r.raise_for_status()
            with open(opts["file_name"], "wb") as f:
                for chunk in r.iter_content(chunk_size=4096): 
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)

    def get_json_data(self, file_path):
        if not os.path.exists(file_path):
            return []
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        return json_data
    

def get_argv(argv):
    start = 0
    end = 0
    try:
        opts, args = getopt.getopt(argv,"hs:e:n:",["start=","end=","num="])
    except getopt.GetoptError:
      print('download.py -s <start course id> -e <end course id> -n <single course id num>')
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print('download.py -s <start course id> -e <end course id> -n <single course id num>')
         sys.exit()
      elif opt in ("-s", "--start"):
         start = arg
      elif opt in ("-e", "--end"):
         end = arg
      elif opt in ("-n", "--num"):
         start = end = arg
    if start == 0 or end == 0:
        print('Error!, start course id or end course id incorrect')
        sys.exit()
    return int(start), int(end)

if __name__ == "__main__":
    start, end = get_argv(sys.argv[1:])
    #print(start, end, type(start))
    base_path = "./files"
    downloader = Downloader()
    for course_id in range(start, end + 1):
        json_data = downloader.get_json_data("./json/{}.json".format(course_id))
        #check if success
        for data in json_data:
            file_path = "{}/{}".format(base_path, course_id)
            #check file_path, if not exists , create.
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            file_name = "{}/{}".format(file_path, data["file_name"]) 
            print(file_name)
            #check file_name, if exists continue.
            if os.path.exists(file_name):
                print(file_name, "exists, skip...")
                continue

            downloader.download_file({"video_url": data["video_url"], "file_name": file_name, "referer": data["referer"]})
            time.sleep(2)
            #break
        print(course_id, "....Done.")
        #break
    print("All Done.")