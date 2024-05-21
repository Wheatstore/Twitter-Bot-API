import requests
import json
from bs4 import BeautifulSoup
import time

tweets_count = 0

current_headlines = []
new_headlines = []
# Function to send tweet
def send_tweet(new_headline):
    # Twitter API endpoint

    url = "https://api.twitter.com/2/tweets"

    payload = json.dumps({
    "text": f"{new_headline} \n #AI #Politics #News"
    })
    headers = {
        'Content-Type': '',
        'Authorization': '"',
        'Cookie': ''
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


# Function to check for new headlines
def check_for_new_headlines(new_headlines_list):
    global current_headlines
    global tweets_count

    # Compare with previous headlines and tweet new ones
    for headline in new_headlines_list:
        if headline not in current_headlines and tweets_count < 6:
            current_headlines.append(headline)
            #send_tweet(headline)
            tweets_count += 1
        elif tweets_count >= 5:
            print("Maximum tweets reached.")
            tweets_count = 0
            break
        else:
            print(f"Existing Headline found: {headline}")

def get_cnbc_headlines():
    global current_headlines
    global new_headlines

    url = "https://www.cnbc.com/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        for headline in soup.find_all('a', class_='LatestNews-headline'):
            new_headlines.append(headline.text.strip())
        return new_headlines
    else:
        print("Failed to retrieve CNBC headlines.")
        return []

def get_nbc_headlines():
    global new_headlines

    url = "https://www.nbcnews.com/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        headlines = soup.find_all("h2", class_="styles_teaseTitle__H4OWQ")


        for headline in headlines:
            new_headlines.append(headline.text.strip())

        return new_headlines
    else:
        print("Unable to access the site")


while True:
    get_nbc_headlines()
    get_cnbc_headlines()
    with open('wepage.txt', 'w') as file:
        file.write(str(new_headlines[0:5]))
    check_for_new_headlines(new_headlines)
    print(f"Tweet Count = {tweets_count}")
    time.sleep(7200)
