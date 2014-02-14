###Antonio Sirianni
###Introduction to Natural Language Processing


import nltk
import re
from collections import Counter
import random
from random import choice
corpusraw = open('hotelreviewssmall.txt')
corpuswhole = open('reviews.train')
corpusbible = open('kjbible.train')

###Process bodies of Text###


###CREATE N_GRAMS##

def tokenizecorpus(body):
    """Takes body of text and turns it into a list of lists of text."""
    newbody = body.readlines()
    baselist =[]
    for x in newbody:
        y = nltk.word_tokenize(x)
        baselist.append(y)
    return baselist

def ngramify(body,z):
    """Turns a list of words into a series of n-grams. Helper for ngramifylists."""
    listofgrams = []
    lengthoflist = len(body)
    for y in range(0,(lengthoflist - z + 1)):
        gram = []
        for x in range (y,y+z):
            gram.append(body[x])
        listofgrams.append(gram)
    return listofgrams

def ngramifylists(body,z):
    """Turns a list of a list of words into a series of n-grams. """
    allgrams = []
    for x in body:
        grams = ngramify(x,z)
        for y in grams:
            allgrams.append(y)
    return allgrams

##Calculates All Tokens##

def tokenize(body):
    """Creates a list of all tokens in a corpus."""
    a = body
    tokens =[]
    for x in a:
        for y in x:
            if not y in tokens:
                tokens.append(y)
    return tokens

###FUNCTIONS THAT RANDOMLY SELECT WORDS###
def calculateprobabilities(ngram,body):
    """Randomly select a word based on the preceding n-gram, or conversely,
    create a dictionary with all of your choices of random words. A helper function
    for stochasticize dictionary."""
    y = len(ngram)+1
    p = ngramifylists(body,y)
    tokens = tokenize(body)
    q = []
    dictionary ={}
    print ngram
    for token in tokens:
        dictionary[token]=0
    for x in p:
       if ngram == x[0:-1]:
            q.append(x[-1])
    print len(q)
    for words in q:
        try:
            dictionary[words] = dictionary[words]+1
        except:
            dictionary[words]= 1   
    return dictionary

def stochasticizedictionary(ngram,body):
    """Uses rowvectorize to calculate a dictionary of relative proabilities for
    a next word, then randomly selects a word. A helper function for sentencize."""
    dictionary = calculateprobabilities(ngram,body)
    wordprob = []
    for a in dictionary:
        wordprob.append((a,dictionary[a]))
    total = sum(prob for word, prob in wordprob)
    randomnum = random.uniform(0, total)
    counternum = 0
    for word, prob in wordprob:
        if counternum + prob >= randomnum:
            return word
        counternum = prob + counternum
    
###Function That Makes Sentences### 
def sentencize(body,end,n):
    """Uses the stochasticize dictionary function to randomly select words
    and then make a sententce."""
    sentence =[]    
    while len(sentence) < 8:
        if len(sentence) < n:
            nextword = stochasticizedictionary(sentence,body)
        elif n == 1:
            nextword = stochasticizedictionary([],body)
        else:
            nextword = stochasticizedictionary(sentence[-(n-1):],body)
        sentence.append(nextword)
        if sentence[-1] == end:
            return sentence
    return sentence


corpus = tokenizecorpus(corpuswhole)
print corpus [6]
#print sentencize(corpus,'.',3)

#print sentencize(corpus,2,'and')


