import scrapetube
import pandas as pd
channelId = input("Enter the Youtube channel ID=")
list = []
url = "https://www.youtube.com/watch?v="
dataframe = pd.DataFrame(columns=["URL"])

videos = scrapetube.get_channel(channelId)
for video in videos:
    url1=url+str(video["videoId"])
    print(url1)
    list.append(url1)
dataframe["URL"] = list
dataframe.to_excel("MYURL.xlsx")