import scrapy
from arabic_reshaper import arabic_reshaper
from bidi.algorithm import get_display


class KuwaitHokomaSpider(scrapy.Spider):
    name = 'kuwait_hokoma'
    allowed_domains = ['kuwaitpolitics.org']
    start_urls = ['https://www.one-tab.com/page/l8F3oQcmSVSAVjtLVy2xxg']

    def parse(self, response):
        # all data line up under tabGroupContainer so
        all_hokomat=response.xpath("//div[@class='tabGroupContainer']")
        # loop through all data and extracting name and title
        for hokoma in all_hokomat:
            url=hokoma.xpath('a/@href').extract_first()
            title=hokoma.xpath('a/text()').extract_first()
            title = arabic_format_sentence(title)
            yield scrapy.Request(url=url,callback=self.parse_this_hokoma)

    def parse_this_hokoma(self,response):
        all_rows=response.xpath('//div/table/tbody/tr')
        for row in all_rows:
            th_name=row.xpath('td[1]/a/text()').extract_first()
            th_name = arabic_format_sentence(th_name)
            shakh_or_wazeer_montakhab = row.xpath('td[3]/text()').extract_first().strip()
            shakh_or_wazeer_montakhab = arabic_format_sentence(shakh_or_wazeer_montakhab)
            fara_al_alhakima = row.xpath('td[4]/text()').extract_first()
            fara_al_alhakima = arabic_format_sentence(fara_al_alhakima)
            al_taefa = row.xpath('td[5]/text()').extract_first()
            al_taefa = arabic_format_sentence(al_taefa)
            al_kabila = row.xpath('td[6]/text()').extract_first()
            al_kabila = arabic_format_sentence(al_kabila)
            al_taiar_alsiasy = row.xpath('td[7]/text()').extract_first()
            al_taiar_alsiasy = arabic_format_sentence(al_taiar_alsiasy)
            yield {
                'الاسم':th_name[::-1],
                'شيخ او وزير منتخب':shakh_or_wazeer_montakhab[::-1],
                'فرع العائلة':fara_al_alhakima[::-1],
                'al_taefa':al_taefa[::-1],
                'al_kabila':al_kabila[::-1],
                'al_taiar_alsiasy':al_taiar_alsiasy[::-1]
            }


def arabic_format_sentence(sentence):
    arabic_formated=arabic_reshaper.reshape(sentence)
    return get_display(arabic_formated)