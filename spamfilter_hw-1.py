import os

def update_freq_table(table, filename):
    """
    given the name of a file, add all occurrences of words in the file to the frequency table, which is a dictionary of {word : count}
    """
    with open(filename, 'r') as f:
        """
        open file to read
        """
        for line in f:
            line = line.strip()
            for word in line.split(" "):

                if word.isalpha():
                    word = word.lower()
                    if word in table:
                        table[word] += 1
                    else:
                        table[word] = 1
'''
test_table = {}
directory = "./ham"
filename = "5991.2002-02-07.williams.ham.txt"
update_freq_table(test_table, directory+"/"+filename)
print test_table
'''

def create_freq_table(dirname):
    """
    create a word frequency table (a dictionary).scanning all the files under the given directory and updating the frequency table. Returns the frequency table.
    """
    table = {}

    dirs = os.listdir( dirname ) #scanning all the files under the given directory
    for filename in dirs:
        #print file
        update_freq_table(table, dirname+"/"+filename) #updating the frequency table. Returns the frequency table.

    return table
'''
spamdir = "./spam"
spam_table = create_freq_table(spamdir)
print len(spam_table)
print spam_table['science']
'''

def prob_word_given_label(word, table):
    """
    returns the number of occurrences of the word in the table as a smoothed percentage of the total number of word occurrences in the table.
    """
    totalObserved = 0
    for key in table:
        totalObserved += table[key]

    if word in table:
        value = table[word]
    else:
        value = 0
    return float(value+1) / totalObserved

'''
spamdir = "./spam"
spam_table = create_freq_table(spamdir)
print prob_word_given_label("science", spam_table)
'''

def prob_spam_given_word(word, ham_table, spam_table):
    """
    use the Bayes theorem to calculate and return the conditional probability of an email being spam given that it contains a certain word.
    """
    word = word.lower()

    pws = prob_word_given_label(word, spam_table)
    pwh = prob_word_given_label(word, ham_table)
    return pws / (pws+pwh)

## https://en.wikipedia.org/wiki/Naive_Bayes_spam_filtering
def naive_bayes(line, ham_table, spam_table):
    ps = []
    for word in line.split(" "):
        ps.append(prob_spam_given_word(word, ham_table, spam_table))
    term1 = 1
    term2 = 1
    for p in ps:
        term1 *= p
        term2 *= 1 - p
    result = float(term1) / (term1 + term2)
    return result

'''
hamdir = "./ham"
spamdir = "./spam"
ham_table = create_freq_table(hamdir)
spam_table = create_freq_table(spamdir)
print prob_spam_given_word("science", ham_table, spam_table)
print naive_bayes('Our growing and ever evolving media company includes the weekly print edition website and other digital assets five signature annual events and mobile payments platform', ham_table, spam_table)
'''

def main():
    """
    creates the word frequency tables for ham and spam, then enters an infinite loop which gets user input, determines the probability that the message is spam, and prints the result.
    """
    hamdir = "./ham"
    spamdir = "./spam"
    ham_table = create_freq_table(hamdir)
    spam_table = create_freq_table(spamdir)
    while True:
        line = raw_input("please input sentences (no punctuation): ")
        print "probability of the suspect message being spam:", naive_bayes(line, ham_table, spam_table)

if __name__ == '__main__':
  main()
