from nltk.corpus import wordnet
from bs4 import BeautifulSoup
import requests

def smaller(length, size):
    if(length < size):
        return length
    else:
        return size

# Settings
path = "/home/will/source/CompanyNamer/words.txt"
results_path = "/home/will/source/CompanyNamer/results.txt"
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

# Add original words to the list
print("Extending list with original word list")
thesaurus_list.extend(word_list)

# Remove duplicates
thesaurus_list = list(dict.fromkeys(thesaurus_list))

# Run everything through a portmeandu finder
pm_list = []

# we'll run through every possible combination of two words
# Basically, iterate through n/2, a pair is len - i
length = len(thesaurus_list)
print(thesaurus_list)
total = (length * (length - 1)) / 2

for i in range(length):
    for j in range(length - i - 1):
        # add i to j
        print("Generating portmeandeus for "+thesaurus_list[i]+" and "+thesaurus_list[i+j+1]+" ("+str(i+j)+"/"+str(total)+")")
        page = requests.get("http://portmanteaur.com/?words="+thesaurus_list[i]+"+"+thesaurus_list[i+j+1])

        results = BeautifulSoup(page.content, 'html.parser')
        results = results.find_all('div',class_="results")

        if len(results) < 2:
            continue

        order1 = results[0]
        order2 = results[1]

        for tag in order1.find_all('span'):
            tag.unwrap()

        for tag in order2.find_all('span'):
            tag.unwrap()

        # Parse out the tags
        list1 = order1.contents
        list2 = order2.contents

        for y in list1:
            if (y==','):
                continue
            pm_list.append(y)

        for y in list2:
            if (y==','):
                continue
            pm_list.append(y)

# Write to file
with open(results_path, 'w') as f:
    for item in pm_list:
        item = item.strip()
        f.write("%s\n" % item)

# Done
print("Done!")







