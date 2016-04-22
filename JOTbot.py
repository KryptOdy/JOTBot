# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 12:40:01 2016

@author: josephwhite
"""
from __future__ import division
import nltk, re, pprint
from nltk import word_tokenize
import xml.etree.ElementTree as ET

#from lxml import etree
# import lxml
# import xml.etree
# from BeautifulSoup import BeautifulSoup


def is_goodbye(message):
    if message in ["bye", "Bye", "Goodbye", "Good-bye", "goodbye"]:
        return True
    else:
        return False

def is_rude(message):
    words = message.split()
    for word in words:
        if word in ["stupid", "Stupid", "boring", "Boring", "suck", "sucks"]:
            return True
    return False

def is_question(message):
    if message[-1] == "?":
        return True
    else:
        return False

def answer(question):
    # print "Yes"
    print ""
    print "JOT: " + stack_Exch(question)
    print ""

name = "AnonymousUser"

def saysName(message):
    if "My name is" in message:
        nom = message.split()
        nom = nom[3]
        return nom
    else:
        return name

from xml.dom.minidom import parse
import xml.dom.minidom

DOMTree = xml.dom.minidom.parse("Health.xml")
collection = DOMTree.documentElement
posts = collection.getElementsByTagName("row")

def stack_Exch(query):
    i = 0;
    for post in posts:
        if query in post.getAttribute("Title"):
            i = post.getAttribute("AcceptedAnswerId")
            break;
    for post in posts:
        if post.getAttribute("Id") == i:
            ans = post.getAttribute("Body")
            return ans[:100]
            

            # print lxml.html.fromstring(text).text_content()
#            tree = ET.fromstring(ans)
#            notags = ET.tostring(tree, encoding='utf8', method='text')
#            print(notags)

"""f = open('Posts.xml')
s = f.read()

def stack_Exchange(query):
    i = s.find(query)
    i = s[:i].rfind("AcceptedAnswerId")
    i = i + 17
    id = s[i:i+6]
    i = s.find(id)
    i = s[i:].find("Body")
    id = s[i:i+100]
    print id"""
  
  
print "JOT: Hello, I am JOTbot."
print ""
while True:
    message = raw_input()
    name =  saysName(message)
    if is_goodbye(message):
        break
    if is_rude(message):
        print "That's not nice"
    else:
        if is_question(message):
            answer(message)
        else:
            print "Can you repeat that,", name + "?"
print "Goodbye"
