'''
Created to test pawned email addresses.
Tested on Kali Debian 4.14.17-1kali1 (2018-02-16) and python2.
Requirements:
    Selenium
    Chrome
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import sys
import time

#Chrome must be run without root
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
browser = webdriver.Chrome(chrome_options=chrome_options)

#Constants
EMPTYRESPONSE = '<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;"></pre></body></html>'

EMAILS = '/tmp/email.txt'
RESULTS = '/tmp/workfile.txt'


def createEmailListFromTxtFile(email):
    with open(EMAILS) as file:
        for line in file:
            line = line.strip()
            email.append(line)
    return email

def checkEmails(email):
    #first request to test WAF and get redirect
    browser.get("https://haveibeenpwned.com/api/breachedaccount/test@gmail.test")
    time.sleep(10)

    f = open(RESULTS, 'w')
    
    for i in email:
        try:
            browser.get("https://haveibeenpwned.com/api/breachedaccount/" + i)

            if EMPTYRESPONSE not in browser.page_source:
                try:
                    print i + " found in: " + browser.find_element_by_tag_name('pre').text.encode('utf-8')
                    f.write(i + " found in: " + browser.find_element_by_tag_name('pre').text.encode('utf-8') + "\n")

                except:
                    print "Error, need to recheck: " + i
                    f.write("Error, need to recheck: " + i + "\n")
            time.sleep(7)

        except:
            sys.exit('Cannot open web page')
    f.close()

def main():
    email = []
    checkEmails(createEmailListFromTxtFile(email))

if __name__ == '__main__':
	main()
