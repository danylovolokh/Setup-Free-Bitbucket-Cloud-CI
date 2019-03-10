# How to setup a Free CI for Android project based on bitbucket cloud pipelines.

This project is created as a "manual" for setting up a FREE CI (continious Intergation) based on [bitbucket pipelines](https://bitbucket.org/product/features/pipelines)

At the time of writting (10.03.2019) **bitbucket cloud offers you a free 50 build minutes** to get started with Pipelines. 

# Steps build a version with CI server
1. Update build number, build version name etc...
2. Update build.gradle
3. Commit and push changes to the repository
4. Collect a change log
5. Build the application
6. Upload the apk files to the storage for future usage.

Additional steps:

7. Sign the application with the "release" signing key.
8. Upload a version to the Fabric Beta for testing purposes.

## 1. Update build number, build version name etc...
We will use a separate file to keep the build history: build_info.json

> ##### The file *build_info.json* is located in the root of the project.

Example:
```javascript
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

### To update the *build_info.json* we need to execute python script *1_update_build_info_json.py*

> ##### The file *1_update_build_info_json.py* is located in the root of the project.

This script does the following changes to the *build_info.json*:
- increments build_number
- changes build_date to the current date
- updates previous build date
- updates build tag
- updates previous build tag

## 2. Update build.gradle

In order to update build.gradle file of the app module I've added a few changes to the root build.gradle. 

Add the following piece of code to the *build.gradle* in the root of the project.
> ##### The file *build.gradle* is located in the root of the project.
```
ext {
    versionCodeValue = 9999
    versionNameValue = "debugApplication"
}
```
You also need to change the *build.gradle* in the app module.
> ##### The file *build.gradle* is located in the "app" folder of the project.
```
   defaultConfig {
        ...
        versionName versionNameValue
        versionCode versionCodeValue
        ...
    }
``` 
    

### To update *versionNameValue* and *versionCode* in the *build.gradle* we need to execute python script *2_update_gradle_build_version.py*

> ##### The file *2_update_gradle_build_version.py* is located in the root of the project.

This script takes the "*application_name*" and "*application_version*" from *build_info.json*, creates a *versionNameValue*  and adds it to the *build.gradle* which is located in the root of the project. And values in the root of the project are used as *versionName* and *versionCode* in the *build.gradle* of the app module.

> ##### versionNameValue = application_version + '.' + build_number
> ##### versionCodeValue = build_number

## 3. Commit and push changes to the repository
### To commit the changes to build_info.json we need to execute python script *3_commit_build_version.py*
Please note: we do not commit "build.gradle" files. We only modify the *build_info.json*

## 4. Collect a change log
### To collect the change log we need to execute python script *4_collect_change_log.py*

Change contains all the commit messages from the commits between this build and the previous build.

In this project we create a separate change log files for every flavor of the application. Then these separate change logs can be used as a "Release Notes" when we upload different versions to the Fabric. Because the only way to distinguish "flavors" in Fabric Beta "Release notes" is to have different release notes, we create separate change log files for each flavor.

After you run *4_collect_change_log.py* 2 new files will be created in the root of the project:
- change_log_external.txt
- change_log_internal.txt

Change log is collected between the "*build_tag*" and "*previous_build_tag*".
Example of the *change_log_external.txt*
```
External

"Added how to commit changes"
"Added how to update build.gradle file"
"Added initial Readme file"
"Fix files that were committed by mistake"
"Update upload to Downloads"
```
