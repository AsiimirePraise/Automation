import tweepy
import schedule
import time
import random
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()

# Initialize Twitter API v2 Client
client = tweepy.Client(
    bearer_token=os.getenv('BEARER_TOKEN'),
    consumer_key=os.getenv('API_KEY'),
    consumer_secret=os.getenv('API_SECRET'),
    access_token=os.getenv('ACCESS_TOKEN'),
    access_token_secret=os.getenv('ACCESS_TOKEN_SECRET')
)

# List to store user-input quotes
user_quotes = []

def collect_quotes():
    print("\nEnter your quotes (type 'DONE' when finished):")
    while True:
        quote = input("> ")
        if quote.upper() == "DONE":
            break
        user_quotes.append(quote)
    print(f"\nCollected {len(user_quotes)} quotes")

def post_tweet():
    """Post a random user-provided tweet"""
    if not user_quotes:
        print("No quotes available to tweet!")
        return
    
    try:
        tweet_text = f"{user_quotes.pop(0)} | {datetime.now().strftime('%H:%M')}"
        response = client.create_tweet(text=tweet_text)
        print(f"   Tweeted: {tweet_text}")
        print(f"   Tweet ID: {response.data['id']}")
        print(f"   Quotes remaining: {len(user_quotes)}")
    except tweepy.TweepyException as e:
        print(f"Failed to post: {e}")

# Main Program
if __name__ == "__main__":
    # Step 1: Collect quotes from user
    collect_quotes()
    
    # Step 2: Verify Twitter authentication
    try:
        print("\n...Testing Twitter authentication...")
        test_response = client.create_tweet(text="Auth test - will delete")
        client.delete_tweet(test_response.data['id'])
        print("Authentication successful!")
    except Exception as e:
        print(f"Auth failed: {e}")
        exit()

    # Step 3: Schedule tweets
    print("\n...Setting up schedule...")
    schedule.every().day.at("09:00").do(post_tweet)  # 9 AM
    schedule.every().day.at("17:30").do(post_tweet)  # 5:30 PM
    schedule.every().day.at("20:00").do(post_tweet)  # 8 PM

    # Immediate first tweet
    print("\n...Posting first tweet now...")
    post_tweet()

    # Start scheduler
    print("\nTwitter Bot Active")
    print("Next scheduled tweets:")
    print("- 9:00 AM")
    print("- 5:30 PM")
    print("- 8:00 PM")
    print("Press Ctrl+C to stop")

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\nBot stopped gracefully.")
        if user_quotes:
            print(f"{len(user_quotes)} unsent quotes remaining")