#IMPORT REQUIRED PACKAGES
from googleapiclient.discovery import build
import pymongo
import mysql.connector
import pandas as pd
import streamlit as st

#CONNECT TO YOUTUBE API
api_key = "AIzaSyAUThD7w3WmT38dBAwgUIrXssLeUmyKfoU" 
youtube = build('youtube','v3',developerKey=api_key)

# get_channel_details
def get_channel_details(channel_id):
    ch_data = []
    response = youtube.channels().list(part = 'snippet,contentDetails,statistics',
                                     id= channel_id).execute()

    for i in range(len(response['items'])):
        data = dict(
                    Channel_id = channel_id[i],
                    Channel_name = response['items'][i]['snippet']['title'],
                    Playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'],
                    Views = response['items'][i]['statistics']['viewCount'],
                    Total_videos = response['items'][i]['statistics']['videoCount'],
                    Description = response['items'][i]['snippet']['description']
                    )
        ch_data.append(data)
    return ch_data

#get_playlist_details
def get_playlists_details(channel_id):
    playlists_data = []
    next_page_token = None
    while True:
        try:
            response = youtube.playlists().list(part="snippet",
                                                channelId=channel_id,
                                                maxResults=50,
                                                pageToken=next_page_token).execute()
            for playlist in response.get('items', []):
                playlist_id = playlist['id']
                playlist_name = playlist['snippet']['title']
                playlists_data.append({
                    'Playlist_id': playlist_id,
                    'Channel_id': channel_id,
                    'Playlist_name': playlist_name
                })
            next_page_token = response.get('nextPageToken')
            if next_page_token is None:
                break
        except Exception as e:
            print(f"Error: {e}")
            break
    return playlists_data

#get_video_id
def get_video_id(channel_id):
    video_ids = []
    res = youtube.channels().list(id=channel_id, 
                                  part='contentDetails').execute()
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    next_page_token = None
    
    while True:
        res = youtube.playlistItems().list(playlistId=playlist_id, 
                                           part='snippet', 
                                           maxResults=50,
                                           pageToken=next_page_token).execute()
        
        for i in range(len(res['items'])):
            video_ids.append(res['items'][i]['snippet']['resourceId']['videoId'])
        next_page_token = res.get('nextPageToken')
        
        if next_page_token is None:
            break
    return video_ids

#get_video_details
def get_video_details(v_ids):
    video_stats = []
    
    for i in range(0, len(v_ids), 50):
        response = youtube.videos().list(
                    part="snippet,contentDetails,statistics",
                    id=','.join(v_ids[i:i+50])).execute()
        for video in response['items']:
            video_details = dict(Channel_name = video['snippet']['channelTitle'],
                                Channel_id = video['snippet']['channelId'],
                                Video_id = video['id'],
                                Title = video['snippet']['title'],
                                Thumbnail = video['snippet']['thumbnails']['default']['url'],
                                Description = video['snippet']['description'],
                                Published_date = video['snippet']['publishedAt'],
                                Duration = video['contentDetails']['duration'],
                                Views = video['statistics']['viewCount'],
                                Likes = video['statistics'].get('likeCount'),
                                Dislikes = video['statistics'].get('dislikeCount'),
                                Comments = video['statistics'].get('commentCount'),
                                Favorite_count = video['statistics']['favoriteCount'],
                                Caption_status = video['contentDetails']['caption']
                               )
            video_stats.append(video_details)
    return video_stats

