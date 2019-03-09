import subprocess
import sys
import Utils

current_branch = ""

# >> fields from build_info.json
build_number = ""
application_version = ""
application_name = ""
build_tag = ""
# << fields from build_info.json

def tag_branch():
    print(">> tag_branch gitTag [%s]" % build_tag)

    sys.stdout.flush()

    msg = "[%s] tag [%s] build [%s] at branch [%s]" % (application_name, build_tag, build_number, current_branch)

    git_tag_execute = ["git", "tag", "-a", "-f", "-m", msg, build_tag]

    error_message = "git tag failed"
    execute_command(error_message, git_tag_execute)

    print("<< tag_branch")
    return

def commit_build_info_json():
    print (">> commit_build_info_json")

    filename = "build_info.json"

    git_add = ["git", "add", filename]
    error_message = "git add %s failed" % filename

    execute_command(error_message, git_add)

    commit_message = "%s version %s at branch '%s' build updated to %s" % (application_name, application_version, current_branch, build_number)
    git_commit = ["git", "commit", "-m", commit_message, filename]
    error_message = "git commit %s failed" % filename

    execute_command(error_message, git_commit)

    print ("<< commit_build_info_json")


def execute_command(error_message, git_commit):
    try:

        codeproc = subprocess.Popen(git_commit, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = codeproc.stdout.read().decode("utf-8").strip()
        print(result)

    except Exception as e:
        print(error_message)
        print(e)
        sys.stdout.flush()
        sys.exit(1)


def push_changes():
    print(">> push_changes")

    print("push_changes, pushing")
    git_push_exec = ["git", "push"]
    error_message = "git push failed"
    execute_command(error_message, git_push_exec)

    print("push_changes, pushing up tag")
    git_push_tag_exec = ["git", "push", "origin", build_tag]
    error_message = "git push tag failed"
    execute_command(error_message, git_push_tag_exec)

    print("push_changes, force pushing")
    git_exec_push_force = ["git", "push", "--force"]
    error_message = "git push --force failed"
    execute_command(error_message, git_exec_push_force)

    print("<< push_changes")


def main(argv):
    print (">> main")

    sys.stdout.flush()
    global build_number, \
        application_version, \
        application_name, \
        build_tag, \
        date

    sys.stdout.flush()

    build_info = Utils.get_build_info()

    date                      = build_info.date

    build_number              = build_info.build_number
    application_version       = build_info.application_version
    application_name          = build_info.application_name
    build_tag                 = build_info.build_tag

    commit_build_info_json()

    tag_branch()

    push_changes()

    sys.stdout.flush()

    print ("<< main")
    return

if __name__ == '__main__':
    main(sys.argv)