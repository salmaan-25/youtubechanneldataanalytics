from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

api_key = 'AIzaSyDDrG65Wt6-07Jg3ZbGlEuXwqDYej7fg34'

channel_ids = {
    'UCKLXFXgvJ665OFySSDbbRaw',
    'UCvyZS6W6zMJCZBVzF-Ei6sw',
    'UCY6KjrDBN_tIRFT_QNqQbRQ',
    'UCHXLHapBVeJPHACQJGkHunw',
    'UCMiJRAwDNSNzuYeN2uWa0pA'
}

youtube = build('youtube', 'v3', developerKey=api_key)

def get_channel_stats(youtube, channel_ids):
    all_data = []
    request = youtube.channels().list(
        part='snippet,contentDetails,statistics',
        id=','.join(channel_ids)
    )
    response = request.execute()

    for i in range(len(response['items'])):
        data = dict(
            Channel_name=response['items'][i]['snippet']['title'],
            Subscribers=response['items'][i]['statistics']['subscriberCount'],
            Views=response['items'][i]['statistics']['viewCount'],
            Total_videos=response['items'][i]['statistics']['videoCount'],
            playlist_id=response['items'][i]['contentDetails']['relatedPlaylists']['uploads']
        )
        all_data.append(data)

    return all_data

channel_statistics = get_channel_stats(youtube, channel_ids)
channel_data = pd.DataFrame(channel_statistics)
channel_data['Subscribers'] = pd.to_numeric(channel_data['Subscribers'])
channel_data['Views'] = pd.to_numeric(channel_data['Views'])
channel_data['Total_videos'] = pd.to_numeric(channel_data['Total_videos'])

print(channel_data)
print(channel_data.dtypes)

sns.set(rc={'figure.figsize': (10, 8)})
ax = sns.barplot(x='Channel_name', y='Subscribers', data=channel_data)
plt.show()

# ---------------------
# GET PLAYLIST ID
# ---------------------
playlist_id = channel_data.loc[channel_data['Channel_name'] == 'Buying Facts', 'playlist_id'].iloc[0]

# ---------------------
# GET VIDEO IDS
# ---------------------
def get_video_ids(youtube, playlist_id):
    request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=playlist_id,
        maxResults=50
    )
    response = request.execute()

    video_ids = []
    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])

    next_page_token = response.get('nextPageToken')
    more_pages = True

    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()

            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])

            next_page_token = response.get('nextPageToken')

    return video_ids

video_ids = get_video_ids(youtube, playlist_id)
print(video_ids)

# ---------------------
# GET VIDEO DETAILS
# ---------------------
def get_video_details(youtube, video_ids):
    all_video_stats = []

    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part='snippet,statistics',
            id=','.join(video_ids[i:i+50])
        )
        response = request.execute()

        for video in response['items']:
            video_stats = dict(
                Title=video['snippet']['title'],
                Published_date=video['snippet']['publishedAt'],
                Views=int(video['statistics'].get('viewCount', 0)),
                Likes=int(video['statistics'].get('likeCount', 0)),
                Dislikes=0,  # YouTube API no longer provides this
                Comments=int(video['statistics'].get('commentCount', 0))
            )
            all_video_stats.append(video_stats)

    return all_video_stats  # Return the list of dicts

video_details = get_video_details(youtube, video_ids)
print(video_details)

# ---------------------
# CONVERT TO DATAFRAME
# ---------------------
video_data = pd.DataFrame(video_details)
print(video_data)

# Convert numeric columns to proper numeric format
df['Views'] = df['Views'].astype(str).str.replace(',', '').astype(float)
df['Likes'] = df['Likes'].astype(str).str.replace(',', '').astype(float)
df['Dislikes'] = df['Dislikes'].astype(str).str.replace(',', '').astype(float)
df['Comments'] = df['Comments'].astype(str).str.replace(',', '').astype(float)

video_data.to_csv('video_data.csv', index=False)


