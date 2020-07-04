# rentstrike-twitter-convo
A Twitter scrape and analysis of the conversation around rent strikes during COVID-19.

1. (twitter_streamer.py) Scrape 1-week of tweets in the heat of the rent strike movement. Tweets contained the terms "rent strike", "rent withhold", "withhold rent", "landlord", "tenant". 2 GB of tweets were scraped and funneled directly to an AWS S3 bucket.
2. Parse the JSON data into CSV format for analysis. (FUTURE STEP)
3. NLP & topic clustering to identify major themes. (FUTURE STEP)
4. Map the conversation networks to identify major groups of users engaged in discussion. (FUTURE STEP)
