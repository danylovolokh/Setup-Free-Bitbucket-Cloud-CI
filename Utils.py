import os
import sys
import json
import subprocess
import time

build_info_json_filepath = ""
current_branch = ""
date = ""

# >> fields from build_info.json
build_number = ""
build_date = ""
previous_build_tag = ""
repo_url = ""
git_branch = ""
application_version = ""
application_name = ""
previous_build_date = ""
build_tag = ""

def check_not_empty(var, var_name):
    try:
        assert(var != "")
    except:
        print("check_info, %s is empty" % var_name)
        sys.stdout.flush()
        sys.exit(1)
    return

def parse_build_info():
    print (">> parse_build_info")

    global build_info_json_filepath
    global \
        build_number, \
        build_date, \
        previous_build_tag, \
        repo_url, \
        git_branch, \
        application_version, \
        application_name, \
        previous_build_date, \
        build_tag

    build_info_json_filepath = os.path.join("build_info.json")

    print ("parse_build_info, Getting git configuration from %s" %build_info_json_filepath)

    if not os.path.exists(build_info_json_filepath):
        print("parse_build_info, %s does not exist" % build_info_json_filepath)
        sys.stdout.flush()
        sys.exit(1)

    try:
        f = open(build_info_json_filepath, 'r')
        configFileJson = json.load(f)
    except Exception as e:
        print("parse_build_info, json.load failed %s" % e)
        f.close()
        sys.stdout.flush()
        sys.exit(1)

    f.close()

    build_number           = configFileJson["build_number"]
    build_date             = configFileJson["build_date"]
    previous_build_tag     = configFileJson["previous_build_tag"]
    repo_url               = configFileJson["repo_url"]
    git_branch             = configFileJson["git_branch"]
    application_version    = configFileJson["application_version"]
    application_name       = configFileJson["application_name"]
    previous_build_date    = configFileJson["previous_build_date"]
    build_tag              = configFileJson["build_tag"]


    print("build_number           = %s" % build_number)
    print("build_date             = %s" % build_date)
    print("previous_build_date    = %s" % previous_build_date)
    print("repo_url               = %s" % repo_url)
    print("git_branch             = %s" % git_branch)
    print("application_version    = %s" % application_version)
    print("application_name       = %s" % application_name)
    print("build_tag              = %s" % build_tag)
    print("previous_build_tag     = %s" % previous_build_tag)

    check_not_empty(build_number, "build_number")
    check_not_empty(build_date, "build_date")
    check_not_empty(repo_url, "repo_url")
    check_not_empty(git_branch, "git_branch")
    check_not_empty(application_version, "application_version")
    check_not_empty(application_name, "application_name")
    check_not_empty(build_tag, "build_tag")
    check_not_empty(previous_build_tag, "previous_build_tag")

    print ("<< parse_build_info")
    return

def get_current_git_branch():
    global current_branch

    print(">> get_current_git_branch")
    sys.stdout.flush()

    git_get_current_branch = ["git", "symbolic-ref", "--short", "HEAD"]

    try:

        codeproc = subprocess.Popen(git_get_current_branch, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        current_branch = codeproc.stdout.read().decode("utf-8").strip()

    except Exception as e:
        print("git symbolic-ref --short HEAD failed")
        print(e)
        sys.stdout.flush()
        sys.exit(1)

    sys.stdout.flush()

    print("<< get_current_git_branch, currentBranch: [%s]" % current_branch)
    return

def set_current_date():
    print(">> set_current_date")
    global date

    temp = time.localtime()
    year = str(temp.tm_year)
    month = str(temp.tm_mon).zfill(2)
    day = str(temp.tm_mday).zfill(2)
    date = ("%s-%s-%s" % (year, month, day))

    print("<< set_current_date %s" % date)
    sys.stdout.flush()

def get_build_info():

    build_info = BuildInfo()

    parse_build_info()

    get_current_git_branch()

    set_current_date()

    build_info.build_info_json_filepath = build_info_json_filepath
    build_info.current_branch = current_branch
    build_info.date = date

    build_info.build_number         = build_number
    build_info.build_date           = build_date
    build_info.previous_build_tag   = previous_build_tag
    build_info.repo_url             = repo_url
    build_info.git_branch           = git_branch
    build_info.application_version  = application_version
    build_info.application_name     = application_name
    build_info.previous_build_date  = previous_build_date
    build_info.build_tag            = build_tag

    return build_info

class BuildInfo:
    def __init__(self):
        pass

    build_info_json_filepath = ""
    current_branch = ""
    date = ""

    # >> fields from build_info.json
    build_number = ""
    build_date = ""
    previous_build_tag = ""
    repo_url = ""
    git_branch = ""
    application_version = ""
    application_name = ""
    previous_build_date = ""
    build_tag = ""
    # << fields from build_info.json
