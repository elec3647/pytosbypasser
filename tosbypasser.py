# coding=utf-8
import os

import requests
from bs4 import BeautifulSoup, SoupStrainer
cache_dir = '/Users/kreitzem/wifi_redirects'
r = requests.get("http://captive.apple.com")
b = BeautifulSoup(r.text, 'lxml')
if b.title.text == 'Success':
    print "We are connected to the internets."
    exit(0)
else:
    print "We are not logged in."
    #fh = open(os.path.join(cache_dir, b.title.text.replace(' ', '_') + '.html'), 'w')
    #fh.write(b.prettify(encoding='UTF-8'))
    #fh.close()
    #print b.prettify()
    #for x in b.find_all('a'):
    #    print x.prettify()
    #    print "======================================================================="
    forms = b.find_all('form')
    #for x in b.find_all('form'):
    #    print x.prettify()
    #    print "======================================================================="
    for form in forms:
        inputs = form.find_all('input')
        for form_input in inputs:
            print "======================================================================="
            print form_input.prettify()
            print form_input._
            #for attrib in form_input:
            #    print "======================================================================="
            #    print attrib



    #for link in BeautifulSoup(r.text, parseOnlyThese=SoupStrainer('a')):
    #    if link.has_attr('href'):
    #        print link['href']

