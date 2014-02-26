###Antonio Sirianni
###Introduction to Natural Language Processing
#!/usr/bin/env python

import nltk
import re
import math
from collections import Counter
import random
from random import choice
import time
import csv

#Create Separate Sets of Grams for each of the 4 Categories of Veracity/Affect#
def clean_sort_gramify(text,true,positive,n):
    if true ==2:
        sortedlines = sort_lines_brief(text,positive)
    else:    
        sortedlines = sort_lines(text,true,positive)
    cleanedlines = clean_up_lines(sortedlines,n)
    grams = ngramify(cleanedlines,n)
    return grams

def clean_gramify(text,n):
    gramtuples =[]
    cleanedlines = clean_up_lines_two(text,n)
    for x in cleanedlines:
        grams = ngramify(x,n)
        gramtuples.append(grams)
    return gramtuples

def sort_lines(stringtext,a,b):
    sortedtext = []
    text = stringtext
    for x in text:
        #print x
        if (x[0] == str(a)) and (x[2] == str(b)):
            sortedtext.append(x)
    return sortedtext

def sort_lines_brief(stringtext,b):
    sortedtext = []
    text = stringtext
    for x in text:
        #print x
        if x[2] == str(b):
            sortedtext.append(x)
    return sortedtext

def ngramify(word_list,z):
    """Turns a list of words into a series of n-grams."""
    listofgrams = []
    lengthoflist = len(word_list)
    for y in range(0,(lengthoflist - z + 1)):
        gram = []
        for x in range (y,y+z):
            gram.append(word_list[x])
        gramtuple = tuple(gram)
        listofgrams.append(gramtuple)
    return listofgrams

def clean_up_lines(stringtext,n):
    cleanedtext = []
    for x in stringtext:
        y = clean_up(x,n)
        for z in y:
            cleanedtext.append(z)
    return cleanedtext

def clean_up_lines_two(stringtext,n):
    cleanedtext = []
    for x in stringtext:
        cleanedline = []
        y = clean_up(x,n)
        for z in y:
            cleanedline.append(z)
        cleanedtext.append(cleanedline)
    #print cleanedtext
    return cleanedtext

def clean_up(stringtext,n):
    text = stringtext
    text = re.sub(r'<.*>','',text)
    #replace verse numbers (beginning of sentence) with <s> tag
    text = re.sub(r'[0-9]+[:,][0-9]+(,*)\s*','', text)
    #replace newlines with spaces (we do a space split below)
    text = re.sub(r'[\n]+',' ', text)
    #puts space around punctuation except sentence enders
    text = re.sub(r'[^\w\s\'\.!\?]', ' \g<0> ', text)
    #puts an end sentence token after each sentence along with whitespace.
    text = re.sub(r'(\.+)|(!+)|(\?+)', ' \g<0> </s> ', text) 
    #put n-1 <s> tokens before every </s> token
    for x in range(n-1):
        text = re.sub('</s>', '</s> <s>', text)
    #lowercase, remove leading/trailing spaces
    text = text.lower().strip()
    #split on 1+ spaces:
    text = re.split(r' +', text)
    for x in range(n-1):
        text.insert(0, '<s>')
    return text

