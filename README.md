# Twitter Full Archive Search Script
## About
This is a python script for searching for tweets containing a particular keyword, hashtag, or mention using [Twitter's Full-Archive Search API](https://developer.twitter.com/en/docs/twitter-api/premium/search-api/quick-start/premium-full-archive). This API allows users, provided sufficient credentials, to search Twitter's entire catalog of tweets as opposed to the [Twitter Standard Search API](https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets).

For a script that searches for Tweets using the [Twitter Standard Search API](https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets), look here: [Gather Tweets From Search](https://github.com/feconroses/gather-tweets-from-search).

**Note: This Script was written in January 2020. As such, the script may be outdated for Twitter's current API structure.*

## Dependencies
This script was written and run using python 3.8 and the following libraries.

###### Python Libraries
* [Tweepy 3.8.0](https://docs.tweepy.org/en/v3.8.0/)
* CSV
* SSL
* Time
* Requests
* OS

##### Installing Python Libraries
###### Virtual Environment
When running application locally, it is recommend that a virtual environment is used to isolate the project's dependencies from other projects and your system's environment. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/). Once you have a virtual environment setup and running (or you're feeling bold and ignored that step), you can install the python dependencies by operning a termnial session, navigating to the root folder of this project directory, and running:

```bash
pip install -r requirements.txt
```
This will install all of the required packages listed in the `requirements.txt` file.

The script can be run by in the same terminal session by running:
```bash
python3 search_tweets.py
```
## Motivation
This script was originally used in part to gather data for writing my Senior Thesis, **Social Media and Ethical Consumption: An Event Study of #boycotthandm**, submitted in partial fulfillment of the requirements for the degree of Bachelor of Arts in Economics from Yale University.

## Credits
This project largely borrows code from [Federico Pascual's](https://github.com/feconroses) script [gather-tweets-from-search](https://github.com/feconroses/gather-tweets-from-search), without which this project (and my thesis) would not have as easily been possible.

Small modifications where made to the original script to adapt it for use for **Twitter's Full-Archive Search API**, as well as allow for API credentials to be pulled from the OS environment.