#get_comment_details
def comment_details(video_ids):
    comments = []
    for i in video_ids:
        try:
            request = youtube.commentThreads().list(part='snippet,replies',videoId=i,maxResults=100)
            response = request.execute()
            if len(response['items'])>0:
                for j in range(len(response['items'])):
                    comments.append({
                        'video_id': i,
                        'Comment_Author': response['items'][j]['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        'Comment_Text': response['items'][j]['snippet']['topLevelComment']['snippet']['textOriginal'],
                        'Comment_PublishedAt':response['items'][j]['snippet']['topLevelComment']['snippet']['publishedAt'].replace('Z',''),
                        'Comment_Likes': int(response['items'][j]['snippet']['topLevelComment']['snippet']['likeCount'])
                        })
                    
        except:
            comments.append(
            {'video_id':i,'Comment_Author':None,'Comment_Text':None,'Comment_PublishedAt':None,'Comment_Likes':None})
    return comments

#CREATE CONNECTION TO MONGODB
client=pymongo.MongoClient("mongodb+srv://monishar249:m0ngoDB249@cluster0.j6bz0lh.mongodb.net/?retryWrites=true&w=majority")

#CREATE YOUTUBE DATABASE IN MONGODB
db=client['youtube']

#insert channel details into MongoDB
def insert_channel_MDB(ch_id):
    ch_details = get_channel_details(ch_id)
    youtube_collection=db['channel']
    youtube_collection.insert_many(ch_details)

#insert playlist details into MongoDB
def insert_playlist_MDB(ch_id):
    play_det=get_playlists_details(ch_id)
    youtube_collection=db['playlist']
    youtube_collection.insert_many(play_det)

#insert video details into MongoDB
def insert_video_MDB(v_ids):
    vid_details=get_video_details(v_ids)
    youtube_collection=db['videos']
    youtube_collection.insert_many(vid_details)

#insert comment details into MongoDB
def insert_comment_MDB(v_ids):
    youtube_collection=db['comments']
    comment=comment_details(v_ids)
    youtube_collection.insert_many(comment)  

#insert_all_details_into_MongoDB
def insert_into_MONGODB(ch_id):
    insert_channel_MDB(ch_id)
    insert_playlist_MDB(ch_id)
    v_ids =get_video_id(ch_id)
    insert_video_MDB(v_ids)
    insert_comment_MDB(v_ids)

#CREATE CONNECTION TO SQL
mydb=mysql.connector.connect(host='localhost',user='root',password='12345',database='youtube')
mycursor=mydb.cursor()

#INSERT CHANNEL DETAILS INTO SQL
def insert_into_channels():
    collections = db['channel']
    query = """INSERT INTO channel(channel_id,channel_name,playlist_id,views,total_videos,description) VALUES(%s,%s,%s,%s,%s,%s)"""
    for i in collections.find({},{'_id' : 0}):
        mycursor.execute(query,tuple(i.values()))
    mydb.commit()

#INSERT PLAYLIST DETAILS INTO SQL
def insert_into_playlist():
    playlist_colle=db['playlist']
    query = """INSERT INTO playlist(playlist_id, channel_id, playlist_name) VALUES (%s, %s, %s)"""

    for i in playlist_colle.find({},{'_id' : 0}):
        mycursor.execute(query,tuple(i.values()))
    mydb.commit()

#INSERT VIDEOS DETAILS INTO SQL
def insert_into_videos():
    vid_colle=db['videos']
    query="""INSERT INTO videos(Channel_name,Channel_id,Video_id,Title,Thumbnail,Description,Published_date,Duration,Views,Likes,Dislikes,Comments,Favorite_count,Caption_status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    for i in vid_colle.find({},{'_id' : 0}):
        mycursor.execute(query,tuple(i.values()))
    mydb.commit()

#INSERT COMMENTS DETAILS INTO SQL
def insert_into_comments():
    comm_coll=db['comments']
    query = """INSERT INTO comments ( video_id , Comment_Author , Comment_Text , Comment_PublishedAt, Comment_Likes ) VALUES (%s, %s, %s, %s, %s)"""
    for i in comm_coll.find({},{'_id' : 0}):
        mycursor.execute(query,tuple(i.values()))
    mydb.commit()

#FUNCTION TO INSERT ALL DETAILS INTO YOUTUBE(SQL) DATABASE IN TABLE
def insert_into_sql():
    insert_into_playlist()
    insert_into_channels()
    insert_into_videos()
    insert_into_comments()

#streamlit

st.markdown("<h1 style='font-size:35px; color:red'>YOUTUBE DATA HARVESTING AND WAREHOUSING</h1>", unsafe_allow_html=True)
st.header("KEY SKILLS")
st.caption("Python scripting, Data Scraping, MongoDB, SQL")

channel_id=st.text_input("Enter channel ID")

if st.button("Extract and Store Data in MongoDB"):
    ch_ls=[]
    db=client["youtube"]
    ch_collection=db['videos']
    for data in ch_collection.find({},{"_id":0,'Channel_id':1}):
        ch_ls.append(data['Channel_id'])
    if channel_id in ch_ls:
        st.sucess("Channel_id already exist")
    else:
        upload=insert_into_MONGODB(channel_id)
        st.success("uploaded successfully")
         
if st.button("Transform to SQL"):
    s=insert_into_sql()
    st.success("transformed successfully")
         
questions = st.selectbox('Select Questions',
    ['1. What are the names of all the videos and their corresponding channels?',
    '2. Which channels have the most number of videos, and how many videos do they have?',
    '3. What are the top 10 most viewed videos and their respective channels?',
    '4. How many comments were made on each video, and what are their corresponding video names?',
    '5. Which videos have the highest number of likes, and what are their corresponding channel names?',
    '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
    '7. What is the total number of views for each channel, and what are their corresponding channel names?',
    '8. What are the names of all the channels that have published videos in the year 2022?',
    '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?',
    '10. Which videos have the highest number of comments, and what are their corresponding channel names?'])

if questions == '1. What are the names of all the videos and their corresponding channels?':
    mycursor.execute("""select title as video_name,channel_name from videos""")
    df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
    st.write(df)
        
elif questions == '2. Which channels have the most number of videos, and how many videos do they have?':
    mycursor.execute("""select total_videos, channel_name from channel order by total_videos desc limit 1""")
    df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
    st.write(df)
       
elif questions == '3. What are the top 10 most viewed videos and their respective channels?':
    mycursor.execute("""select title,channel_name from videos order by views desc limit 10""")
    df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
    st.write(df)

elif questions == '4. How many comments were made on each video, and what are their corresponding video names?':
    mycursor.execute("""select title,comments from videos""")
    df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
    st.write(df)

elif questions == '5. Which videos have the highest number of likes, and what are their corresponding channel names?':
    mycursor.execute("""select title, channel_name, likes from videos order by likes desc limit 1""")
    df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
    st.write(df)
        
elif questions == '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?':
    mycursor.execute("""select title, dislikes, likes from videos""")
    df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
    st.write(df)
         
elif questions == '7. What is the total number of views for each channel, and what are their corresponding channel names?':
    mycursor.execute("""select views, channel_name from channel """)
    df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
    st.write(df)

elif questions == '8. What are the names of all the channels that have published videos in the year 2022?':
    mycursor.execute("""SELECT DISTINCT channel_name FROM videos WHERE YEAR(published_date) = 2022""")
    df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
    st.write(df)

elif questions == '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?':
    mycursor.execute("""select channel_name, avg((REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(duration, 'M', 1), 'T', -1), '[^0-9]', '')*60) +(REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(duration, 'S', 1), 'M', -1), '[^0-9]', ''))) as duration_in_seconds from videos group by channel_name""")
    df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
    st.write(df)


elif questions == '10. Which videos have the highest number of comments, and what are their corresponding channel names?':
    mycursor.execute("""select title, comments from videos order by comments desc limit 1""")
    df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
    st.write(df)