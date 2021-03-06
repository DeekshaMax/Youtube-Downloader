import os
import re
import time
import urllib.error
import urllib.request

import pafy
from pytube import YouTube


def getPageHtml(url):
    try:
        yTUBE = urllib.request.urlopen(url).read()
        return str(yTUBE)
    except urllib.error.URLError as e:
        print(e.reason)
        exit(1)


def getPlaylistUrlID(url):
    if 'list=' in url:
        eq_idx = url.index('=') + 1
        pl_id = url[eq_idx:]
        if '&' in url:
            amp = url.index('&')
            pl_id = url[eq_idx:amp]
        return pl_id
    else:
        print("Veronica => ", url, "is not a youtube playlist. <-_->")
        exit(1)


def getFinalVideoUrl(vid_urls):
    final_urls = []
    for vid_url in vid_urls:
        url_amp = len(vid_url)
        if '&' in vid_url:
            url_amp = vid_url.index('&')
        final_urls.append('http://www.youtube.com/' + vid_url[:url_amp])
    return final_urls


def printVideoTitle(vid_urls):
    i = 1
    for url in vid_urls:
        video = pafy.new(url)
        print(i, ". ", video.title, " => ", url)
        i += 1


def getPlaylistVideoUrls(page_content, url):
    playlist_id = getPlaylistUrlID(url)

    vid_url_pat = re.compile(r'watch\?v=\S+?list=' + playlist_id)
    vid_url_matches = list(set(re.findall(vid_url_pat, page_content)))

    if vid_url_matches:
        final_vid_urls = getFinalVideoUrl(vid_url_matches)
        print("\nVeronica => Found", len(final_vid_urls), "videos in playlist. {^$^}")
        printVideoTitle(final_vid_urls)
        return final_vid_urls
    else:
        print('\nVeronica => No videos found. <-_->')
        exit(1)


# function added to get audio files along with the video files from the playlist

def download_Video_Audio(directoryPath, vid_url, quality):
    try:
        video = pafy.new(vid_url)
    except Exception as e:
        print("\nVeronica => T_T Error:", str(e), "- Skipping Video with url '" + str(vid_url) + "'.")
        return

    streams = video.streams
    fileTitle = video.title

    # print(os.path.exists(directoryPath+'/'+fileTitle+'.mp4'))

    # to check it file exist or not
    if os.path.exists(directoryPath + '/' + fileTitle + '.mp4'):
        print("\nVeronica => Seems like ", fileTitle, "already exists in this directory! So, I am skipping video...")
        return

    print("\nVeronica => ^_^ downloading, ", fileTitle + " video")

    print("\nVeronica => Found these qualites")

    for i in streams:
        print("Veronica => ", i)

    print("\nVeronica => Downloading the normal(video+audio) with mp4 extension")

    for vid in streams:
        # print(vid.mediatype=='normal' , vid.extension=='mp4' , str(quality) in vid.quality)
        if (vid.mediatype == 'normal' and vid.extension == 'mp4'):
            if str(720) == str(quality) and str(720) in vid.quality:
                vid.download(directoryPath)
                break
            elif str(640) == str(quality) and str(640) in vid.quality:
                vid.download(directoryPath)
                break
        # downloading subtitle too.
        try:
            yt = YouTube(vid_url)
            caption = yt.captions.get_by_language_code('en')
            # print(str(caption.generate_srt_captions()))
            # '''
            fileSubTitlePath = directoryPath + '/' + fileTitle + '.srt'
            file1 = open(fileSubTitlePath, "w")  # write mode

            file1.write(str(caption.generate_srt_captions()))
            file1.close()
            # '''
        except Exception:
            print("\nVeronica => Seems like subtitle not available for ", fileTitle, " So, I am skipping subtitile...")

        print("\nVeronica => Successfully downloaded", fileTitle, "!")


if __name__ == '__main__':
    print("\nWelcome to Youtube Video Downloader.")
    print("\nHello, I am Veronica \(^_^)/, your Assistant.")
    print("\nVeronica => What would you like to download?")

    print("\nVeronica => 1. Video \nVeronica => 2. Playlist")
    print("User => ", end="")
    choice = int(input())
    if choice == 1:
        print("\nVeronica => Enter video url")
        print("User => ", end="")
        url = input()
        url = url.replace(" ", "")
        # url ="https://www.youtube.com/playlist?list=PLqM7alHXFySH8VivqUPnNFJ0kxgzgHrVb"

        print("\nVeronica => Enter prefered quality of video (640p/720p)")
        print("User => ", end="")
        quality = input()
        # quality=720

        print("\nVeronica => Enter directory url")
        print("User => ", end="")
        directory = input()

        # make directory if dir specified doesn't exist
        try:
            os.makedirs(directory, exist_ok=True)
        except OSError as e:
            print(e.reason)
            exit(1)

        if not url.startswith("http"):
            url = 'https://' + url

        download_Video_Audio(directory, url, quality)

    elif choice == 2:
        print("\nVeronica => Enter playlist url")
        print("User => ", end="")
        url = input()
        url = url.replace(" ", "")
        # url ="https://www.youtube.com/playlist?list=PLqM7alHXFySH8VivqUPnNFJ0kxgzgHrVb"

        print("\nVeronica => Enter prefered quality of videos (640p/720p)")
        print("User => ", end="")
        quality = input()
        # quality=720

        print("\nVeronica => Enter directory url")
        print("User => ", end="")
        directory = input()

        # make directory if dir specified doesn't exist
        try:
            os.makedirs(directory, exist_ok=True)
        except OSError as e:
            print(e.reason)
            exit(1)

        if not url.startswith("http"):
            url = 'https://' + url
        playlist_page_content = getPageHtml(url)
        vid_urls_in_playlist = getPlaylistVideoUrls(playlist_page_content, url)

        print("\nVeronica => Do you want to download whole playlist or a part of? (yes/no)")
        print("User => ", end="")
        choiceForRange = input()
        if choiceForRange == 'yes' or choiceForRange == 'y':
            start = 1
            end = len(vid_urls_in_playlist)
        else:
            print("\nVeronica => Enter range for playlist, in format (start-last)")
            print("User => ", end="")
            rangeOfPlaylist = input()
            start, end = rangeOfPlaylist.split('-')
        # print(vid_urls_in_playlist[2],type(vid_urls_in_playlist))
        # downloads videos and audios
        for index in range(int(start) - 1, int(end)):
            vid_url = vid_urls_in_playlist[index]
            # print(vid_url)
            download_Video_Audio(directory, vid_url, quality)
            time.sleep(1)
    else:
        print("\nVeronica => OOPS, Pls. select from 1 or 2")
