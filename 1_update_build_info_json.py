import json
import os
import subprocess
import sys
import time

build_info_json_filepath = ""
current_branch = ""
date = ""

# >> field from build_info.json
build_number = ""
build_date = ""
previous_build_tag = ""
repo_url = ""
git_branch = ""
application_version = ""
application_name = ""
previous_build_date = ""
build_tag = ""
# << field from build_info.json


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


def update_build_info_json():
  print(">> update_build_info_json")
  sys.stdout.flush()
  filename = "build_info.json"
  print("update_build_info_json, absolute path [%s]" % os.path.abspath(filename))
  sys.stdout.flush()

  if os.path.exists(filename):
      print ("update_build_info_json, %s does exist" % filename)

      update_build_number()
      update_build_date()
      update_build_tag()

      write_build_info_json()

  else:
      print ("update_build_info_json, %s does not exist" % filename)
      sys.stdout.flush()
      sys.exit(1)

  print("<< update_build_info_json")
  return


def write_build_info_json():
    print(">> write_build_info_json")

    build_info = "{\n"
    build_info += "\"build_number\":\"%s\",\n" % build_number
    build_info += "\"build_date\":\"%s\",\n" % build_date
    build_info += "\"previous_build_date\":\"%s\",\n" % previous_build_date
    build_info += "\"application_name\":\"%s\",\n" % application_name
    build_info += "\"application_version\":\"%s\",\n" % application_version
    build_info += "\"build_tag\":\"%s\",\n" % build_tag
    build_info += "\"previous_build_tag\":\"%s\",\n" % previous_build_tag
    build_info += "\"repo_url\":\"%s\",\n" % repo_url
    build_info += "\"git_branch\":\"%s\"\n" % git_branch
    build_info += "}"

    print("write_build_info_json, build_info %s" %build_info)

    build_info_file_path = "build_info.json"
    build_info_file = open(build_info_file_path, 'w')
    build_info_file.write(build_info)
    build_info_file.flush()
    build_info_file.close()
    print("<< write_build_info_json")

def update_build_date():
    global \
        previous_build_date, \
        build_date, \
        date

    local_time = time.localtime(time.time())
    hour = str(local_time.tm_hour).zfill(2)
    min  = str(local_time.tm_min).zfill(2)

    previous_build_date = build_date

    build_date = "%s %s:%s" % (date, hour, min)

    print("update_build_date, build_date %s" % build_date)
    print("update_build_date, previous_build_date %s" % previous_build_date)

def update_build_tag():
    global \
        previous_build_tag, \
        build_tag

    previous_build_tag = build_tag
    build_tag = "%s/%s/%s" % (application_name, application_version, build_number)

    print("update_build_tag, previous_build_tag %s" % previous_build_tag)
    print("update_build_tag, build_tag %s" % build_tag)

def update_build_number():
    global build_number
    build_number = str(int(build_number) + 1)
    print("update_build_number, new build_number %s" % build_number)

# Creates the Git tag using the info prepared by prepareTag(), tags the Git repo
# using the tag, and then pushes the tag
def tag_branch():
  # os.chdir(gitRoot)
  print(">> tag_branch %s Git repo with %s" % (repoName, gitTag))
  sys.stdout.flush()

  gitExec = ["git", "tag", "-a", "-f", "-m"]
  msg = "%s tag %s build " % (repoName, gitPrefix)
  msg += "%s.%s number %s" % (gitLabel, current_branch, buildNumber)

  gitExec.append(msg)
  gitExec.append(gitTag)

  print("tag_branch, tagging")
  errorMessage = "git tag failed"
  callExec(gitExec, quiet=False, continuous=False, err=errorMessage, redirect="")

  print("tag_branch, pushing")
  gitExec = ["git", "push"]
  errorMessage = "git push failed"
  callExec(gitExec, quiet=False, continuous=False, err=errorMessage, redirect="")

  print("tag_branch, force pushing")
  gitExec = ["git", "push", "--force"]
  errorMessage = "git push --force failed"
  callExec(gitExec, quiet=False, continuous=False, err=errorMessage, redirect="")
  # os.chdir(root)
  print("<< tag_branch")
  return

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

# Start point
def main(argv):
  print (">> main")

  sys.stdout.flush()

  # 1. Parse data in build_info.json
  parse_build_info()

  # 2. Get current branch from git
  get_current_git_branch()

  # 3. Assign current date to "date" field
  set_current_date()

  # 3.
  update_build_info_json()

  sys.stdout.flush()

  print ("<< main")
  return

if __name__ == '__main__':
  main(sys.argv)
