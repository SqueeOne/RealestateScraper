@Echo Off
REM activate Python env
CALL "C:\Users\Squee\Documents\Coding\RealScrape\env\Scripts\activate.bat"
CD "C:\Users\Squee\Documents\Coding\RealScrape\RealestateSpider\RealestateSpider\spiders\"
CALL "C:\Users\Squee\AppData\Local\Programs\Python\Python37\python.exe" "C:\Users\Squee\AppData\Local\Programs\Python\Python37\Scripts\scrapy.exe" crawl realestates
