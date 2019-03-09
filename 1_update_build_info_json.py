import os
import sys
import time
import Utils

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

    print(">> update_build_number, old build_number [%s]" % build_number)
    build_number = str(int(build_number) + 1)
    print("update_build_number, new build_number %s" % build_number)

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

def main(argv):
  print (">> main")

  global build_number, \
      build_date, \
      previous_build_tag, \
      repo_url, \
      git_branch, \
      application_version, \
      application_name, \
      previous_build_date, \
      build_tag, \
      date

  sys.stdout.flush()

  build_info = Utils.get_build_info()

  date                      = build_info.date

# >> fields from build_info.json
  build_number              = build_info.build_number
  build_date                = build_info.build_date
  previous_build_tag        = build_info.previous_build_tag
  repo_url                  = build_info.repo_url
  git_branch                = build_info.git_branch
  application_version       = build_info.application_version
  application_name          = build_info.application_name
  previous_build_date       = build_info.previous_build_date
  build_tag                 = build_info.build_tag

  # 3.
  update_build_info_json()

  sys.stdout.flush()

  print ("<< main")
  return

if __name__ == '__main__':
  main(sys.argv)
