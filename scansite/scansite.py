# Hello fellow software developer! My name is Will and I 
# would like to start by saying I don't know much about
# Python or web crawlers. This is an adventure more to 
# learn about these things rather than make top quality
# software, although hopefully the end result is a good
# one nevertheless.

# As a first step, let's first import the urllib, 
# heard from this site:
# http://www-rohan.sdsu.edu/~gawron/python_for_ss/course_core/book_draft/web/urllib.html
# that it should be helpful for retriving web resources.
# And browsing through the documentation never hurts:
# https://docs.python.org/3/library/urllib.html

import urllib;
from urllib.parse import urlparse

# We are going to need some helper functions for this scanner
# to work. We put all these functions at the top of the file
# so they will be defined when we run them at the bottom of the
# file. This seems to be the way Python does things.

# This function will look at the parts of the given url string and
# determine if we have everything we need to be able to use this
# URL as a base from which to conduct our search. It will return
# True if the URL looks good and false otherwise.
def validateUrl(url):

    # Using the urlparse function (from the urllib.parse library)
    # we are going to get back the url in its component parts. It
    # will be something that looks like:
    #
    # ParseResult:
    # - scheme='http'
    # - netloc='example.com:80'
    # - path='/some/example/path.html'
    # - params=''
    # - query=''
    # - fragment=''
    #
    # Not sure why netloc is given as one thing here. I imagine
    # having a hostname and a port number may address more use
    # cases. Anyhow! Hmm, it seems these can also be accessed
    # independently through hostname and port if they exist.
    # If they do not exist, they will not be set and we'll get an
    # AttributeError when looking for them, so we'll stick to
    # netloc for now.

    urlParts = urlparse(url)

    print("Checking scheme: {0}".format(urlParts.scheme))
    print("Checking network location: {0}".format(urlParts.netloc))

    if not(urlParts.scheme == "http" or urlParts.scheme == "https"):

        # Let the user know what we are looking for, websites
        # that we can scan over HTTP or HTTPS
        print("The URL scheme must be http or https.");
        return False
    elif urlParts.netloc == "":
        print("The network location does not seem to be set in the given URL.")
        return False
    return True;

# Finally, after writing those functions we can look at
# actually running the program.

# I guess we should ask the user the base URL of the site
# they want to scan. Hmm... input seems helpful here, 
# let's use that.

url = input('Please enter the base URL of the site to scan: ')

# So know we have a url from the user, let's assume that
# it is not valid.
validUrl = False;

# And then keep getting new URLs until we have something 
# we can use.
while not validUrl and url != "q":

    # Firstly, we would to know if the user has given us
    # a valid URL. We made a function validateUrl to do
    # exactly that.

    validUrl = validateUrl(url);
    if not(validUrl):
        print("The given URL is not valid.")

        # Here, we give the user another chance to put in a URL
        # that will work.
        url = input("Please enter a URL in the form http://example.com/: ")
    else:
        print("Scanning website found at " + url)
        validUrl = True;

# If the user chose to quit, let's let them know we
# received their command and say goodbye.
if url == "q":
    print("Goodbye!")