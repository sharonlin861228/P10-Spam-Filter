# P10-Spam-Filter
CS301-10
Program Skills
Reading from text files
Using the os module to get system information
Constructing relative paths
Practice with dictionaries
Using a provided mathematical function (Naive Bayes)
Summary
Ever wonder how your email service got so good at picking out spam (Links to an external site.) messages? Well, it's got a lot of experience, and you're about to write a program that's ALSO going to have a lot of experience.

We've collected a bunch of unsolicited emails ("spam") and a bunch of real emails ("ham") - and by "a bunch", we mean 2000 of each. Rather than reading them yourself, you're going to write a program to read them and use what you learn from them to predict whether a new message is spam or ham!

Program Requirements
NOTICE: This program is NOT implementable using the repl.it environment. Yes, you do have to use Python on Your Computer this time.

For this program, we'll be giving you one function (naive_bayes()), and you'll implement five (5) other functions with the following names and behaviors:

update_freq_table(table, filename) - given the name of a file, add all occurrences of words in the file to the frequency table, which is a dictionary of {word : count}.
create_freq_table(dirname) - create a word frequency table (a dictionary) by scanning all the files under the given directory and updating the frequency table. Returns the frequency table.
prob_word_given_label(word, table) - returns the number of occurrences of the word in the table as a smoothed percentage of the total number of word occurrences in the table.
prob_spam_given_word(word, ham_table, spam_table) - use the Bayes theorem to calculate and return the conditional probability of an email being spam given that it contains a certain word.
main() - creates the word frequency tables for ham and spam, then enters an infinite loop which gets user input, determines the probability that the message is spam, and prints the result.
Provided function: Naive Bayes
First, you should copy this function directly into your code. Do not change it in any way - use it as provided.

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
Provided files: Ham and Spam
Here is a .zip file of the 2000 ham and 2000 spam training files. They're divided out into two subdirectories, appropriately named ham and spam. Your code should live at the same level as those two directories:

$ ls
ham/    spam/    spamfilter_hw.py
1. Update frequency table
Similar to the original demonstration we did in class with the dictionary histogram for counting letter occurrences, here you're updating a dictionary with word counts.

Key differences:

You will need to open and read a file to get the words you are counting.
All words should be letters only (use .isalpha() to help with this).
All words should be all lowercase (use .lower() to help with this).
You will not need to return any value from this function; all updates should be made to a shallow copy of the dictionary.

To test this function works correctly, you can try the following in the interactive interpreter (indicated by the ">>>" prompt - this is not part of your output!):

>>> test_table = {}
>>> directory = "./ham"
>>> filename = "5991.2002-02-07.williams.ham.txt"
>>> update_freq_table(test_table, directory+"/"+filename)
>>> print test_table
{'deal': 1, 'revised': 1, 'number': 1, 'parsing': 1, 'individual': 1, 
 'file': 1, 'scheduling': 1, 'portland': 1, 'txt': 1, 'interchange': 1, 
 'log': 1, 'no': 2, 'that': 1, 'awarded': 1, 'start': 2, 'detected': 1, 
 'unable': 1, 'ancillary': 1, 'final': 2, 'locate': 1, 'to': 1, 'schedule': 2, 
 'matches': 1, 'preferred': 2, 'cannot': 1, 'california': 1, 'schedules': 2, 
 'date': 2, 'a': 1, 'westdesk': 1, 'hour': 2, 'hourahead': 2, 'variances': 1, 
 'messages': 1, 'o': 1, 'assign': 1, 'iso': 1, 'the': 1, 'or': 1}
2. Create frequency table
Using the function that you just wrote, we now want to create a frequency table using the words from all of the files in one of the directories (spam or ham).

You can use the os.listdir() (Links to an external site.) function to get a list of all of the filenames in a given directory, and then loop through them to update the frequency table. Be careful: the filenames that you get from this function will still need their parent directory appended to their path!

