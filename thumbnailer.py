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


def make_thumbnails(cur_process, userpath, board=None):
    """ crawl userpaths for thumbnails to make """
    if board is None:
        print "%s - %s: Current Directory is %s" % (cur_process, get_logtime(), userpath)
        thumbdir = os.path.join(userpath, "thumbs")

        if not os.path.isdir(thumbdir):  # check if thumbdir exists
            os.mkdir(thumbdir)  # make thumbdir
            print "%s - %s: Thumbnail directory created at %s" % (
                cur_process, get_logtime(), thumbdir)
        else:
            pass
        imagepath = os.path.join(userpath, "images")
    else:
        print board
        thumbdir = os.path.join(userpath, "thumbs", board)

        if not os.path.isdir(thumbdir):  # check if thumbdir exists
            os.mkdir(thumbdir)  # make thumbdir
            print "%s - %s: Thumbnail directory created at %s" % (
                cur_process, get_logtime(), thumbdir)
        else:
            pass
        imagepath = os.path.join(userpath, "images", board)

    cur_image_list = [f for f in os.listdir(imagepath) if os.path.isfile(os.path.join(imagepath, f)) and f.endswith(('.jpg', '.jpeg', '.png')) and not f.startswith('.')]

    for image in cur_image_list:
        make_thumbnail(cur_process, imagepath, thumbdir, image)



def thumbnailcrawler():
    """ Crawl for images without thumbnails? """
    while True:
        # Get list of all user directories
        user_directories = [f for f in os.listdir(users_dir) if os.path.isdir(
            os.path.join(users_dir, f)) is True and f not in ("thumbs", "css", "js", "img")]

        for user in user_directories:
            absolute_user_path = os.path.join(users_dir, user)

            # Make thumbnails for all the root directory images
            make_thumbnails("Thumbnail Crawler", absolute_user_path)

            # Get a list of the user's directories ("boards")
            user_board_list = [f for f in os.listdir(
                os.path.join(absolute_user_path, "images")
                ) if os.path.isdir(os.path.join(
                    absolute_user_path, "images", f)
                ) is True and f not in ("thumbs", "css", "js", "img")]

            print "%s - Thumbnail Crawler: Boards in %s are: %s" % (
                get_logtime(), absolute_user_path, user_board_list)

            # Make thumbnails for images in boards
            for board in user_board_list:
                make_thumbnails("Thumbnail Crawler", absolute_user_path, board)

        # Sleep for two minutes
        time.sleep(120)


if __name__ == "__main__":

    print "Moodboard Upload Server 0.3"

    HEIGHT = 350
    DATABASE = 'moodboard.db'
    users_dir = ""
    THUMBNAILQ = multiprocessing.Queue()

    if thumbnailcrawlerswitch == 1:
        print "Start Thumbnail Crawler"
        crawlerprocess = multiprocessing.Process(target=thumbnailcrawler)
        crawlerprocess.start()
    else:
        print("Thumbnailer disabled")
