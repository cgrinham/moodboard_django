#! /usr/bin/python
""" 
moodboard Upload Server
Copyright Christie Grinham 2014
christiegrinham@gmail.com

 """

import sys
import os
from datetime import datetime
import multiprocessing
import time
from PIL import Image

thumbnailcrawlerswitch = 1


# Listing
def get_logtime():
    """ Return the date and time """
    return datetime.now().strftime('%Y/%m/%d %H:%M')


def list_files(cur_foldername, reverse):
    """ Return list of files of specified type """
    output = [f for f in os.listdir(cur_foldername) if os.path.isfile(
        os.path.join(cur_foldername, f)) and f.endswith(
        ('.jpg', '.jpeg', '.png')) and not f.startswith('.')]

    if reverse == True:
        # Sort newFileList by date added(?)
        output.sort(key=lambda x: os.stat(os.path.join(cur_foldername, x)).st_mtime)
        output.reverse() # reverse image list so new files are first
    else:
        pass

    return output

def list_folders(cur_folder):
    """ Return list of folders in given folder """
    return [f for f in os.listdir(cur_folder) if os.path.isdir(os.path.join(cur_folder, f)) == True and f not in ("thumbs", "css", "js", "img")]


def make_thumbnail(cur_process, folder, thumbdir, image):
    """ Make the actual thumbnail """
    #print "%s - %s: Make thumbnail %s in thumbdir %s" % (get_logtime(), cur_process, image, thumbdir)
    if not os.path.exists(os.path.join(thumbdir, image)): #if thumbnail doesn't exist
        imagepath = os.path.join(folder, image)
        print "%s - %s: PIL - File to open is: %s"  % (get_logtime(), cur_process, imagepath)
        try:
            
            img = Image.open(imagepath).convert('RGB') # open and convert to RGB

            hpercent = (float(HEIGHT) / float(img.size[1])) # find ratio of new height to old height
            wsize = int(float(img.size[0]) * hpercent) # apply ratio to create new width
            img = img.resize((int(wsize), int(HEIGHT)), Image.ANTIALIAS) # resize image with antialiasing
            img.save(os.path.join(thumbdir, image), format='JPEG', quality=90) # save with quality of 80, optimise setting caused crash
            print "%s - %s: Sucessfully resized: %s \n" % (get_logtime(), cur_process, image)
        except IOError:
            print "%s - %s: IO Error. %s will be deleted and downloaded properly next sync" % (get_logtime(), cur_process, imagepath)
            os.remove(imagepath)
    else:
        #print "%s - %s: Thumbnail for %s exists \n" % (get_logtime(), cur_process, image)
        pass


def make_thumbnails(cur_process, folder):
    """ crawl folders for thumbnails to make """
    print "%s - %s: Current Directory is %s" % (cur_process, get_logtime(), folder)
    #thumbdir = os.path.join(folder, ".moodthumbs")
    thumbdir = "/var/www/moodboard/moodboard/static/moodboard/users/inpala/thumbs"

    if not os.path.isdir(thumbdir): # check if thumbdir exists
        os.mkdir(thumbdir) # make thumbdir
        print "%s - %s: Thumbnail directory created at %s" % (cur_process, get_logtime(), thumbdir)
    else:
        pass

    cur_image_list = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and f.endswith(('.jpg', '.jpeg', '.png')) and not f.startswith('.')]

    for image in cur_image_list:
        make_thumbnail(cur_process, folder, thumbdir, image)

def thumbnailcrawler():
    """ Crawl for images without thumbnails? """
    while True:
        userfolderlist = [f for f in os.listdir(USERSFOLDER) if os.path.isdir(os.path.join(USERSFOLDER, f)) == True and f not in ("thumbs", "css", "js", "img")]

        for folder in userfolderlist:
            abs_folder = os.path.join(USERSFOLDER, folder, "images")

            make_thumbnails("Thumbnail Crawler", abs_folder)

            subfolderlist = [f for f in os.listdir(abs_folder) if os.path.isdir(os.path.join(abs_folder, f)) == True and f not in ("thumbs", "css", "js", "img")]

            print "%s - Thumbnail Crawler: Subfolders in %s are: %s" % (get_logtime(), abs_folder, subfolderlist)

            for subfolder in subfolderlist:
                make_thumbnails("Thumbnail Crawler", os.path.join(abs_folder, subfolder))

        # Sleep for two minutes
        time.sleep(120)

if __name__ == "__main__":

    print "Moodboard Upload Server 0.3"

    HEIGHT = 350
    DATABASE = 'moodboard.db'
    USERSFOLDER = "/var/www/moodboard/moodboard/static/moodboard/users"
    THUMBNAILQ = multiprocessing.Queue()

    if thumbnailcrawlerswitch == 1:
        print "Start Thumbnail Crawler"
        crawlerprocess = multiprocessing.Process(target=thumbnailcrawler)
        crawlerprocess.start()
    else:
        print("Thumbnailer disabled")