Once you've created and updated this dictionary with all of the files, you should return it.

>>> spamdir = "./spam"
>>> spam_table = create_freq_table(spamdir)
>>> print len(spam_table)
35804
>>> print spam_table['science']
12
3. Word probability given a label
For this function, what we want to know is what percent of words observed in a given table are the word we're talking about. That is: what percent of spam words are "science"? What percent of ham words are "science"?

To account for the fact that we may encounter words that didn't show up in our training documents, we'll smooth this computation out by adding a fudge factor of one (since we don't want any words to have ZERO probability):

\frac{word\:freq+1}{total\:observed}
w
o
r
d
f
r
e
q
+
1
t
o
t
a
l
o
b
s
e
r
v
e
d

We've observed a lot of words, so you'll be returning some pretty small numbers.

>>> print prob_word_given_label("science", spam_table)
3.310845055e-05
4. Spam probability given word
Our last, and most crucial, calculation is to figure out how likely it is that a given word is part of a spam message. This function is a helper function for the naive_bayes() function that you copied into your code earlier; it calculates the probability that a given word indicates spam. (The naive_bayes() function combines all of those probabilities.)

This, however, is just a simple mathematical function (Links to an external site.):

\frac{P\left(word\mid spam\right)}{P\left(word\mid spam\right)+P\left(word\mid ham\right)}
P
(
w
o
r
d
∣
s
p
a
m
)
P
(
w
o
r
d
∣
s
p
a
m
)
+
P
(
w
o
r
d
∣
h
a
m
)

That is, to determine the probability that a given word is spam, you'll need to call your word_given_label() function for this word given both the spam and ham dictionaries. Combine them following the expression above and return that value as a float, and let the naive_bayes() function do the rest!

>>> print prob_spam_given_word('science', ham_table, spam_table)
0.639023665239
>>> print naive_bayes('Our growing and ever evolving media company includes the weekly print edition website and other digital assets five signature annual events and mobile payments platform', ham_table, spam_table)
0.996427640276
5. Main function
Your main function should contain the spam and ham directories as relative paths ("./spam" and "./ham" respectively), create the frequency tables using your functions, and then repeatedly prompt the user for messages to filter using the naive_bayes() function and display the results:

please input sentences (no punctuation): Our growing and ever evolving media company includes the weekly print edition website and other digital assets five signature annual events and mobile payments platform
probability of the suspect message being spam: 0.996427640276
please input sentences (no punctuation): Please circulate the following announcement regarding the search for a Computer Science assistant professor I have also attached a document for easy distribution Thank you
probability of the suspect message being spam: 4.1170479502e-05
...
Note that it is not imperative that you match these values directly, but rather that your program correctly labels spam (>.5) and ham (<.5).

Here are some test ham phrases:

Please circulate the following announcement regarding the search for a Computer Science assistant professor I have also attached a document for easy distribution Thank you
Monday is holiday There will be multiple celebrations in the town This year the company is sponsoring one at Union South including free lunch
i realize that many of you will be working over the new year s week end to ensure a smooth transaction into the new year in advance i truly appreciate all of the efforts
and some test spam phrases:

Our growing and ever evolving media company includes the weekly print edition website and other digital assets five signature annual events and mobile payments platform
ENJOY THIS BLIZZARD OF WELCOME BACK SPECIALS ON THE LAST FEW LOCATIONS AND EARN A FREE UPGRADE SIGNING BONUS OR RENT SPECIAL AT SELECT LOCATIONS
These great houses and apartments wont last long Our residents enjoy Free online rent payment Professional management 24 hour emergency maintenance Amazing location in the middle of everything
Commenting Your Code
As with last week's program, every function you write is required to include a docstring, and you must also write comments in your code.

Handing In Your Program
Students completing this program in pairs should join a P10 Group. If you are having trouble joining (not creating!) a P10 Group, please contact Hobbes with your partner's name.

When you're done, upload all functions in a file called spamfilter_hw.py.
