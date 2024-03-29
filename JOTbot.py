# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 12:40:01 2016

@author: josephwhite
"""
from __future__ import division
import nltk, re, pprint
from nltk import word_tokenize as wt
from nltk import sent_tokenize
from collections import defaultdict
import xml.etree.ElementTree as ET

#from lxml import etree
# import lxml
# import xml.etree
from bs4 import BeautifulSoup

class Node:
    def __init__(self, val):
        self.verb = None
        self.argument = None
        self.subject = val

dictionary = defaultdict(dict)

# detect if the message is a goodbye, which indicates user's desire to exit
def is_goodbye(message):
    if message in ["bye", "Bye", "Goodbye", "Good-bye", "goodbye"]:
        return True
    else:
        return False

# detect insult by looking for presence of flagged words
def is_rude(message):
    words = message.split()
    for word in words:
        if word in ["stupid", "Stupid", "boring", "Boring", "suck", "sucks"]:
            return True
    return False

# check for question mark
def is_question(message):
    if message[-1] == "?":
        return True
    else:
        return False

# answer a question
def answer(question):
    
    # tokenize and parse
    tokenize = wt(question)
    pos = nltk.pos_tag(tokenize)

    print pos

    subject = "placeholder"
    for tag in pos:
        if ('NNP' in tag) or ('NN' in tag):
            subject = tag[0]
            print subject

    #Search for Subject in dictionary
    if subject in dictionary:
        node = dictionary[subject]
        print "JOT: Yes I know, " + subject + " " + node.verb + " "+ node.argument
    else:
        ans = stack_Exch(question)
        if (ans != None):
            print "JOT: " + ans
            return
        
        print subject
        ans = stack_Exch(subject)
        if (ans != None): 
            print "JOT: " + ans
            return

        print "Sorry I don't understand the question."


name = "AnonymousUser"
# detect if the user says their name
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

# scrape an answer from stackExchange
def stack_Exch(query):
    i = 0;
    for post in posts:
        title = post.getAttribute("Title")
        title = wt(title)
        if query in title:
            i = post.getAttribute("AcceptedAnswerId")
            break;
    for post in posts:
        if post.getAttribute("Id") == i:
            ans = post.getAttribute("Body")
            sentences = nltk.sent_tokenize(ans)
            ans = sentences[0] + sentences[1]
            ans = BeautifulSoup(ans, 'html.parser')
            return ans.get_text()
    return "I don't know the answer to that question."            

            # print lxml.html.fromstring(text).text_content()
#            tree = ET.fromstring(ans)
#            notags = ET.tostring(tree, encoding='utf8', method='text')
#            print(notags)  
  
print "JOT: Hello, I am JOTbot."
while True:
    message = raw_input()
    name =  saysName(message)
    tokenize = wt(message)
    if is_goodbye(message):
        break
    if is_rude(message):
        print "That's not nice"
    else:
        if is_question(message):
            answer(message)
        else:
            print "Ok"

            #Insert statement into table
            pos = nltk.pos_tag(tokenize)
            
            #Take first NNP
            if ('NNP' in pos[0][1]) or ('NN' in pos[0][1]):
                n = Node(pos[0][0])
                # Take Verb
                if 'VB' or 'VBZ' in pos[1][0]:
                    n.verb = pos[1][0]

                adjunct = ""
                for x in range(2, len(pos)):
                    adjunct = adjunct + pos[x][0] + " "
                n.argument = adjunct

                dictionary[n.subject] = n

            # print "Can you repeat that,", name + "?"

print "Goodbye"
