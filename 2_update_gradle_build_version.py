import json
import os
import sys

build_info_json_filepath = ""

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

def change_build_version_name_and_version_code():
    # Read in the file
    with open('build.gradle', 'r') as file:
        file_data = file.read()

    new_version_name = application_version + '.' + build_number
    print("change_build_version_name_and_version_code, new versionCode [" + build_number + "]")
    print("change_build_version_name_and_version_code, new version name [" + new_version_name + "]")

    # Replace the target string
    file_data = file_data.replace('9999', build_number)
    file_data = file_data.replace('debugApplication', new_version_name)
    # Write the file out again
    with open('build.gradle', 'w') as file:
        file.write(file_data)

def main(argv):
    print (">> main")

    sys.stdout.flush()

    # 1. Parse data in build_info.json
    parse_build_info()

    # 2. Change build.gradle
    change_build_version_name_and_version_code()

    sys.stdout.flush()

    print ("<< main")
    return

if __name__ == '__main__':
    main(sys.argv)