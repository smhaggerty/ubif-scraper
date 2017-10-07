# -*- coding: utf-8 -*-
import scrapy
from time import ctime
from scrapy.spiders import Spider
import re


class Item(scrapy.Item):
    name = scrapy.Field()
    repair = scrapy.Field()
    price = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
    logo = scrapy.Field()


class MainSpider(Spider):


    name = "main"
    allowed_domains = ['www.ubreakifix.com']
    start_urls = ['https://www.ubreakifix.com/iphone-repair',
                  'https://www.ubreakifix.com/google-repair',
                  'https://www.ubreakifix.com/samsung-repair',
                  'https://www.ubreakifix.com/lg-repair',
                  'https://www.ubreakifix.com/htc-repair',
                  'https://www.ubreakifix.com/motorola-repair',
                  'https://www.ubreakifix.com/blackberry-repair',
                  'https://www.ubreakifix.com/nokia-repair',
                  'https://www.ubreakifix.com/amazon-repair',
                  'https://www.ubreakifix.com/game-console-repair',
                  'https://www.ubreakifix.com/ipod-repair',
                  'https://www.ubreakifix.com/tablet-repair',
                  'https://www.ubreakifix.com/computer-repair',
                  'https://www.ubreakifix.com/iphone-repair']

    def parse(self, response):
        if response.xpath("/html/body/div[5]/div[1]/div[2]/section/div/div[2]/div[3]/div/div/a[2]") == []:
            urls = response.xpath("/html/body/div[5]/div[1]/div[2]/section/div/div[2]/div[2]/div/div/a/@href").extract()
            for url in urls:
                url = response.urljoin(url)
                yield scrapy.Request(url=url, callback=self.parse)

        else:
            repairs = response.xpath(
                "/html/body/div[5]/div[1]/div[2]/section/div/div[2]/div[3]/div/div/a[2]/figure/figcaption").extract()
            for caption in repairs:
                item = Item()
                item['price'], item['repair'] =  self.caption_handler(caption)
                item['logo'] = self.get_logo_path(item['repair'])
                item['name'] = self.get_name(response.url)
                item['repair'] = item['name'] + " " + item['repair']
                item['date'], item['url'] = ctime(), response.url
                yield item

    def caption_handler(self, caption):
        price = self.find_price(caption)
        caption = caption[15:]
        repair_start_index = self.find_repair_start_index(caption)
        repair_stop_index = self.find_repair_stop_index(caption)
        repair = re.sub("&amp;", "&", caption[repair_start_index:repair_stop_index])
        return price, repair

    def find_price(self, caption):
        price = ""
        if caption.find("Quote") != -1:
            price = "Price not available online"
        elif caption.find("Free") != -1:
            price = "Free"
        elif caption.find("$") != -1:
            price_index = caption.find("$")
            price = re.sub("[a-zA-z</\s]", "", caption[price_index:price_index + 8])
        return price

    def get_name(self, url):
        name_list = url.split("/")[-1].split("-")[:-1]
        name_list = [word.capitalize() for word in name_list]
        name_list = [word.replace('Iphone', 'iPhone').replace('Ipod', 'iPod').replace('Ipad', 'iPad').replace('Se', 'SE').replace('Pc', 'PC') for word in name_list]
        return " ".join(name_list)

    def find_repair_start_index(self, caption):
        capital_indexes = [i for i, j in enumerate(caption) if j.isupper()]
        return capital_indexes[0]

    def find_repair_stop_index(self, caption):
        i = caption.find('\n')
        return i

    def get_logo_path(self, repair):
        icon_paths = {
            "&": "ubif-icons/glass-lcd.png",
            "LCD": "ubif-icons/lcd.png",
            "Battery": "ubif-icons/battery.png",
            "Charge": "ubif-icons/charge-port.png",
            "Headphone": "ubif-icons/headphone.png",
            "Water": "ubif-icons/water-damage.png",
            "Diagnostic": "ubif-icons/diagnostic.png",
            "Glass": "ubif-icons/glass.png",
            "Screen": "ubif-icons/glass.png",
            "Camera": "ubif-icons/camera-red.png",
            "Virus": "ubif-icons/virus.png",
            "Hard": "ubif-icons/hard-drive.png",
            "Memory": "ubif-icons/memory.png",
            "Loud": "ubif-icons/loudspeaker.png",
            "Home": "ubif-icons/home-button.png",
            "Power": "ubif-icons/power-button.png",
            "Volume": "ubif-icons/volume.png",
            "Microphone": "ubif-icons/microphone.png",
            "Vibrator": "ubif-icons/vibrator.png",
            "Ear": "ubif-icons/earspeaker.png",
            "& Back": "ubif-icons/front-back-glass.png",
            "Back Cover": "ubif-icons/back-cover.png",
            "Disc": "ubif-icons/disc-drive.png"
        }

        for term in icon_paths.keys():
            if term in repair:
                return icon_paths[term]