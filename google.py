import nltk
from nltk import sent_tokenize 
import urllib
import json as m_json
from bs4 import BeautifulSoup

#query = raw_input ( 'Query: ' )

# search for a query on google
def search(query):
    query = query + " stackexchange"
    # query = query + " wikipedia"

    # code adapted form a stackoverflow question
    query = urllib.urlencode ( { 'q' : query } )
    response = urllib.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query).read()
    json = m_json.loads ( response )
    results = json [ 'responseData' ] [ 'results' ]
    result = results[0]
    
    
    title = result['title']
    url = result['url']
    ans = urllib.urlopen(url).read()
    i = ans.find("answercell")
    ans = ans[i+12:i+500]
    # i = ans.find("mw-content-text")
    # ans = ans[i-9:i+2000]
    pretty = BeautifulSoup(ans, 'html.parser').get_text()
    sentences = nltk.sent_tokenize(pretty)
    n = 2
    if len(sentences) <= n:
        n = len(sentences)
    for k in range(0,n):
        print sentences[i]
