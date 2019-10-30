import scrapy



class RealestatesSpider(scrapy.Spider):
    name = "realestates"
    start_urls = [
        'https://www.nepremicnine.net/24ur.html',
        'https://www.nepremicnine.net/znizane-cene.html',
    ]


    def parse(self, response):
        for add in response.css('div.oglas_container'):
            year = ''
            try:
                year = add.css('span.leto *::text').getall()[1]
            except IndexError:
                year = ''

            page1_dict = {
                'add_title': add.css('span.title::text').get(),
                'type_of_sale': add.css('span.posr::text').get(),
                'class_of_realestate': add.css('span.vrsta::text').get(),
                'type_of_realestate': add.css('span.tipi::text').get(),
                'year_built': year,
                'size_attribute': add.css('span.velikost::text').get(),
                'add_text': add.css('div.kratek::text').get(),
                'price': add.css('span.cena::text').get(),
            }
            #yield page1_dict

            a = add.css('a::attr(href)').get()
            a = response.urljoin(a)
            request = scrapy.Request(a, callback=self.parse_page2, cb_kwargs=dict())
            for k, v in page1_dict.items():
                request.cb_kwargs[k] = v
            yield request
            

        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


    def parse_page2(self, response, add_title, type_of_sale, class_of_realestate, type_of_realestate, year_built, size_attribute, add_text, price):
        
        full_text = response.css('div.web-opis p::text').getall()
        contact = response.css('div.kontakt-opis p::text').getall()
        contact_dict = dict()
        index = 1
        for line in contact:
            contact_dict['line_{0}'.format(index)] = line.strip()
            index+=1

        contact_tel = response.css('div.kontakt-opis a::attr(href)').getall()

        
        yield dict(
            add_title=add_title.strip(),
            type_of_sale=type_of_sale.strip(),
            class_of_realestate=class_of_realestate.strip(),
            type_of_realestate=type_of_realestate.strip(),
            year_built=year_built.strip(), 
            size_attribute=size_attribute.strip(), 
            add_text=add_text.strip(), 
            price=price.strip(),
            full_text=full_text,
            contact=contact_dict,
            contact_phone = contact_tel,
        )