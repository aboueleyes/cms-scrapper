# cms-scrapper
A selenium (headless browser) script that scrapes video links from CMS website

> **⚠️ This script is made for linux , if you are using Windows it is pain ,just use linux **

## Description

The script scrapes the m3u8 file so you can access the videos from dacast directly, making it very easy to stream or to download 

## Installation 

```bash
> sudo apt install git chromium-chromedriver python3-pip 
> git clone https://github.com/aboueleyes/cms-scrapper.git
> cd cms-scrapper/
> sudo pip3 install -r requirements.txt
```
Also you need mpv or vlc to stream the videos and youtube-dl to download 

## Usage 
```bash 
> python scrape.py -o "links_file"
> mpv "video_link" # for steraming
> python download.py -i "links_file" # for downloading
 ```
##  Contribution 

For any feedback or issues, feel free to open an issue, make sure to keep it as detailed as possible.

If you would like to contribute, feel free to fork the repo, and open a PR. However, please create an issue first with the feature/bug-fix you would like to implement

## License

The script is open source under the MIT License.

DISCLAIMER: This script is in no way legally associated with the GUC. It is simply a personal project for automating day-to-day tasks involving the GUC system.

