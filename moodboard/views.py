from django.shortcuts import render
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
import sys

from .models import UserImage
from django.contrib.auth.models import User
# Then wherever, views or context processor
from moodboard import settings # See how we're not importing project's settings


MOODBOARD_USERS = '/home/christie/Sync/Programming/Python/Projects/moodboard_django/moodboard/static/moodboard/users/'


def list_files(cur_foldername, reverse=True):
    """ Return list of files of specified type """
    cur_foldername = cur_foldername.decode("utf8")
    output = []
    for f in os.listdir(cur_foldername):
        f = f.decode("utf8")
        if os.path.isfile(os.path.join(cur_foldername, f)) and f.endswith(('.jpg', '.jpeg', '.png')):
            output.append(f)
    
    # output = [f for f in os.listdir(cur_foldername) if os.path.isfile(os.path.join(cur_foldername, f)) and f.endswith(('.jpg', '.jpeg', '.png'))]

    if reverse is True:
        # Sort newFileList by date added(?)
        output.sort(key=lambda x: os.stat(os.path.join(cur_foldername, x)).st_mtime)
        output.reverse()  # reverse image list so new files are first
    else:
        pass

    return output


def list_folders(cur_folder):
    """ Return list of folders in given folder """
    return [f for f in os.listdir(cur_folder) if os.path.isdir(os.path.join(cur_folder, f)) == True and f not in ("thumbs", "css", "js", "img")]


""" START VIEWS """


def index(request):
    userlist = list_folders(MOODBOARD_USERS)
    print(userlist)

    new_users_list = []

    for user in userlist:
        images_path = os.path.join(MOODBOARD_USERS, user, "images")
        cur_image_list = list_files(images_path)

        if cur_image_list != []:
            new_users_list.append((user,
                                   os.path.join("moodboard/users", user,
                                                "images", cur_image_list[0]),
                                   len(cur_image_list)))
        else:
            pass

    if not request.user.is_authenticated():
        loggedin = False
    else:
        loggedin = True

    context = {'userslist': new_users_list, 'users_enabled': settings.USER_ACCOUNTS, 'loggedin': loggedin}

    # return HttpResponse(str(new_users_list))
    return render(request, 'moodboard/index.html', context)

# Create your views here.
def user(request, username, directory=""):
    if directory:
        isdir = True
        newimagelist = list_files(os.path.join(MOODBOARD_USERS, username, 'images', directory))
        imagelist = []
        for image in newimagelist:
            imagelist.append(os.path.join(MOODBOARD_USERS, username,'images', directory, image))
    else:
        isdir = False
        newimagelist = list_files(os.path.join(MOODBOARD_USERS, username, 'images'))
        imagelist = newimagelist
        # for image in newimagelist:
        #    imagelist.append("moodboard/users/%s/images/%s" % (username, image))


    # paginate the image list
    paginator = Paginator(imagelist, 20)

    # get page number from url ?page= 
    page = request.GET.get('page')
    try:
        pagedlist = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        pagedlist = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        pagedlist = paginator.page(paginator.num_pages)

    # find the next page number if there is one
    try:
        next_page = pagedlist.next_page_number()
    except EmptyPage:
        next_page = ""
    # find the previous page number if there is one
    try:
        previous_page = pagedlist.previous_page_number()
    except EmptyPage:
        previous_page = ""

    dirlist = list_folders(os.path.join(MOODBOARD_USERS, username, 'images'))

    if not request.user.is_authenticated():
        loggedin = False
    else:
        loggedin = True

    context = {'imagelist': pagedlist,
               'directory': directory,
               'dirlist': dirlist,
               'isdir': isdir,
               'has_next': pagedlist.has_next(),
               'next_page': next_page,
               'has_previous': pagedlist.has_previous(),
               'previous_page': previous_page,
               'numberofimages': len(imagelist),
               'username': username,
               'loggedin': loggedin
               }
    return render(request, 'moodboard/user.html', context)


def useraccount(request, username):
    context = {'username': username,
    'message': 'hello'}
    return render(request, 'moodboard/message.html', context)


def userdb(request, username, tag=""):

    # Check if the current user is loggedin
    if not request.user.is_authenticated():
        loggedin = False
    else:
        loggedin = True

    # Get username id from database then feed to image query
    user = User.objects.get(username=username)

    if tag:
        imagelist = UserImage.objects.filter(owner=user.id, tags__name=tag)
    else:
        imagelist = UserImage.objects.filter(owner=user.id)

    context = {'imagelist': imagelist,
               'loggedin': loggedin,
               'username': username,
               'user': user,
               'numberofimages': len(imagelist),
               'newtag': tag}

    return render(request, 'moodboard/userdb.html', context)

# USER REGISTER, LOGIN ETC


def register(request):
    if request.method == 'POST':
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return forms.HttpResponseRedirect("/books/")
    else:
        form = forms.UserCreationForm()
    return render(request, "moodboard/register.html", {
        'form': form,
    })


def logout(request):
    if request.user.is_authenticated():
        auth_logout(request)
        context = {"message": "Success \n User has been logged out"}
        return render(request, "moodboard/message.html", context)
    else:
        return HttpResponse("Failed <br> User was not logged in so could not be logged out")