class gramdict:
    def __init__(self,listone,listtwo,number):
        ##Creates a list of decision rules for two distinct lists of grams.
        ##Dictionary counts the occurences of grams in the first list.
        dictone = {}
        ##Dictionary counts the occurences of grams in the second list.
        dicttwo = {}
        ##listonegrams is the total number of grams in listone
        listonegrams = len(listone)
        ##listtwograms is the total number of grams in listtwo
        listtwograms = len(listtwo)
        #print listtwograms
        dictionary = {}
        ##Allvocab is the number of distinct grams in either list.
        allvocab = set(listone + listtwo)
        ##vocabone is the number of distinct grams in the first list.
        vocabone = len(set(listone))
        ##vocabtwo is the number of distinct grams in the second list.
        vocabtwo = len(set(listtwo))
        for x in listone:
            try:
                dictone[x] += 1
            except:
                dictone[x] =1
        for y in listtwo:
            try:
                dicttwo[y] +=1
            except:
                dicttwo[y] =1
        rules =[]
        for z in allvocab:
        ##we now create a rule for each gram that occurs in either list by looking at the frequencies
        ##of grams in each list. numone is the number of appearances of a gram in listone.
        ##num two is the number of appearance of a gram in listtwo.
            try:
                numone = dictone[z]
            except:
                numone = 0
            try:
                numtwo = dicttwo[z]
            except:
                numtwo = 0
            ## we now determine in which list the gram is more frequent, and calculate a rule in favor of it.
            ## the rules are sorted by the lower bounds of a confidence interval calculated below.
            if (numone/float(numtwo+numone)) > (listonegrams/float(listonegrams+listtwograms)):
                #p is the proportion of all instances of a gram occuring in list one.
                #q is the proprtion of all grams occuring in list one. used for normalizing.
                #v is the proportion of all distinct grams occuring in list one. used for normalizing.
                #n is the total number of occurences of the gram.
                p = (numone/float(numtwo+numone))
                q = listonegrams/float(listonegrams+listtwograms)
                v = vocabone/float(vocabone+vocabtwo)
                n = numone + numtwo
                if numone == n:
                    ##If all occurrences are in one list or the other, bayesian Conf Int is calcualted##
                    #SE = 0.1887*math.log(numone) + 0.2521 #95%
                    SE = 0.1711*math.log(numone) + 0.35 # 90%
                    #SE = 0.2458*math.log(numone) + 0.0423
                    #SE = 0.135*math.log(numone) + 0.5089 #75%
                    #SE = 0.175 *math.log(numone) +.331108
                else:
                    SE = 1*math.sqrt(p*(1-p)/n)       
                confint = (p-SE)
                newrule = [z,confint/v,numone+numtwo,1]
            else:
                #p is the proportion of all instances of a gram occuring in list two.
                #q is the proprtion of all grams occuring in list two. used for normalizing.
                #v is the proportion of all distinct grams occuring in list two. used for normalizing.
                #n is the total number of occurences of the gram.
                p = (numtwo/float(numtwo+numone))
                q = listtwograms/float(listonegrams+listtwograms)
                v = vocabtwo/float(vocabone+vocabtwo)
                n = numone + numtwo
                if numtwo == n:
                    ##If all occurrences are in one list or the other, bayesian Conf Int is calcualted##
                    #SE = 0.1887*math.log(numtwo) + 0.2521 #95%
                    SE = 0.1711*math.log(numtwo) + 0.35 #90%
                    #SE = 0.2458*math.log(numtwo) + 0.0423
                    #SE = 0.135*math.log(numtwo) + 0.5089 #75%
                    #SE = 0.175 *math.log(numtwo) +.331108
                else:
                    SE = 1*math.sqrt(p*(1-p)/n)
                confint = (p-SE)
                newrule = [z,confint/v,numone+numtwo,0]
            rules.append(newrule)
        ## we now sort the rules by the lowerbound of the confidence interval calculated.
        rules.sort(key = lambda x: -x[1])
        #for x in range (0,25):
        #    print rules[x][1]
        #    print rules[x][3]
        
        self.rules = rules
        self.allvocab = allvocab
        self.listone = listone
        self.listtwo = listtwo
          
def predicitify(trainset,testset,posnum,truthnum):
    ###Determine if the review is generally positive or negative for each set.###
    ##create list for positive data
    allposdata = clean_sort_gramify(trainset,2,1,posnum)
    ##create list for negative data
    allnegdata = clean_sort_gramify(trainset,2,0,posnum)
    ##find rules for positive vs negative data
    truepos = clean_sort_gramify(trainset,1,1,truthnum)
    falsepos = clean_sort_gramify(trainset,0,1,truthnum)
    trueneg = clean_sort_gramify(trainset,1,0,truthnum)
    falseneg = clean_sort_gramify(trainset,0,0,truthnum)
    posornegrules = gramdict(allposdata,allnegdata,posnum).rules
    posrules = gramdict(truepos,falsepos,truthnum).rules
    negrules = gramdict(trueneg,falseneg,truthnum).rules
    testlines = clean_gramify(testset,posnum)
    ###determine if tuple should follow positive or negative rule set###
    firstresults =[]
    for a in testlines:
        c = rule_check(posornegrules,a)
        firstresults.append(c)        
    finalresults =[]
    for p in firstresults:
    #determine veracity of positive entries
        if p[1] == 1:
            d = rule_check(posrules,p[0])
            finalresults.append(d)
    #determine veracity of negative entries
        else:
            e = rule_check(negrules,p[0])
            finalresults.append(e)
    vectorizedresults = []
    for y in finalresults:
        try:
            vectorizedresults.append(y[1])
        except:
            vectorizedresults.append(0)
    return vectorizedresults
    
def rule_check(rules,lineoftext):
    """helper for predictify"""  
    for x in rules:
        for a in lineoftext:
            if x[0] == a:
                return [lineoftext,x[3]]
    return[lineoftext,0]

def truth_vector(linesoftext):
    vector = []
    for x in linesoftext:
        vector.append(x[0])
    return vector

def calculate_accuracy(x,y):
    z = len(x)
    p = 0
    q = 0
    trues = 0
    falses = 0
    for a in range (0,z):
        if str(x[a]) == str(y[a]):
            p = p+1
            q = q+1
        else:
            q = q+1
        if str(y[a]) == '1':
            trues = trues +1
        else:
            falses = falses + 1
    print trues
    print falses
    return float(p)/float(q)

if __name__ == '__main__':
    tic = time.time()
    train = open('reviews.train').readlines()
    test = open('reviews.test').readlines()
    valid = open('reviews.valid').readlines()
    kaggle = open('kaggle_data_file.txt').readlines()
    kaggle=kaggle[1:]
    #print len(kaggle)
    #print len(train)
  
    a = truth_vector(valid)
    '''
    b = predicitify(train,valid,2,2)
    print calculate_accuracy(a,b)
    '''
    
    d = truth_vector(kaggle)
    c = predicitify(train,kaggle,1,1)
    #print calculate_accuracy(d,c)
    number = 0
    print 'Id'+','+'Label'
    for x in c:
        print str(number) +',' + str(x)
        number = number + 1
    #print time.time() - tic'''
