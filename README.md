# InstaLoad
InstaLoad (Instagram + Download) is an app that downloads all images and videos from your Instagram profile.

This programs allows users to log in and download their Instagram posts. If your account is public, you don't have to log in at all. It uses Selenium web drivers (PhantomJS) and BeautifulSoup to scrape all the links of images and videos which are then downloaded using the requests module.
_____

Instructions:

Program is pretty straight forward to use. Log in (if you need to), enter the username that you want to download from, program searches through all posts, including the albums, and creates a dir named after the username, in which you get Images and Videos folder, where images and videos get downloaded respectively. All posts are downloaded sequentially and are given a number, "1" being the latest image/video posted. All images and videos in albums are seperated and downloaded individually as well into the respective folders.
This program only saves images and videos. No tags, captions, hastags, etc. are saved.

The app (InstaLoad.exe) was created using cx_freeze. If you just want to use the app, download the App folder as a zip file containing all the librarires, extract all files, then run InstaLoad.exe, the app with the purple icon. If you want to see and use the code, all of it was written in python and can be seen/downloaded in the Source folder.

Caveat:

Since this program doesn't use the Instagram API, but instead uses Selenium, it just automates the web browsing. This process is slow since Instagram requires a lot of JS and Ajax to be loaded. This program was tested and got an average download rate of 10-12 posts per min. The benefit of this script is that it can run in the background, so you can minimize and leave it running in the background.

Disclaimer:

Please follow all Instagram rules and guidelines. It is not recommended to download other people's content without their permission, especially if their account is set to private.

