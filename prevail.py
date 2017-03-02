import requests
import time
from bs4 import BeautifulSoup


def check_connection():
    headers = {
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8,af;q=0.6',
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
    cnt = 0
    fail = 0
    while True:
        try:
            html_doc = s.get(url).text
        except requests.exceptions.ConnectionError as e:
            print("Failure: %s" % e)
        soup = BeautifulSoup(html_doc, 'lxml')
        status = soup.title.string
        print("Connection Status '%s'" % status)
        if status != success_string:
            fail += 1
            forms = find_forms(soup.prettify())
            token = forms[0]['inputs']['tok']
            params['tok'] = token
            params['redir'] = forms[0]['inputs']['redir']
            print()
            print("Resetting Connection")
            r = s.get(url, headers=headers, params=params)
            if r.status_code != 200:
                print("Reset Return Code:", r.status_code)
            print()
        cnt += 1
        if (cnt % 30) == 0:
            print("Success Rate %0.2f%%" % (100 * (float(cnt - fail) / cnt)))
        time.sleep(2)


def find_forms(form_string):
    my_forms = []
    s = BeautifulSoup(form_string, 'lxml')
    try:
        forms = s.find_all('form')
    except TypeError:
        print("Found no forms")
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


check_connection()
