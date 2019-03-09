import subprocess
import sys
import Utils

# >> fields from build_info.json
previous_build_tag = ""
build_tag = ""
# << fields from build_info.json

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


def main(argv):
    print (">> main")

    sys.stdout.flush()

    global previous_build_tag, \
        build_tag

    sys.stdout.flush()

    build_info = Utils.get_build_info()

    previous_build_tag        = build_info.previous_build_tag
    build_tag                 = build_info.build_tag

    # Example: "git log --pretty=format:"%s" SetupBitbucketCloudCI/1.0/2..SetupBitbucketCloudCI/1.0/3~1"
    git_change_log = ["git", "log", "--pretty=format:\"%s\"", "%s..%s~1" %(previous_build_tag, build_tag)]

    code_proc = subprocess.Popen(git_change_log, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output_text = code_proc.stdout.read().decode("utf-8").strip()

    external_file_name = "change_log_external.txt"

    with open(external_file_name, "w+") as output:
        output.write("External\n\n")
        output.write(output_text)
        output.close()

    internal_file_name = "change_log_internal.txt"
    with open(internal_file_name, "w+") as output:
        output.write("Internal\n\n")
        output.write(output_text)
        output.close()

    sys.stdout.flush()

    print ("<< main")
    return

if __name__ == '__main__':
    main(sys.argv)