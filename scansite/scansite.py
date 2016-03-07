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
# https://docs.python.org/3/library/urllib.html

import urllib;
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError

# This is an interesting one, it gives us an object that will
# detect things like start and end tags it is reading HTML tags
# we can listen in and act on these events: e.g. saving the
# value of the href attribute.
from html.parser import HTMLParser

# This variable sitting up here by itself will later
# become the base url from which all other web pages are
# gathered. We will also limit our results to pages served
# from the same base.
baseURL = "";
baseURLsecure = "";
baseURLparts = None;

# We also just want this to be a short implementation, not
# accidentally overrun the web. So let's give it a max depth of
# 5 for starters. Max depth means it takes more than 3 clicks
# to get to a page from the page our original baseURL, we will
# ignore it.
maxDepth = 5;

# To keep track of what pages that we have already scanned, let's
# create a list for that. This list will be a list of lists, each
# identified by the url of the given scanned page. The list within
# the list will be the urls of pages that link to the key url. 
# As well, the HTTP status code will be stored alongside each url.
# So the list will look something like:
# scannedpages = [
#   ('http://example.com', 200, ['http://ilinktoexample.com']),
#   ('http://me.com', 200, ['http://ilinktome.com', 'http://ilinktoexample.com'])
# ]
outcomes = []

scannedpages = []

# And we need a queue of pages that will be scanned
unscannedpages = []

class LinkParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global scannedpages
        global unscannedpages
        if tag == "a":
            link = gethref(attrs)

            # If we failed to get a link, we can leave
            if link != False:
                cleanlink = sanitizelink(link)

                # If we failed to clean the link and make it useable, we can also leave
                if cleanlink != False:

                    # Finally, if we already know about this link, we don't need to scan it
                    # again.
                    if not((cleanlink in scannedpages) or (cleanlink in unscannedpages)):

                        # The nesting at this point is ridiculous, we are on the
                        # sixth indentation. Refactoring the code may make it a
                        # bit more readable.
                        unscannedpages.append(cleanlink)

# We are going to need some helper functions for this scanner
# to work. We put all these functions at the top of the file
# so they will be defined when we run them at the bottom of the
# file. This seems to be the way Python does things.

# Starting with a simple one: if we are given a list of attributes
# in the form [('name', 'value'),...] let's have a function called
# gethref which will return the value of the first href attribute
def gethref(attributes):
    for att in attributes:
        if att[0] == "href":
            return att[1]
    return False

# We would like to be able to do a similar think with the src
# attribute on script tags, let's do that in this getsrc function:
def getsrc(attributes):
    for att in attributes:
        if att[0] == "src":
            return att[1]
    return False

# We need full URLs that we can use to retrieve more web pages
# with, partial URLs, paths like /about or my.jpg are not going
# to get us anywhere. We also only want links that start with
# the baseurl, since we just want to scan the one website. This
# function could be extended to account for different parameters
# but we will just separate web resources by their path for now
def sanitizelink(url):
    global baseURLparts
    urlparts = urlparse(url)
    cleanurl = "";
    if url == "#":
        return False
    if not urlparts.netloc:
        return baseURLparts.scheme + "://" + baseURLparts.netloc + urlparts.path
    elif not urlparts.scheme:
        return baseURLparts.scheme + "://" + urlparts.netloc + urlparts.path
    elif not (urlparts.scheme == "http" or urlparts.scheme == "https"):
        return False
    else:
        return baseURLparts.scheme + "://" + urlparts.netloc + urlparts.path
    
        
    


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
    
    # Let's show the user that we are checking the scheme and the
    # network location as part of our validation
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


# This function we are going to write is going to scan a URL,
# treating it as the base url for all future URLs which we will
# scan. That is, every other URL scanned should be in the same
# directory or a subdirectory of the given URL.
def scanBase(url):
    global baseURL
    global baseURLsecure
    global unscannedpages
    global baseURLparts
    try:
        webPage = urlopen(url)

        # We get the URL a second time here in case a redirect was used.
        # If there was a redirect, let's check with our user if it 
        # is OK to use it. Otherwise, let's start scanning!
        finalURL = webPage.geturl()
        if finalURL.lower() == url.lower() or input("A redirect was used to show the page: {0}. Type 'y' to continue: ".format(finalURL)) == 'y':

            # Woo hoo! We've got a URL that works, let's start scanning for errors
            # on this website.
            baseURLparts = urlparse(finalURL)
            baseURL = "http://" + baseURLparts.netloc + baseURLparts.path
            baseURLsecure = "https://" + baseURLparts.netloc + baseURLparts.path
            unscannedpages.append(baseURL)
            scan()

        # The user was not happy with the URL, let's get out of here. It may
        # be more user-friendly to give them another opportunity to write a
        # new URL, but for now, let's take this easy way out.
        else:
            print("Goodbye")

    # If we get a HTTP error, let's show it here. This includes things
    # like receiving a 404 error
    except HTTPError as err:
        print(format(err))

    # Maybe there is still something wrong with the URL, despite our
    # earlier effort to verify it. Let's handle any more URL problems
    # here.
    except URLError as err:
        print(format(err))
    
    # I am pretty sure there are other errors that could be caught
    # here, but I just found the WindowsError for now. WindowsError
    # seems to be a catch-all error, so any error not matching the
    # above will end up here.
    except WindowsError as err:
        print("Unable to connect. Please check your connection and the URL and try again. Full error: {0}".format(err))

# This function will scan a given url, checking its HTTP code
# then checking 
def scan():
    global unscannedpages
    target = unscannedpages.pop()
    moretogo = True;
    try:
        while moretogo:
            success = False
            try:
                result = urlopen(target)
                success = True
            except:
                print("Error opening: {0}".format(target))

            rescode = 0 if not success else result.getcode()
            if rescode == 200 and sharesbase(target):
                try:
                    scrapurls(target, result.read().decode('utf-8'))
                    print("Scanned {1}".format(rescode, target))
                except UnicodeDecodeError:
                    print("Skipping non Unicode resource: {0}".format(target))
            elif success:
                recordresult(target, rescode)
            try:
                target = unscannedpages.pop()
            except:
                moretogo = False
        showresult()
    except KeyboardInterrupt:
        print("Scan interrupted")


# We need a function to show the outcomes of our hard work.
def showresult():
    global outcomes
    print("Results")
    print("HTTP Code | URL")
    for result in outcomes:
        print("{0} {1}".format(result[1], result[0]))

def recordresult(url, code):
    global outcomes
    global scannedpages
    outcomes.append((url, code, []))
    scannedpages.append(url)

# It would be nice if we could quickly check whether the URL
# shares the same base as our original path. The sharesbase
# function is the answer to this.
def sharesbase(url):
    global baseURL
    global baseURLsecure
    return url.startswith(baseURL) or url.startswith(baseURLsecure)
    


# This function is passed a HTML string. The HTML will be
# parsed and as link tags are discovered, they will be added
# to the unscanned pages list.
def scrapurls(url, html):
    global outcomes
    global scannedpages
    outcomes.append((url, 200, []))
    scannedpages.append(url)
    parser = LinkParser()
    parser.feed(html)

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
else:
    
    # At this point, we have a seemingly valid URL and we
    # are going to try and run with it.
    scanBase(url)