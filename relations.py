from nltk import word_tokenize

class RelationNet:
    
    def __init__(self, comparePhrase):
        # self.synsets = {}
        self.allThings = {}
        self.indices = {}
        self.relations = {}
        self.compPhrase = comparePhrase
        self.count = 0
    
    def put_rel(self, thing1, thing2):
        """self.allThings[thing1] = self.count
        self.indices[self.count] = thing1
        self.count += 1
        self.allThings[thing2] = self.count
        self.indices[self.count] = thing2
        self.count += 1"""
        if self.relations.has_key(thing1) == False:
            self.relations[thing1] = []
        self.relations[thing1].append(thing2)
        if self.contains(thing1, thing1):
            print "JOT: Warning: cycle detected."


    def set_compPhrase(self, phrase):
        self.compPhrase = phrase
        
    def get_compPhrase(self):
        return self.compPhrase

    # recursive contains method
    def contains(self, thing1, thing2):
        # if the dictionary doesn't contain thing1, thing1 can't contain thing2
        if self.relations.has_key(thing1) == False:
            return False        
        # if thing2 is found in the relations of thing1, return true
        if thing2 in self.relations[thing1]:
            return True
        # recursively search the children of thing1
        found = False
        for latter in self.relations[thing1]:
            found = self.contains(latter, thing2)
            if found == True:
                return True
        return False

    # get the relationship between thing1 and thing2
    def get_rel(self, thing1, thing2):

        # print self.relations
        phr = self.compPhrase

        #if self.relations.has_key(thing2):
        if self.contains(thing2, thing1): 
            #if thing1 in self.relations[thing2]:
            print "JOT: no, " + thing1 + " is not " + phr + " " + thing2
            return

        """if self.relations.has_key(thing1) == False:
            #print "JOT: no, " + thing1 + "is not " + phr + thing2
            print "It might or it might not be."
            return"""
        
        if self.contains(thing1, thing2):
            print "JOT: yes, " +  thing1 + " is " + phr + " " + thing2
            return

        #elif thing2 in self.relations[thing1]:
            #print "JOT: yes, " + thing1 + "is " + phr + thing2
            #return
        else:
            #print "JOT: no, " + thing1 + "is not " + phr + thing2
            print "JOT: It might or it might not be."
            return

    @staticmethod
    def find_compPhrase(message):
        i = message.find("than")
        toks1 = word_tokenize(message[:i])
        compPhrase = toks1[-1] + " than"
        return compPhrase

nets = {}

rn = RelationNet("bigger than")
rn.put_rel("a dog", "a mouse")
rn.put_rel("mount everest", "mount greylock")
rn.put_rel("a liter", "a pint")
# rn.get_rel("a mouse" , "a dog")
# rn.get_rel("a dog", "a mouse")

while True:
    # read a line from the user
    message = raw_input("usr: ")
    mlen = len(message)
    
    # find the comparison phrase (marked by the presence of the word than)
    cp = RelationNet.find_compPhrase(message)
    cplen = len(cp)
    i = message.find(cp)

    # a statement of fact: find the dictionary containing the appropriate
    # relations and enter it into the dictionary (or create a new one)
    if message[-1] == ".":
        if nets.has_key(cp):
            currentNet = nets[cp]
        else:
            nets[cp] = RelationNet(cp)
            currentNet = nets[cp]

        currentNet.put_rel(message[0:i-4], message[i+cplen+1:mlen-1])

    # a query: find the appropriate dictionary and do a query there
    elif message[-1] == "?":
        currentNet = nets[cp]
        currentNet.get_rel(message[3:i-1], message[i+cplen+1:mlen-1])
      
    else:
        break

    """toks = message.split()
    if toks[0] == 'p':
        rn.put_rel(toks[1], toks[2])
    elif toks[0] == 'g':
        rn.get_rel(toks[1], toks[2])
    else:
        print "Goodbye"
        break"""

