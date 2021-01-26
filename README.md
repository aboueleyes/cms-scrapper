# cms-scrapper
A selenium (headless browser) script that scrapes video links from CMS website

> ⚠️ This script is made for Linux, if you are using Windows it is pain, just use Linux 

## Description

The script scrapes the m3u8 file so you can access the videos from dacast directly, making it very easy to stream or to download 

## Showcase 
#### Scrapping

[![asciicast](https://asciinema.org/a/RJ1c0PynTzM1u0hhWznKBLMm1.svg)](https://asciinema.org/a/RJ1c0PynTzM1u0hhWznKBLMm1)

#### Downloading 

[![asciicast](https://asciinema.org/a/TxObSGcbKXoq4J5bZjIqs50KH.svg)](https://asciinema.org/a/TxObSGcbKXoq4J5bZjIqs50KH)

#### Playing 

[![asciicast](https://asciinema.org/a/igiytcXttjgadEWaHhOaPGsus.svg)](https://asciinema.org/a/igiytcXttjgadEWaHhOaPGsus)

## Installation 

```bash
> sudo apt install git chromium-chromedriver python3-pip ffmpeg nodejs npm mpv
> sudo npm install --global ffmpeg-progressbar-cli    
> git clone https://github.com/aboueleyes/cms-scrapper.git
> cd cms-scrapper/
> sudo pip3 install -r requirements.txt
```
Also you need mpv or vlc to stream the videos

## Usage 
```bash 
> python scrape.py -o "links_file" # Heavy operation please be patient 
> python play.py -i "links_file" # for streaming
> python download.py -i "links_file" # for downloading
 ```
##  Contribution 

For any feedback or issues, feel free to open an issue, make sure to keep it as detailed as possible.

If you would like to contribute, feel free to fork the repo, and open a PR. However, please create an issue first with the feature/bug-fix you would like to implement

## License

The script is open source under the MIT License.

DISCLAIMER: This script is in no way legally associated with the GUC. It is simply a personal project for automating day-to-day tasks involving the GUC system.

