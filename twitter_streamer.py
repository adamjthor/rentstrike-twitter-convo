from tweepy import Stream, OAuthHandler, StreamListener
import json
from time import sleep
from datetime import datetime
import boto3
from botocore.exceptions import NoCredentialsError



# Create the Listener object to listen to the incoming tweets
class listener(StreamListener):
	
	# Tell it what to do when it receives data
	def on_data(self, data):
		
		try:
			# Define 'tweet' as the json interpretation of the incoming string
			tweet = json.loads(data)

			# Print the tweet count & tweet text in the terminal 
			# and append it to a list of tweets that we create below
			print(len(tweets), tweet['user']['screen_name'], tweet['text'])
			tweets.append(tweet)

			# Once the tweet list gets to a certain length...
			if len(tweets) > N:
				# ...get the current datetime...
				now = datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S-%f')[:-3]
				# ...open a new file...
				filename = "tweet_stream_"+now+".json"
				f = open(directory+filename, "w")
				# ...dump the tweets into the file...
				json.dump(tweets, f)
				# ...close the file...
				f.close()
				# ... and reset the tweet list to empty
				tweets[:] = []
				print('Tweets saved to file', now)

				# Instantiate an s3 session
				s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
				# Try to upload the file to the s3 bucket
				try:
					s3.upload_file(directory+filename, s3_bucket_name, 'rs/'+filename)
					print('s3 upload successful')
				except FileNotFoundError:
					print('File not found')
				except NoCredentialsError:
					print('Credentials not available')

		except Exception as e:
			print(e)

	# Tell it what to do if it encounters an error receiving tweets
	def on_error(self, status):
		print(status)
		if status == 420:
			sleep(900) # wait 15mins if we get the error code re: Rate Limit Exceeded



# Define the max size of the tweet list and create the initial empty tweet list
N = 200
tweets = []

# Define AWS s3 credentials & directory/bucket info
ACCESS_KEY = 'your-access-key'
SECRET_KEY = 'your-secret-key'
directory = '/Users/your_username/Desktop/tweets/'
s3_bucket_name = 'your-s3-bucket-name'

# Define Twitter API credentials
ConsumerKey = 'your-consumer-key'
ConsumerSecret = 'your-consumer-secret'
AccessToken = 'your-access-token'
AccessTokenSecret = 'your-access-token-secret'

# These 2 lines create the authentication
auth = OAuthHandler(ConsumerKey, ConsumerSecret)
auth.set_access_token(AccessToken, AccessTokenSecret)

# Create the Stream object, which receives 2 objects:
# the authentication we just created, and an instance of the listener object we created
twitterStream = Stream(auth, listener())

# Tell the Stream object what to do. In this case, we filter it to a particular track.
track = ["rent strike", "rent withhold", "withhold rent", "landlord", "tenant"]
twitterStream.filter(track = track)
