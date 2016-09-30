import csv

def replace_two_or_more(s):
	# add words to a set
	a = set(s.split())
	#convert set to list
	return list(a)

#function to clean the tweet
def process_tweet(tweet):
	# Convert to lower case
	tweet = tweet.lower()
	tweets = replace_two_or_more(tweet)
	feature_vector = []
	for word in tweets:
		#remove punctuations symbols
		word = word.strip()
		word = word.replace("\'", "")
		word = word.replace("\\", "")
		word = word.replace("?", "")
		word = word.replace(".", "")
		word = word.replace("!", "")
		word = word.replace("\"", "")
		word = word.replace(",", "")
		word = word.replace("\'", "")
		word = word.replace(")", "")
		word = word.replace("(", "")
		word = word.replace("[", "")
		word = word.replace("]", "")
		#ignore some text
		if ((word in stopwords) or (word.startswith("@")) or (
				word.startswith("&")) or (word.startswith("www")) or (
				word.startswith("#")) or (word.startswith("http")) or (
		word.isdigit())):
			continue
		else:
			#add to feature_vector if word is formatted
			feature_vector.append(word.lower())
	return feature_vector



#function to find max element key in a dictionary
def find_max(mydict):
	return max(mydict, key=mydict.get)


stop_words = []


# start getStopWordList
def get_stop_word_list(stop_word_list_file_name):
	fp = open(stop_word_list_file_name, 'r')
	line = fp.readline()
	while line:
		word = line.strip()
		stop_words.append(word)
		line = fp.readline()
	fp.close()
	return stop_words


# end

total_words = 0
total_sentimental_occurences = {'0': 0, '2': 0, '4': 0}
feature_list = {}

#get probability of occurence of a feature if it belongs to a certain class - P(feature|class)
def get_prob_features_under_class(feature_vector, sentiment):
	result = 1
	counter = 0
	for word in feature_vector:
		if word in feature_list:
			counter = 1
			if total_sentimental_occurences[sentiment] != 0:
				result *= feature_list[word][sentiment] / total_sentimental_occurences[sentiment]
			else:
				return 0
	if counter == 0:
		return 0
	return result

#get probability of occurence of a certain class - P(class)
def get_prob_class(sentiment):
	result = total_sentimental_occurences[sentiment] / total_words
	return result

#get probability of occurence of a certain feature - P(feature)
def get_prob_features(feature_vector):
	result = 1.0000
	counter = 0
	for feature in feature_vector:
		if feature in feature_list:
			counter = 1
			result *= feature_list[feature]['count'] / total_words

	if counter == 0:
		return 0
	return result

#predict nature of a sentence according to its feature vector
def predict(feature_vector):
	prob_acc_to_sentiments = {}
	prob_of_features = get_prob_features(feature_vector)
	if prob_of_features == 0:
		print("No Data - you gotta train me more!")
		return
	#calculating probability of occuring of sentence in each class
	for sentiment in total_sentimental_occurences:
		# P(class|features) = P(features|class)*P(class)/P(features)
		prob_acc_to_sentiments[sentiment] = get_prob_features_under_class(feature_vector, sentiment) * \
		get_prob_class(sentiment) / prob_of_features
	#find class with maximum probability
	result = find_max(prob_acc_to_sentiments)
	key = result
	if result == '4':
		result = "Positive"
	elif result == '0':
		result = "Negative"
	else:
		result = "Neutral"
	print("The sentence is ", result)
	return key


# Read the tweets one by one and process it
inp_tweets = csv.reader(open('test.csv', 'r'), delimiter=',', quotechar='\"', )
stopwords = get_stop_word_list('stopwordsList.txt')
tweets = []
print("Training started .....")
for row in inp_tweets:
	#first element in given dataset gives sentiment and 6th gives the actual tweet
	sentiment = row[0]
	tweet = row[5]
	#extract feature vector from a tweet by cleaning it
	feature_vector = process_tweet(tweet)
	for feature in feature_vector:
		if not feature in feature_list:
			#if a word is not in currently maintained list , then add it
			feature_list[feature] = {'0': 0, '2': 0, '4': 0, 'count': 0}
		#increment the sentiment count  of the word
		feature_list[feature][sentiment] += 1
		feature_list[feature]['count'] += 1
		total_sentimental_occurences[sentiment] += 1
		total_words += 1
print("Training complete.")
print("Total Words - ", total_words)
print("Total classifications", total_sentimental_occurences)

while True:
	#input a sentence from user and predict its nature
	tweet = input("Enter a sentence : ")
	feature_vector = process_tweet(tweet)
	predict(feature_vector)
