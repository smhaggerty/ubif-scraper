# -*- coding: utf-8 -*-
import json
import re
import scrapy
import os
from scrapy import Spider, Item, Field
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from time import ctime


class Item(Item):


    name = Field()
    repair = Field()
    price = Field()
    date = Field()
    url = Field()
    logo = Field()


class UBIFItemLoader(ItemLoader):


    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    desc_out = Join()

class JsonWriterPipeline(object):


    def __init__(self):
        self.file = open('repairs.json', 'w')
        self.file.write("[\n")

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + ',' + '\n'
        self.file.write(line)
        self.file.flush()
        return item


class UBIFSpider(Spider):


    name = "ubif"
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
                  'https://www.ubreakifix.com/computer-repair']

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
                item['logo'] = 'ubif-icons/' + self.get_logo_filename(item['repair'])
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

    def get_logo_filename(self, repair):
        icon_paths = {
            "&": "glass-lcd.png",
            "LCD": "lcd.png",
            "Battery": "battery.png",
            "Charge": "charge-port.png",
            "Headphone": "headphone.png",
            "Water": "water-damage.png",
            "Diagnostic": "diagnostic.png",
            "Glass": "glass.png",
            "Screen": "glass.png",
            "Camera": "camera-red.png",
            "Virus": "virus.png",
            "Hard": "hard-drive.png",
            "Memory": "memory.png",
            "Loud": "loudspeaker.png",
            "Home": "home-button.png",
            "Power": "power-button.png",
            "Volume": "volume.png",
            "Microphone": "microphone.png",
            "Vibrator": "vibrator.png",
            "Ear": "earspeaker.png",
            "& Back": "front-back-glass.png",
            "Back Cover": "back-cover.png",
            "Back Housing" : "back-cover.png",
            "Disc": "disc-drive.png",
            "Wheel": "click-wheel.png",
            "Complete": "complete.png",
            "Clean": "virus.png",
            "Light": "light.png",
            "BluRay": "disc-drive.png",
            "Dock": "charge-port",
            "E74": "e74.png",
            "Ring": "ring.png"
        }

        for term in icon_paths.keys():
            if term in repair:
                return icon_paths[term]

if __name__ == '__main__':
    process = CrawlerProcess({ 'ITEM_PIPELINES': { '__main__.JsonWriterPipeline': 100} })
    process.crawl(UBIFSpider)
    process.start()

    with open('repairs.json', 'rb+') as filehandle:
        filehandle.seek(-2, os.SEEK_END)
        filehandle.truncate()
        filehandle.flush()

    with open('repairs.json', 'a') as myfile:
        myfile.write("]")