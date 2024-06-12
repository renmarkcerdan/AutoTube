from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import requests
import random
import os
import json
from urllib.request import urlopen
from utils.upload_video import upload_video
import moviepy.editor as mp
import moviepy.video.fx.all as vfx
from googleapiclient.errors import HttpError

def downloadVideo(link, id):
    tiktokID = link.split("/")[-1]

    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    data_path = os.path.join(dir_path, "AutoTube/data/")
    already_posted = []

    #   Check for a posted_already.json file
    posted_already_path = os.path.join(data_path, "tiktok_posted.json")

    if not os.path.isfile(posted_already_path):
        os.makedirs(posted_already_path)

    print("Loading tiktok_posted.json from data folder.")
    with open(posted_already_path, "r", encoding='utf-8') as file:
        already_posted = json.load(file)

    if tiktokID not in already_posted:
        print(f"Downloading video {id} from: {link}")
        cookies = {
            'cf_clearance': '9YXSwJYOP0eQJxdqf3TclHiICvYlXTE4OS456Q2V4ag-1709732372-1.0.1.1-PiDx2R.Q4Djxga2ucFrDJn1ef_QgYANVbxQmxyUs1ETzbwUMZqAGNkj_1Kl2CwN8dP42_i_2XLxGOLtXWGSodQ',
            '_ga': 'GA1.1.1424394371.1709732387',
            '__gads': 'ID=2f0f944e7b03ca9b:T=1709732394:RT=1709732394:S=ALNI_MblRhJkmQhfxJ3iJ4aOZ-hBAq9MUA',
            '__gpi': 'UID=00000d294a66f412:T=1709732394:RT=1709732394:S=ALNI_MZDZBn6LMCMfbnELSgdZvk_HjlOFw',
            '__eoi': 'ID=fa73c6365f15f3c1:T=1709732394:RT=1709732394:S=AA-Afjaav9lSzuxPhfbRRX_AMnBZ',
            'FCNEC': '%5B%5B%22AKsRol8I7Mj3zdUWS-tdUw-M-alQ0sOVt9Qq3_7S3_1pBw0fHbaEGtf67ZFuGghx8XqseGT89baOnn7NMnFFFc9WW-5ECCCoQzal1xOxev-cj7Ztsp69fZtakYFYU0ory80hVvhE13O4GoKAse1ByJiGKWLYaA_ESQ%3D%3D%22%5D%5D',
            '_ga_ZSF3D6YSLC': 'GS1.1.1709732387.1.1.1709732425.0.0.0',
        }

        headers = {
            'authority': 'ssstik.io',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-PH,en-US;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
            # 'cookie': 'cf_clearance=9YXSwJYOP0eQJxdqf3TclHiICvYlXTE4OS456Q2V4ag-1709732372-1.0.1.1-PiDx2R.Q4Djxga2ucFrDJn1ef_QgYANVbxQmxyUs1ETzbwUMZqAGNkj_1Kl2CwN8dP42_i_2XLxGOLtXWGSodQ; _ga=GA1.1.1424394371.1709732387; __gads=ID=2f0f944e7b03ca9b:T=1709732394:RT=1709732394:S=ALNI_MblRhJkmQhfxJ3iJ4aOZ-hBAq9MUA; __gpi=UID=00000d294a66f412:T=1709732394:RT=1709732394:S=ALNI_MZDZBn6LMCMfbnELSgdZvk_HjlOFw; __eoi=ID=fa73c6365f15f3c1:T=1709732394:RT=1709732394:S=AA-Afjaav9lSzuxPhfbRRX_AMnBZ; FCNEC=%5B%5B%22AKsRol8I7Mj3zdUWS-tdUw-M-alQ0sOVt9Qq3_7S3_1pBw0fHbaEGtf67ZFuGghx8XqseGT89baOnn7NMnFFFc9WW-5ECCCoQzal1xOxev-cj7Ztsp69fZtakYFYU0ory80hVvhE13O4GoKAse1ByJiGKWLYaA_ESQ%3D%3D%22%5D%5D; _ga_ZSF3D6YSLC=GS1.1.1709732387.1.1.1709732425.0.0.0',
            'if-modified-since': 'Wed, 06 Mar 2024 13:00:35 GMT',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version': '"122.0.6261.94"',
            'sec-ch-ua-full-version-list': '"Chromium";v="122.0.6261.94", "Not(A:Brand";v="24.0.0.0", "Google Chrome";v="122.0.6261.94"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"macOS"',
            'sec-ch-ua-platform-version': '"12.7.2"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }

        params = {
            'url': 'dl',
        }

        data = {
            'id': link,
            'locale': 'en',
            'tt': 'VDM3NUJh', # NOTE: This value gets changed, please use the value that you get when you copy the curl command from the network console
        }

        print("STEP 4: Getting the download link")
        print("If this step fails, PLEASE read the steps above")
        response = requests.post('https://ssstik.io/abc?url=dl', cookies=cookies, headers=headers, data=data)
        downloadSoup = BeautifulSoup(response.text, "html.parser")

        downloadLink = downloadSoup.a["href"]
        videoTitle = downloadSoup.p.getText().strip()

        dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        data_path = os.path.join(dir_path, "AutoTube/videos/")
        video = os.path.join(data_path, f"{videoTitle}.mp4")
        tempVideo = os.path.join(data_path, "video.mp4")
        print("STEP 5: Saving the video :)")

        mp4File = urlopen(downloadLink)
        # Feel free to change the download directory
        try:
            with open(f"{video}", "wb") as output:
                while True:
                    data = mp4File.read()
                    if data:
                        print("STEP 5.1: Currently Writing the file..")
                        output.write(data)
                        time.sleep(10)
                        clip = mp.VideoFileClip(f"{video}")
                        duration = clip.duration
                        if(duration > 60):
                            clip = clip.subclip(0, 60)
                            print("STEP 5.2: Subclip processing..")
                            
                        # clip.write_videofile(f"{newName}")
                        clip.write_videofile(f"{tempVideo}", fps = 30)
                        os.remove(video)
                        # clip = mp.VideoFileClip(f"{newName}")

                        time.sleep(10)
                        clip = mp.VideoFileClip(f"{tempVideo}")
                        (w, h) = clip.size
                        crop_width = h * 9/16
                        x1, x2 = (w - crop_width)//2, (w+crop_width)//2
                        y1, y2 = 0, h
                        clip = vfx.crop(clip, x1=x1, y1=y1, x2=x2, y2=y2)
                        # newClip = vfx.crop(newClip, x1=0, y1=0, width=1080, height=1980)
                        clip.write_videofile(f"{video}", fps = 30)
                        if os.path.exists(tempVideo):
                            os.remove(tempVideo)
                            
                        if os.path.exists(video):
                            print("STEP 5.3: Oyea File is done and ready to upload!")
                            tiktokUser = link.split("/")[3]
                            video_data = {
                                "file": f"{video}",
                                "title": f"{videoTitle}",
                                "description": f"#shorts {tiktokUser}",
                                "keywords":"meme,reddit,Dankestmemes,comdey,tiktok,tiktokvideos",
                                "privacyStatus":"public"
                            }
                            error = None;
                            try:
                                upload_video(video_data) 
                            except HttpError as e:
                                error = f"{e.content.error.reason}"
                            if error is not None:
                                print(f"{error} trying to re-upload the video..")
                                response = None
                                retry = 0
                                while response is None:
                                    upload_video(video_data)
                                    retry += 1
                                    if retry > 10:
                                        exit("No longer attempting to retry.")
                                    max_sleep = 2 ** retry
                                    sleep_seconds = random.random() * max_sleep
                                    print("Sleeping %f seconds and then retrying..." % sleep_seconds)
                                    time.sleep(sleep_seconds)

                            already_posted.append(tiktokID)
                            with open(posted_already_path, "w") as outfile:
                                json.dump(already_posted, outfile)
                            print("STEP 6: Hoof! Glad it works! time for the next video after 15mins!")
                            os.remove(video)
                            time.sleep(60 * 5) # 5mins interval
                    else:
                        break
        except Exception as e:
            print(f"Error Occured on Tiktok Scraping: {str(e)}")
            # print(f"Error Occured on Tiktok Scraping: {str(e)} \n See you tomorrow!")
            # time.sleep(60 * 60 * 24 - 1)

def startScraping():
    print("STEP 1: Open Chrome browser")
    options = Options()
    options.add_argument("start-maximized")
    # options.add_argument('--headless')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options)
    # Change the tiktok link
    driver.get("https://www.theendlessmeal.com/easy-vegetarian-chili-recipe/")

    # IF YOU GET A TIKTOK CAPTCHA, CHANGE THE TIMEOUT HERE
    # to 60 seconds, just enough time for you to complete the captcha yourself.
    time.sleep(60)

    scroll_pause_time = 1
    screen_height = driver.execute_script("return window.screen.height;")
    i = 1

    print("STEP 2: Scrolling page")
    while True:
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        i += 1
        time.sleep(scroll_pause_time)
        scroll_height = driver.execute_script("return document.body.scrollHeight;")  
        if (screen_height) * i > scroll_height:
            break 

    # this class may change, so make sure to inspect the page and find the correct class
    className = "dpsp-pin-it-wrapper"
    urlsToDownload = []
    script  = "let l = [];"
    script += "Array.from(document.getElementsByClassName(\""
    script += className
    script += "\")).forEach(item => { l.push(item.querySelector('img').src)});"
    script += "return l;"

    urlsToDownload = driver.execute_script(script)

    print(f"STEP 3: Time to download {len(urlsToDownload)} videos")
    for index, url in enumerate(urlsToDownload):
        print(f"Downloading video: {index}")
        # downloadVideo(url, index)
        time.sleep(10)