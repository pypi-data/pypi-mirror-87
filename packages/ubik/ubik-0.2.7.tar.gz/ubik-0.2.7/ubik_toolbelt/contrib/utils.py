# coding: utf-8
import os
import pwd
import grp
import hashlib

def user_exists(user):
    try:
        pwd.getpwnam(user)
        return True
    except KeyError:
        return False

def group_exists(group):
    try:
        grp.getgrnam(group)
        return True
    except KeyError:
        return False

def get_user_name():
    return pwd.getpwuid(os.getuid()).pw_name

def get_user_group():
    return grp.getgrgid(pwd.getpwuid(os.getuid()).pw_gid).gr_name

def which(file):
    for path in os.environ["PATH"].split(":"):
        if file in os.listdir(path):
            return "%s/%s" % (path, file)
    return False

def get_md5(file, block_size=2**20):
    md5 = hashlib.md5()
    _file = open(file, 'rb')
    while True:
        data = _file.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()
