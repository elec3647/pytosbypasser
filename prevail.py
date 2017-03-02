import requests
import time
from bs4 import BeautifulSoup

def check_connection():
    cookies = {
        'xp_ci': '3z4GvkaFzAbaz4iNz9r0zLM1WV8s9',
        'a': 'QQAJAAAACwA43qwGMTFsM1JFAAAAAC5pYlk=',
        'dssid2': '5bd51299-87f2-40e8-b5cd-1e15222a853e',
        'dssf': '1',
        'optimizelyEndUserId': 'oeu1486410896387r0.750811346997134',
        'pxro': '2',
        'as_gloc':
            '5e47b47d998dad6ad6f134d6254883170cf57f564b7dd9824e605be93955ca93364e186c2e40843ef8ed81fd7dc802ac873f6f0f2cefc7ba4d16ddb9ff6a05e7b70962d8f07e23a73bf7a62a082dde50d2d1ea96f9724d5b48bdc0851e699eb3',
        'rtsid': '%7BUS%3D%7Bt%3Da%3Bi%3DR225%3B%7D%3B%7D',
        'as_sfa': 'Mnx1c3x1c3x8ZW5fVVN8Y29uc3VtZXJ8aW50ZXJuZXR8MHwwfDE=',
        'optimizelySegments': '%7B%22341793217%22%3A%22direct%22%2C%22341794206%22%3A%22false%22%2C%22341824156%22%3A'
                              '%22gc%22%2C%22341932127%22%3A%22none%22%7D',
        'optimizelyBuckets': '%7B%7D',
    }

    headers = {
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8,af;q=0.6',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'http://captive.apple.com/',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
    }
    token = '47a4104d'
    url = 'http://captive.apple.com'
    success_string = 'Success'
    params = {'tok': token,
              'redir': 'http://captive.apple.com'
              }
    s = requests.Session()
    average = 0
    cnt = 0
    fail = 0
    while True:
        try:
            html_doc = s.get(url).text
        except requests.exceptions.ConnectionError as e:
            print "Failure: %s" % e
        soup = BeautifulSoup(html_doc, 'lxml')
        status = soup.title.string
        print "Connection Status '%s'" % status
        if status != success_string:
            fail += 1
            forms = find_forms(soup.prettify())
            token = forms[0]['inputs']['tok']
            params['tok'] = token
            params['redir'] = forms[0]['inputs']['redir']
            print
            print "Resetting Connection"
            r = s.get(url, headers=headers, params=params)
            if r.status_code != 200:
                print "Reset Return Code:", r.status_code
            print
        cnt += 1
        if (cnt % 30) == 0:
            print "Success Rate %0.2f%%" % (100*(float(cnt - fail)/cnt))
        time.sleep(2)


def find_forms(form_string):
    my_forms = []
    s = BeautifulSoup(form_string, 'lxml')
    try:
        forms = s.find_all('form')
    except TypeError:
        print "Found no forms"
        return None
    for form in forms:
        my_form = {}
        try:
            my_form['method'] = form['method']
            my_form['action'] = form['action']
            my_form['inputs'] = {e['name']: e.get('value', '') for e in form.find_all('input', {'name': True})}
            my_forms.append(my_form)
        except KeyError:
            next
    return my_forms

# Test
#file = 'prevail_fail.html'
#failstr = open(file).read()
#print find_forms(failstr)


check_connection()
