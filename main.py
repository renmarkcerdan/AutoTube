"""
This is the main loop file for our AutoTube Bot!

Quick notes!
- Currently it's set to try and post a video then sleep for a day.
- You can change the size of the video currently it's set to post shorts.
    * Do this by adding a parameter of scale to the image_save function.
    * scale=(width,height)
"""

from datetime import date
import time
import os
from utils.CreateMovie import CreateMovie, GetDaySuffix
from utils.RedditBot import RedditBot
from utils.upload_video import upload_video
from scrape_video import startScraping

#Create Reddit Data Bot
redditbot = RedditBot()

# Leave if you want to run it 24/7
while True:
    today = date.today()
    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    data_path = os.path.join(dir_path, "data/")
    dt_string = today.strftime("%m%d%Y")
    data_folder_path = os.path.join(data_path, f"{dt_string}/")
    check_folder = os.path.isdir(data_folder_path)
    # If folder doesn't exist, then create it.
    if not check_folder:
        try:
            # Gets our new posts pass if image related subs. Default is memes
            posts = redditbot.get_posts("memes")

            # Create folder if it doesn't exist
            redditbot.create_data_folder()

            # Go through posts and find 5 that will work for us.
            for post in posts:
                redditbot.save_image(post)

            # Create the movie itself!
            CreateMovie.CreateMP4(redditbot.post_data)
            # Video info for YouTube.
            # This example uses the first post title.
            video_data = {
                    "file": "video.mp4",
                    "title": f"{redditbot.post_data[0]['title'].upper()}",
                    "description": "#shorts",
                    "keywords":"meme,reddit,Dankestmemes",
                    "privacyStatus":"public"
            }

            print(video_data["title"].upper())
            print("Posting Video in 1 minute...")
            time.sleep(10)
            upload_video(video_data)
        except Exception as e:
            print(f"Error Occured Creating Meme: {str(e)}")
    
    # while uploading meme lets start scraping video from tiktok
    startScraping() # uploading scraped video with 15mins interval

    # Sleep until ready to post another video!
    # time.sleep(60 * 60 * 24 - 1)
