from rauth import OAuth1Service
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_protect
import nltk
import re
from instamojo import *

twitter = OAuth1Service(
		name='twitter',
		consumer_key='EGeDjo0UzJPrKYuFnwKw',
		consumer_secret='2KxZ5UC5ZEGRSwra2uEtG3FfxccPRnP2U0Sbx8c',
		request_token_url='https://api.twitter.com/oauth/request_token',
		access_token_url='https://api.twitter.com/oauth/access_token',
		authorize_url='https://api.twitter.com/oauth/authorize',
		base_url='https://api.twitter.com/1.1/')
 
request_token, request_token_secret = twitter.get_request_token()
authorize_url = twitter.get_authorize_url(request_token)


class Offer:
     def __init__(self, title, description, price , currency):
        self.title = title
        self.description = description
        self.price = price
        self.currency = currency
       
def userenter(request):
	return TemplateResponse(request, 'enter.html', {"URL" : authorize_url  })
	
@csrf_protect 
def gettweets(request):
	user = request.POST['user']
	pin = request.POST['pin']
	session = twitter.get_auth_session(request_token,
									request_token_secret,
									method='POST',
									data={'oauth_verifier': pin})
 
	params = {'screen_name': user,  # Screen Name of teh User
			'count': 5}       # 5 tweets
 
	r = session.get('statuses/user_timeline.json', params=params, verify=True)
    
	tweets = []
	for i, tweet in enumerate(r.json(), 1):
		tweets.append(tweet['text'])
		
	return TemplateResponse(request, 'tweets.html', {"User" : user ,"Tweets" :tweets })
	
	

'''
In this method we break the tweet in sentences and 
Parses the sentences and attaches tags like 
(S (GPE Soul/NNP) is/VBZ (NP the/DT title/NN))
(S You/PRP regain/VBP your/PRP$ Soul/NNP)
(S 50/CD Rs/NNS)

For a Sample tweet : 
Soul  is the title. You regain your Soul.50 Rs

It gets the following things : 
Title :Soul
Description : You regain your Soul
Currency :INR
Price:50

'''
def getDetailsNLTK(tweet):
	ar = tweet.split('.')
	tokens  =  nltk.word_tokenize(tweet)
	pattern = "NP: {<DT>?<JJ>*<NN>}" #  a tag pattern of an NP chunk
	'''
	 defines a common NP pattern, i.e., an optional determiner (DT) followed by any 
	 number of adjectives (JJ) and then a noun (NN) 
	'''
	NPChunker = nltk.RegexpParser(pattern) # create a chunk parser 
	title = 'Not Enough Data'
	description = ''
	price = 'Not Found'
	currency = 'Not Found'
	
	for sentence in ar:
		tokens = nltk.word_tokenize(sentence)		
		tagged = nltk.pos_tag(tokens)
		entities = nltk.chunk.ne_chunk(tagged)
		result = NPChunker.parse(entities) # parse the example sentence
		print str(result)
		if 'title' in sentence.lower():
			title = ''
			elts = str(result).split()
			for elt in elts:
				#print elt
				words = elt.split('/')
				#for word in words:
					#print word
				if len(words) ==2:
					#print words[0] + " tag:"+ words[1]
					if words[0].lower() != "title" :
						if 'NNP' in str(words[1]) :
							title += words[0]+" " 
		elif '/CD' not in str(result)  :
			description += sentence 
			#Description can be multiple lines but 
			#wont have a Price or currency in that sentence
		else:
			p = re.compile('\d+')
			price = int(p.findall(sentence)[0])
			if 'INR' in sentence.upper() :
				currency = 'INR'
			elif 'RS' in sentence.upper() :
				currency = 'INR'		
			else:
				currency = 'USD'
			
		
		
	print "Title :" +title
	print "Description :" +description
	print "Currency :" +currency
	print "Price:" +str(price)
	offer = Offer (title ,  description , price , currency )
	return offer



'''
This method simply splits the sentence into 3 parts:
First being the Title, Second Description, 3rs gives
the price and the Currency.

For a Sample tweet : 
Soul  is the title. You regain your Soul.50 Rs

It gets the following things : 
Title : Soul  is the title
Description : You regain your Soul
Currency :INR
Price:50
'''

def getDetailsSimple(tweet):
	ar = tweet.split('.')
	if len(ar)>=3 :
		title = ar[0]
		description = ar[1]
		p = re.compile('\d+')
		price = int(p.findall(ar[2])[0])
		if 'INR' in ar[2].upper() :
			currency = 'INR'
		elif 'RS' in ar[2].upper() :
			currency = 'INR'		
		else:
			currency = 'USD'
		
		
		print "Title :" +title
		print "Description :" +description
		print "Currency :" +currency
		print "Price:" +str(price)
		offer = Offer (title ,  description , price , currency )
	else :
		offer = Offer ("Not Enough Data" ,  "Not Found" , "Not Found" ,"Not Found" )
	return offer
    


@csrf_protect 
def createoffer(request):
	tweet = request.POST['checkboxArray[]']
	offers=[]
	''' 
	Two methods created for getting details from tweet 
	one is the simple method that uses String operations 
	
	and 
	
	The other one uses the NLTK - natural Language Tool Kit 
	That tries to find out the Noun Phases, (Nouns Adjectives Determiners)
	to get the title, Description, cost and currency from the tweet.
	
	Here I am using the NLTK one thats more intuitive
	'''
	
	offers.append(getDetailsNLTK(tweet))
	
	#createoffer_instamojo(getDetailsNLTK(tweet))
	return TemplateResponse(request, 'offer.html', {"Offers" : offers })


'''
It uses offer_create from instamojo to create offers 

I'am having issues with the authentication for which I 
have mailed the support@instamojo

'''	
def createoffer_instamojo(offer):
	dict = {'title' : offer.title,'description' : offer.description , 'currency' : offer.currency , 'price' : offer.price  }
	
	#Add code from Instamojo App
	#to create app using this Dict

	