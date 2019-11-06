# RealestateScraper

Spider that crawls nepremicnine.net.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

first you will need python3.7 or above, virtualenv and pip installed.

after cloning the repository go to the RealestateSpider folder (optionally create a virtualenv) and run "pip install -r requirements.txt"

Install tor-expert-bundle (https://www.torproject.org/download/tor/)

1. Set up a password in command prompt:
"C:\Tor\Tor\tor.exe --hash-password "password" | more"

2. Create a torrc file (no extension) in C:\Tor\torrc

3. Add the following to your torrc file
ControlPort 9051
##If you enable the controlport, be sure to enable one of these
##authentication methods, to prevent attackers from accessing it.
HashedControlPassword 16:1B8FA15192DBBFCE60A6B0022D119A2D12EC69E76E0854C43A75A9BA72

4. Run tor with 'c:\Tor\tor.exe -f "C:\Tor\torrc"'

5. If you receive error StartService() failed : Access is denied see: https://stackoverflow.com/a/47291114/1486850 for fix.

INSTALL PRIVOXY
1. Download it from https://www.privoxy.org/ and install

2. Open Privoxy config.txt and uncomment line forward-socks4a   /   127.0.0.1:9050

3. Run Privoxy

RUN SPIDER
1. You should now be able to run the spider from the RealestateScraper directory with "scrapy crawl realestates"

SCHEDULE SPIDER
1. Make a new basic task in windows task scheduler

1a. Edit spidey.bat to point to correct folders

2. Choose Start a program and point it to spidey.bat, found in the root folder of the project

3. Spider should now crawl periodically

### Prerequisites

Python 3.7 or higher
pip
virtualenv
all depencencies in requirements.txt
Tor-expert-bundle
Privoxy

