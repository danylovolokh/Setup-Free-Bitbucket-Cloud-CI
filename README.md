# How to setup a Free CI for Android project based on bitbucket cloud pipelines.

This project is created as a "manual" for setting up a FREE CI (continious Intergation) based on [bitbucket pipelines](https://bitbucket.org/product/features/pipelines)

At the time of writting (10.03.2019) **bitbucket cloud offers you a free 50 build minutes** to get started with Pipelines. 

# Steps build a version with CI server
1. Update build number, build version name etc...
2. Update build.gradle
3. Commit
4. Collect change log
5. Build the application
6. Upload the apk files to the storage for future usage.

## 1. Update build number, build version name etc...
We will use a separate file to keep the build history: build_info.json

> ##### The file *build_info.json* is located in the root of this repository

Example:
```
{
"build_number":"13",
"build_date":"2019-03-10 09:36",
"previous_build_date":"2019-03-10 09:16",
"application_name":"SetupBitbucketCloudCI",
"application_version":"1.0",
"build_tag":"SetupBitbucketCloudCI/1.0/13",
"previous_build_tag":"SetupBitbucketCloudCI/1.0/12",
"repo_url":"ssh://git@bitbucket.org:DanyloVolokh/setupbitbucketcloudci.git",
"git_branch":"master"
}
```
- **build_number**        - this value is a build number
- **build_date**          - date, when this build was created
- **previous_build_date** - the date of previous build
- **application_name**    - name of the application
- **application_version** - version of the application which will be added to the build.gradle file
- **build_tag**           - a tag name which will be added to the repository when build is created
- **previous_build_tag**  - a tag which was added when previoud build was created 
- **repo_url**            - link to the repository
- **git_branch**          -  branch on which the build is happening

In order to update the *build_info.json* we need to execute python script *1_update_build_info_json.py*

> ##### The file *1_update_build_info_json.py* is located in the root of this repository

This script does the following changes to the *build_info.json*:
- increments build_number
- changes build_date to the current date
- updates previous build date
- updates build tag
- updates previous build tag

## 2. Update build.gradle

In order to update build.gradle file of the app module I've added a few changes to the root build.gradle
