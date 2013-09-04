Instamojo : Tweet to Offer Creation Django App

Installs Required :

1) NLTK
2) docopt

First in this APP we have to enter the Screen_Name of the User whose Tweets we want to check.
Twitter Api now doesn't allow to access tweets directly so we have to do the authorization first.

After Authorizing we get the tweets of the User and we choose which tweets we want to make an Instamojo
offer.

We Select the one and the page represents how the tweets were scraped to form an Offer.


Two methods created for getting details from tweet 
	1) simple method that uses String operations ,and 
	
	2) The other one uses the NLTK - natural Language Tool Kit 
	That tries to find out the Noun Phases, (Nouns Adjectives Determiners)
	to get the title, Description, cost and currency from the tweet.
	
	In the view I have used the NLTK one that's more intuitive
	
Though the NLTK one might be buggier than the String Manipulation one coz that works on intuition
where as in the string operations one we might have to tell user to tweet for an offer in a specified format.

After this we create the app using Instamojo Api's