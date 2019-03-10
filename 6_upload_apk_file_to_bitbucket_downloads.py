import os
import subprocess
import sys
import Utils


# >> fields from build_info.json
build_number = ""
application_version = ""
# << fields from build_info.json

def execute_command(error_message, command):
    print ("execute_command curl [%s]" % command)
    try:

        codeproc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

    global build_number, \
        application_version

    sys.stdout.flush()

    build_info = Utils.get_build_info()

    build_number              = build_info.build_number
    application_version       = build_info.application_version

    version_name = application_version + "_" + application_version.replace(".", "_")
    print ("version_name %s" % version_name)

    final_version_name = version_name + "_" + build_number
    print ("final_version_name %s" % final_version_name)

    os.rename('app/build/outputs/apk/external/release/app-external-release.apk', 'app/build/outputs/apk/external/release/%s_external.apk' % final_version_name)
    os.rename('app/build/outputs/apk/internal/release/app-internal-release.apk', 'app/build/outputs/apk/internal/release/%s_internal.apk' % final_version_name)

    print ("final_version_name [%s]" % final_version_name)

    BB_AUTH_STRING = os.environ.get('BB_AUTH_STRING')
    BITBUCKET_REPO_OWNER = os.environ.get('BITBUCKET_REPO_OWNER')
    BITBUCKET_REPO_SLUG = os.environ.get('BITBUCKET_REPO_SLUG')

    downloads__url = "https://%s@api.bitbucket.org/2.0/repositories/%s/%s/downloads" % (BB_AUTH_STRING, BITBUCKET_REPO_OWNER, BITBUCKET_REPO_SLUG)
    filepath_external = 'app/build/outputs/apk/external/release/%s_external.apk' % final_version_name
    filepath_internal = 'app/build/outputs/apk/internal/release/%s_internal.apk' % final_version_name

    print (">> execute_command curl filepath_external")

    curl_exec = ["curl", "-X", "POST", downloads__url, "--form", "files=@%s" % filepath_external]
    execute_command("failed to upload", curl_exec)

    print (">> execute_command curl filepath_internal")

    curl_exec = ["curl", "-X", "POST", downloads__url, "--form", "files=@%s" % filepath_internal]
    execute_command("failed to upload", curl_exec)

    sys.stdout.flush()

    print ("<< main")
    return

if __name__ == '__main__':
    main(sys.argv)