from nltk.corpus import wordnet
from bs4 import BeautifulSoup
import requests
import sys


def smaller(length, size):
    if(length < size):
        return length
    else:
        return size

# Settings
path = "/home/will/source/CompanyNamer/words.txt"
num_synonyms = 5
num_antonyms = 2

# Load words from a text file
f = open(path, 'r')
x = f.readlines()
f.close()

# Create a list that will hold words
word_list = []

# Iterate through file, for each line, split by commas and add the words to a list
for line in x:
    if line == "" or line == "\n":
        continue
    # Split by commas
    result = [x.strip() for x in line.split(',')]
    word_list.extend(result)

# Thesaurus web scraping
thesaurus_list = []

print("Finding synonyms/antonyms...\n")

thesaurus_progress = 0
word_list_length = len(word_list)

for word in word_list:  

    print('Adding snyonyms/antonyms for '+word+' ('+str(thesaurus_progress)+'/'+str(word_list_length)+')')

    page = requests.get("http://thesaurus.com/browse/"+word)
    results = BeautifulSoup(page.content, 'html.parser')


    results = results.find_all('ul', class_='css-1lc0dpe et6tpn80')
   
    thesaurus_progress+=1

    if len(results) < 2:
        continue
    
    synonyms = results[0].find_all('a')
    antonyms = results[1].find_all('a')
    
    for i in range(smaller(num_synonyms, len(synonyms))):
        thesaurus_list.append(synonyms[i].contents[0])

    for i in range(smaller(num_antonyms, len(antonyms))):
        thesaurus_list.append(antonyms[i].contents[0])

print(thesaurus_list)

#Remove duplicates
#thesaurus_list = list(dict.fromkeys(thesaurus_list))

#for line in thesaurus_list:
 #   print(line)

# Run through portmandeau finder

# Test
#for line in word_list:
    #print(line)

