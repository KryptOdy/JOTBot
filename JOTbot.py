# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 12:40:01 2016

@author: josephwhite
"""

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
    print "Yes"
    
print "Hello, I am JOTbot."
while True:
    message = raw_input()
    if is_goodbye(message):
        break
    if is_rude(message):
        print "That's not nice"
    else:
        if is_question(message):
            answer(message)
        else:
            print "What?"
print "Goodbye"