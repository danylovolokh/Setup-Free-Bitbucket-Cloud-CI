import json
import os
import sys
import Utils

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
    global build_info_json_filepath, \
        build_number, \
        build_date, \
        previous_build_tag, \
        repo_url, \
        git_branch, \
        application_version, \
        application_name, \
        previous_build_date, \
        build_tag, \
        current_branch, \
        date

    build_info = Utils.get_build_info()

    build_info_json_filepath  = build_info.build_info_json_filepath
    current_branch            = build_info.current_branch
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

    # 2. Change build.gradle
    change_build_version_name_and_version_code()

    sys.stdout.flush()

    print ("<< main")
    return

if __name__ == '__main__':
    main(sys.argv)