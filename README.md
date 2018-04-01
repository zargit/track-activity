# track-activity

“Web Crawler Project”

Author: Abdullah Ahmad Zarir


Read Me
------------
This software is able to fetch and show articles / tweets from different websites in the Internet about one or more topic(s) of reader’s interest.

1. User Guide:

1a. Setup

After cloning the repository, python dependencies must be installed in local machine using following command:

      pip install -r requirements.txt

Next, the chromedriver needs to be setup with below instructions:

https://sites.google.com/a/chromium.org/chromedriver/home 
https://gist.github.com/ziadoz/3e8ab7e944d02fe872c3454d17af31a5 (for ubuntu)

Next, the Flask server inside the app directory should be started. By default it listens on port 3000. So visiting localhost:3000 should bring the site.

For a live demo you can visit this URL: zarir.me/track/


1b. User Interaction:

Step 1 -  Adding a Profile: This allows the user to add a topic of interest.








Step 2 - Adding a Source: This allows the user to mention the source website for a selected profile. For example, getting tweets from Mark Zuckerberg’s Twitter account involves following steps:



  






[You can leave ‘keyword’ to be empty for tweets]



[Selecting Mark Zuckerberg in the UI dropdown will now fetch his tweets]



For adding CNN news articles, corresponding source selector is “.cd__headline”. User can mention one or more keywords (screenshot #7)



2. Software Architecture:
----------------------------------

2a. General Structure:

It’s a web application where the front-end is written mostly with Reactjs, a javascript view framework. The backend server code is written with Flask, a python framework for webapps. 

Python based selenium framework is used to perform most of the web scraping.

For basic data storage capabilities, simple json files were kept in the server-side.


2b. Internals:

All the requests from the Web UI goes to the Flask server.

Depending on the request parameters, Flask routes those to the appropriate handlers. 

After receiving the UI request, the heavy-lifting task of ‘crawling’ happens in the server using Selenium framework. 

The application utilizes a headless chrome browser to dynamically load the webpage content and then retrieves the content of that page. 

After that it is simple DOM traversal to find the exact elements those are needed to show in the UI.  
