import json
import boto3
import requests
from bs4 import BeautifulSoup
import os

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

S3_BUCKET = 'genius-bucket-654654514107'
DDB_TABLE = 'genius-table'
GENIUS_API_TOKEN = os.environ['GENIUS_API_TOKEN']

def scrape_lyrics(url):
    """Scrape lyrics from Genius song URL"""
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # Genius lyrics are often inside <div> with "data-lyrics-container"
    lyrics_divs = soup.find_all("div", {"data-lyrics-container": "true"})
    lyrics = "\n".join(div.get_text(separator="\n").strip() for div in lyrics_divs)
    
    return lyrics if lyrics else None

def lambda_handler(event, context):
    table = dynamodb.Table(DDB_TABLE)

    for record in event['Records']:
        body = json.loads(record['body'])
        title = body['title']
        artist = body['artist']
        track_id = body['track_id']
        
        headers = {'Authorization': f'Bearer {GENIUS_API_TOKEN}'}
        search_url = f"https://api.genius.com/search?q={title} {artist}"
        response = requests.get(search_url, headers=headers)
        json_resp = response.json()
        
        try:
            song = json_resp['response']['hits'][0]['result']
            song_url = song['url']
            lyrics = scrape_lyrics(song_url)

            if not lyrics:
                print(f"Lyrics not found for {title} by {artist}")
                continue
            
            result = {
                'track_id': track_id,
                'title': song['title'],
                'artist': song['primary_artist']['name'],
                'url': song_url,
                'lyrics': lyrics
            }

            # Store in S3
            object_key = f"lyrics/{track_id}.json"
            s3.put_object(
                Bucket=S3_BUCKET,
                Key=object_key,
                Body=json.dumps(result)
            )
            print(f"S3 updated: {object_key}")

            # Store in DynamoDB
            table.put_item(Item={
                'user_id': track_id,
                'title': result['title'],
                'artist': result['artist'],
                'url': result['url'],
                'lyrics': result['lyrics']
            })
            print(f"DynamoDB updated for {track_id}")

        except (IndexError, KeyError):
            print(f"No result found for {title} by {artist}")
            continue

    return {
        'statusCode': 200,
        'body': json.dumps('Lambda completed.')
    }
