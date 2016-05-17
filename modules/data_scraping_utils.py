
import urllib.request
import urllib.parse
import urllib.error
import gzip
import json
import io
import requests
import ast
import sys


def http_get_old(url):
    req = urllib.request.Request(url)
    # # Set Authorization header
    # req.add_header('Authorization', 'Bearer ' + access_token)
    # # Set user agent
    # req.add_header('User-agent', user_agent)

    # Tell server we can handle gzipped content
    req.add_header('Accept-encoding', 'gzip')
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as err:
        # If error is of type application/json, it will be an XmlstatsError
        # see https://erikberg.com/api/objects/xmlstats-error
        if err.headers.get('content-type') == 'application/json':
            data = json.loads(err.read().decode('UTF-8'))
            reason = data['error']['description']
        else:
            reason = err.read()
        print('Server returned {} error code!\n{}'.format(err.code, reason))
        sys.exit(1)
    except urllib.error.URLError as err:
        print('Error retrieving file: {}'.format(err.reason))
        sys.exit(1)
    data = None
    headers = response.info()
    if response.info().get('Content-encoding') == 'gzip':
        buf = io.BytesIO(response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    else:
        data = response.read()
    return data

def http_get(url):
    headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.16 Safari/534.24"}
    try:
        r = requests.get(url,headers=headers)
    except requests.exceptions.Timeout:
	    pass
	    # Maybe set up for a retry, or continue in a retry loop
    except requests.exceptions.TooManyRedirects:
	    pass
	    # Tell the user their URL was bad and try a different one
    except requests.exceptions.RequestException as e:
	    # catastrophic error. bail.
	    print (e)
	    sys.exit(1)
    return r.text
