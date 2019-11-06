import scrapy
from RealestateSpider.items import RealestatespiderItem
from datetime import date



class RealestatesSpider(scrapy.Spider):
    name = "realestates"
    start_urls = [
        'https://www.nepremicnine.net/24ur.html',
        #'https://www.nepremicnine.net/znizane-cene.html',
    ]

    # Custom settings for AWS S3 image and output file storage.

    # custom_settings = {
    #     "AWS_ACCESS_KEY_ID": 'AKIAZUTAHZDAXUBXF6QZ',
    #     "AWS_SECRET_ACCESS_KEY": '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',
    #     "ITEM_PIPELINES": {'scrapy.pipelines.images.ImagesPipeline': 1},
    #     "IMAGES_STORE": 's3://realscrapey-bucket/images/',
    #     "AWS_REGION_NAME": 'us-east-2',
    #     "FEED_FORMAT": 'csv',
    #     "FEED_URI": 's3://realscrapey-bucket/output/nepremicnine_{0}.csv'.format(str(date.today()))
    # }

    # custom settings for local image and file storage.
    custom_settings = {
        "FEED_FORMAT": 'csv',
        "FEED_URI": '/Users/Squee/Documents/Coding/RealScrape/tmp/nepremicnine_{0}.csv'.format(str(date.today())),
        "ITEM_PIPELINES": {'scrapy.pipelines.images.ImagesPipeline': 1},
    }
    


    def parse(self, response):
        for add in response.css('div.oglas_container'):

            # prevents year returning null and this breaking the scrape
            year = ''
            try:
                year = add.css('span.leto *::text').getall()[1]
            except IndexError:
                year = ''

            # Compose Response for page main page
            page1_dict = {
                'add_title': add.css('span.title::text').get(),
                'type_of_sale': add.css('span.posr::text').get(),
                'class_of_realestate': add.css('span.vrsta::text').get(),
                'type_of_realestate': add.css('span.tipi::text').get(),
                'year_built': year,
                'size_attribute': add.css('span.velikost::text').get(),
                'add_text': add.css('div.kratek::text').get(),
                'price': add.css('span.cena::text').get(),
                #'image_urls': [add.css('a.slika img::attr(src)').get()],
                'image_urls': [add.css('a.rsImg::attr(data-rsBigImg)').get()],
            }

            # Uncomment the yield below and comment the final yield to check if Tor has changed IP
            #yield scrapy.Request('http://icanhazip.com', callback=self.is_tor_and_privoxy_used)

            # Pass page1_dict to parse_page2 as cb_kwargs
            a = add.css('a::attr(href)').get()
            a = response.urljoin(a)
            request = scrapy.Request(a, callback=self.parse_page2, cb_kwargs=dict())
            for k, v in page1_dict.items():
                request.cb_kwargs[k] = v

            # Comment this yield when checking if tor proxy is working
            yield request
            
        # Find next page and scrape it
        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


    # Add date from main page to data scraped from details page and yield it together
    def parse_page2(self, response, add_title, type_of_sale, class_of_realestate, type_of_realestate, year_built, size_attribute, add_text, price, image_urls):
        
        full_text = response.css('div.web-opis p::text').getall()
        ref_number = response.css('div.dsc strong::text').get()
        contact = response.css('div.kontakt-opis p::text').getall()
        #images = response.css('img.rsTmb::attr(src)').getall()
        images = response.css('div.galerija-container a.rsImg::attr(data-rsbigimg)').getall()
        contact_dict = dict()
        index = 1
        for line in contact:
            contact_dict['line_{0}'.format(index)] = line.strip()
            index+=1

        contact_tel = response.css('div.kontakt-opis a::attr(href)').getall()

        
        yield dict(
            ref_number=str(ref_number).strip(),
            add_title=add_title.strip(),
            type_of_sale=type_of_sale.strip(),
            class_of_realestate=class_of_realestate.strip(),
            type_of_realestate=type_of_realestate.strip(),
            year_built=year_built.strip(), 
            size_attribute=size_attribute.strip(), 
            add_text=add_text.strip(), 
            price=price.strip(),
            image_urls=images,
            full_text=full_text,
            contact=contact_dict,
            contact_phone = contact_tel,
            
        )

    # Function that checks if Tor and Privoxy are working and changing your visible IP
    def is_tor_and_privoxy_used(self, response):
        print ('\n\nSpider: Start')
        print ("My IP is : " + str(response.body))
        print ("Is proxy in response.meta?: ", response.meta)
        print ('\n\nSpider End')
        self.log('Saved file {0}' .format(str('test.html')))