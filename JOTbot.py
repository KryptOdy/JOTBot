# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 12:40:01 2016

@author: josephwhite
"""

import nltk

from nltk.corpus import brown
from nltk.tokenize import word_tokenize as wt
from collections import defaultdict

def enum(*sequential, **named):
    enum = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enum)

Question = enum('WHO', 'WHAT', 'WHEN', 'WHERE', 'WHY', 'IS', 'NULL')
questionState = Question.NULL
isMultiple = False

class SubjectNode:
    def __init__(self, val):
        self.subject = val
        self.pos = None
        self.dict = defaultdict(dict)

class VerbNode:
    def __init__(self, val):
        self.verb = val
        self.pos = None
        self.dict = defaultdict(list)

dictionary = defaultdict(dict)

print "Hello, I am JOTBot."

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

def findAnswer(subj, subjpos, verb):
    global isMultiple
    if subj.lower() in dictionary:

        #Handle verb agreement, really shit
        if subjpos in {'NNP'} and not isMultiple and verb[len(verb)-1] is not 's':
            verb = verb + "s"

        if verb in dictionary[subj.lower()].dict:
            itemList = []
            if len(dictionary[subj.lower()].dict[verb].dict) == 1:
                for item in dictionary[subj.lower()].dict[verb].dict:
                    itemList.append(item)
                response = subj + " " + verb + " " + itemList[0] + "."
                print response
            elif len(dictionary[subj.lower()].dict[verb].dict) == 2:

                for item in dictionary[subj.lower()].dict[verb].dict:
                    itemList.append(item)
                response  = subj + " " + verb + " " + itemList[0] + " and " + itemList[1] + "."
                print response
            else:
                for item in dictionary[subj.lower()].dict[verb].dict:
                    itemList.append(item)
                response = subj + " " + verb + " " + ', '.join(itemList[:len(itemList)-1]) + " and " + itemList[-1] + "."
                print response
        else:
            print "I don't know" #Search StackExchange
    else:
        print "I don't know" #Search Stackexchange

def answer(question):
    global questionState

    tokenize = wt(question)
    pos = nltk.pos_tag(tokenize)
    question = question.split()

    if question[0] == 'Who':
        questionState = Question.WHO
    elif question[0] == 'What':
        questionState = Question.WHAT
    elif question[0] == 'When':
        questionState = Question.WHEN
    elif question[0] == 'Where':
        questionState = Question.WHERE
    elif question[0] == 'Why':
        questionState = Question.WHY
    elif question[0] == 'Is':
        questionState = Question.IS
    questionHandler(question, pos)

    return

def questionHandler(question, pos):
    '''
    Unique problem with NLTK toolkit, sometimes it will wrongly parse POS, based on other Verbs
    For example: "What does Mary eat?" -> [('What', 'WP'), ('does', 'VBZ'), ('Mary', 'NNP'), ('eat', 'NN'), ('?', '.')]
    "eat" is incorrectly parsed as a Noun

    But "What Mary eat?" -> [('What', 'WP'), ('Mary', 'NNP'), ('eat', 'VBD'), ('?', '.')]
    "eat is correctly parsed as a verb"

    Solution could be to remove verb right before Subject, then check if next word is a verb
    Really annoying but its more accurate
    '''
    global questionState
    global Question

    if questionState == Question.WHO:
        return
    elif questionState == Question.WHAT:
        # Find if part of speech is messed up and fix it, if its not wrong its the same
        pos = fixPos(question, pos)
        print pos
        # Case 1: Only one verb in sentence, which is directly before Subject, use that Verb for search
        # Case 2: Two verbs in sentence, use one which is directly after subject if possible
        #If there is one Subject
        for i in range(0, len(pos)):
            if i is not len(pos):
                if pos[i][1] in {'NNP'} and pos[i+1][1] not in {'CC', ','}:
                    # Check if next word is a verb and use it for search
                    if pos[i + 1][1] in {'VB', 'VBZ', 'VBP', 'VBD', 'IN'}:
                        findAnswer(pos[i][0], pos[i][1], pos[i + 1][0])
                    # Use previous
                    else:
                        findAnswer(pos[i][0], pos[i][1], pos[i - 1][0])
                    break
                ##If Subject is the last word
                #May have multiple subjects in this case
                #2 subjects
                elif pos[i][1] and pos[i+2][1] in {'NNP'} and pos[i+1][1] in {'CC'}:
                    firstSub = pos[i][0]
                    firstPos = pos[i][1]
                    secondSub = pos[i+2][0]
                    secondPos = pos[i+2][1]
                    verb = pos[i+3][0]

                    findAnswer(firstSub, firstPos, verb)
                    findAnswer(secondSub, secondPos, verb)
                    break
    elif questionState == Question.WHEN:
        return
    elif questionState == Question.WHERE:
        return
    elif questionState == Question.IS:
        return


    return

def fixPos(question, pos):

    for i in range(0, len(pos)):
        if i == len(pos) - 2 and  pos[i][1] in {'NNP'}:
            break
        if pos[i][1] in {'NNP'} and pos[i+1][1] not in {'CC'}:
            #Remove previous entry from question
            question.pop(i-1)
            #Turn question back to string and get part of speech of next word
            question = ' '.join(question)
            tokenize = wt(question)
            newpos = nltk.pos_tag(tokenize)
            if newpos[i][1] in {'VB', 'VBZ', 'VBP', 'VBD'}:
                newpos.insert(i-1, pos[i-1])
                return newpos
    return pos
def splitSentence(i, pos, message):
    global isMultiple

    argument = pos[0:i]
    verbLink = pos[i]
    adjunct = message[i + 1:]


    for i in range(0, len(pos)):
        # Single Subject
        if i is not len(pos):
            if pos[i][1] in {'NNP'} and pos[i + 1][1] not in {'CC', ','}:
                isMultiple = False
                argumentDic = SubjectNode(argument)
                verbDic = VerbNode(verbLink)
                verbDic.dict[' '.join(adjunct)] = adjunct
                argumentDic.dict[verbLink] = verbDic
                addToKnowledge(argumentDic, verbDic, adjunct)
                break
            elif pos[i][1] and pos[i+2][1] in {'NNP'} and pos[i+1][1] in {'CC'}:
                isMultiple = True
                #Find NNP's
                for word in argument:
                    if word[1] in {'NNP'}:
                        tempList = []
                        tempList.append(word)
                        argumentDic = SubjectNode(tempList)
                        verbDic = VerbNode(verbLink)
                        verbDic.dict[' '.join(adjunct)] = adjunct
                        argumentDic.dict[verbLink] = verbDic
                        addToKnowledge(argumentDic, verbDic, adjunct)
            break

    return

def addToKnowledge(argumentDic, verbDic, adjunct):
    # Check if Subject exists in dictionary, if not add Sub, Verb, and Adjunct
    # If Subject exists check if verb exists
    # if Verb exists, check if list exists, if not add Verb, Adjunct

    subjectName = argumentDic.subject[0][0].lower()
    verbName = verbDic.verb[0].lower()
    # verbName = argumentDic.dict[verbDic.verb].verb
    if subjectName in dictionary:
        if verbName in dictionary[subjectName].dict:
            if ' '.join(adjunct) in dictionary[subjectName].dict[verbName].dict:
                return
            else:
                dictionary[subjectName].dict[verbName].dict[' '.join(adjunct) ] = adjunct
        else:
             verbDic = VerbNode(verbName)
             verbDic.dict[' '.join(adjunct)] = adjunct
             dictionary[subjectName].dict[verbName] = verbDic
    else:
        argumentDic = SubjectNode(subjectName)
        verbDic = VerbNode(verbName)

        verbDic.dict[' '.join(adjunct)] = adjunct
        argumentDic.dict[verbName] = verbDic
        dictionary[subjectName] = argumentDic
    return

while True:
    message = raw_input()
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

            #Turn message into list of strings
            message = message.split()
            #Tag tokenized message into part of speech
            pos = nltk.pos_tag(tokenize)
            # print pos

            #Loop until you find a VerbPhras, Split sentence based on that
            for i in range(0, len(pos)):
                if pos[i][1] in {'VB', 'VBZ', 'VBP', 'VBD', 'IN'}:
                    splitSentence(i, pos, message)
                    break

print "Goodbye"