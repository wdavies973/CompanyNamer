from nltk.corpus import wordnet


# Settings
path = "C:\\Users\\wdavi\\PycharmProjects\\CompanyNamer\\words.txt"
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

thesaurus_list = []

# Thesaurus
for word in word_list:
    antonyms = []

    for syn in wordnet.synsets(word):
        for lm in syn.lemmas():
            if lm.antonyms():
                antonyms.append(lm.antonyms()[0].name())

    synonyms = []

    for syn in wordnet.synsets(word):
        for lm in syn.lemmas():
            synonyms.append(lm.name())

    thesaurus_list.extend(synonyms[:num_synonyms])
    thesaurus_list.extend(antonyms[:num_antonyms])

thesaurus_list.extend(word_list)

pm = []

# Remove duplicates
thesaurus_list = list(dict.fromkeys(thesaurus_list))

for line in thesaurus_list:
    print(line)

# Run through portmandeau finder

# Test
#for line in word_list:
    #print(line)

