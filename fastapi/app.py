from flask import Flask,request,redirect,render_template
import requests



app=Flask(__name__)
YOUTUBE_API_KEY='AIzaSyAK3QWk00zPYQYg5R91knN-qUcBktD940A'

@app.route('/',methods=['GET','POST'])
def index():
    search_url='https://www.googleapis.com/youtube/v3/search'
    video_url='https://www.googleapis.com/youtube/v3/videos'
    videos=[]


    if request.method=='POST':
        search_params={
            'key':YOUTUBE_API_KEY,
            'q':request.form.get('search'),
            'part':'snippet',
            'maxResults':3,
            'type':'video'

         }
        res=requests.get(search_url,params=search_params)
        results=res.json()['items']
        video_ids=[]
        for result in results:
            video_ids.append(result['id']['videoId'])
        video_params={
            'key':YOUTUBE_API_KEY,
            'id': ','.join(video_ids),
            'part':'snippet,contentDetails,statistics',
            'maxResults':3
        }

        r=requests.get(video_url,params=video_params)
        results2=r.json()['items']
        for result in results2:
            video_data={
                'id':result['id'],
                'url':'https://www.youtube.com/watch?v='+result['id'],
                'thumbnail': result['snippet']['thumbnails']['high']['url'],
                'duration':result['contentDetails']['duration'],
                'counts':result['statistics']['viewCount'],
                'title':result['snippet']['title']
            }
            videos.append(video_data)

    return render_template('index.html',videos=videos)




    
if __name__=='__main__':
    app.run(debug=True)

   

    