# How to setup a Free CI for Android project based on bitbucket cloud pipelines.

This project is created as a "manual" for setting up a FREE CI (continious Intergation) based on [bitbucket pipelines](https://bitbucket.org/product/features/pipelines)

At the time of writting (10.03.2019) **bitbucket cloud offers you a free 50 build minutes** to get started with Pipelines. 

# Steps build a version with CI server
1. Update build number, build version name etc...
2. Update build.gradle
3. Commit and push changes to the repository
4. Collect a change log
5. Build the application

Additional steps:

6. Sign the application with the "release" signing key.
7. Upload the apk files to the storage for future usage.
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

## 5. Build the application
Now we are ready to build a "debug" version with bitbucket CI.
In order to build the "debug" version we need to call "./gradlew assembleDebug"

# Setup Bitbucket pipelines.
References:
- [Get started with Bitbucket Pipelines](https://confluence.atlassian.com/bitbucket/get-started-with-bitbucket-pipelines-792298921.html) 
- [Configure bitbucket-pipelines.yml](https://confluence.atlassian.com/bitbucket/configure-bitbucket-pipelines-yml-792298910.html)

In order to setup bitbucket pipelines you need to add *bitbucket-pipelines.yml* file to the root of the project.
```
pipelines:
  custom:
    manual_configuration:
      - step:
          name: Build a version
          image: java:8
          caches:
            - gradle
            - android-sdk
            - pip
          script:

            # Download and unzip android sdk
            - wget --quiet --output-document=android-sdk.zip https://dl.google.com/android/repository/sdk-tools-linux-3859397.zip
            - unzip -o -qq android-sdk.zip -d android-sdk

            # Define Android Home and add PATHs
            - export ANDROID_HOME="/opt/atlassian/pipelines/agent/build/android-sdk"
            - export PATH="$ANDROID_HOME/tools:$ANDROID_HOME/tools/bin:$ANDROID_HOME/platform-tools:$PATH"

            # Download packages.
            - yes | sdkmanager "platform-tools"
            - yes | sdkmanager "platforms;android-27"
            - yes | sdkmanager "build-tools;27.0.3"
            - yes | sdkmanager "extras;android;m2repository"
            - yes | sdkmanager "extras;google;m2repository"
            - yes | sdkmanager "extras;google;instantapps"
            - yes | sdkmanager --licenses

            # Install python
            - echo "Install python"
            - apt-get update
            - apt-get install python-pip -q -y

            # Give write access
            - chmod a+x ./gradlew

            # Clean the project
            - ./gradlew clean

            # Setup correct origin url
            - git config -e
            - git config --global user.email "v.danylo@gmail.com"
            - git config --global user.name "Danylo Volokh Pipeline"
            - git config remote.origin.url https://$BITBUCKET_USER:$BITBUCKET_PASS@bitbucket.org/$BITBUCKET_ACCOUNT/$GIT_REPO_NAME.git

            # Change build version
            - echo "Update info json"
            - python 1_update_build_info_json.py

            # Update application version in gradle file
            - echo "Change build version"
            - python 2_update_gradle_build_version.py

            # Change build version after successful build
            - echo "Commit build version"
            - python 3_commit_build_version.py

            # Collect change log
            - echo "Collect change log"
            - python 4_collect_change_log.py

            # Build apk
            - ./gradlew assembleDebug

definitions:
    caches:
      android-sdk: android-sdk
```

Then you have to "Enable Bitbucket in the Settings of your account.
![alt tag](https://user-images.githubusercontent.com/2686355/54084947-8df32180-4340-11e9-9991-8133f939394a.gif)

You also need to add a few variables to the Pipelines variables
- BITBUCKET_USER - user which has access to write to the master branch
- BITBUCKET_PASS - pasword to this user (password will be encrypted and hidden from everyone else)
- BITBUCKET_ACCOUNT - account on which the repository is stored
- GIT_REPO_NAME - name of the repository

![alt tag](https://user-images.githubusercontent.com/2686355/54085140-00650100-4343-11e9-8e1a-f60a952f41b7.png)

## Now you are ready to build the "debug" version with Bitbucket Pipelines
