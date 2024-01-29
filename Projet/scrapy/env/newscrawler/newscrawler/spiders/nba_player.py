import scrapy
from scrapy import Request
from ..items import ArticleItem


class NbaPlayerSpider(scrapy.Spider):
    name = "nba_player"
    allowed_domains = ["basketusa.com"]
    start_urls = ["https://www.basketusa.com/equipe/atlanta/", "https://www.basketusa.com/equipe/boston/",
                  "https://www.basketusa.com/equipe/brooklyn/", "https://www.basketusa.com/equipe/charlotte/",
                  "https://www.basketusa.com/equipe/chicago/", "https://www.basketusa.com/equipe/cleveland/",
                  "https://www.basketusa.com/equipe/dallas/", "https://www.basketusa.com/equipe/denver/",
                  "https://www.basketusa.com/equipe/detroit/", "https://www.basketusa.com/equipe/golden-state/",
                  "https://www.basketusa.com/equipe/houston/", "https://www.basketusa.com/equipe/indiana/",
                  "https://www.basketusa.com/equipe/los-angeles-clippers/", "https://www.basketusa.com/equipe/los-angeles-lakers/",
                  "https://www.basketusa.com/equipe/memphis/", "https://www.basketusa.com/equipe/miami/",
                  "https://www.basketusa.com/equipe/milwaukee/", "https://www.basketusa.com/equipe/minnesota/",
                  "https://www.basketusa.com/equipe/new-orleans/", "https://www.basketusa.com/equipe/new-york/",
                  "https://www.basketusa.com/equipe/oklahoma-city/", "https://www.basketusa.com/equipe/orlando/",
                  "https://www.basketusa.com/equipe/philadelphia/", "https://www.basketusa.com/equipe/phoenix/",
                  "https://www.basketusa.com/equipe/portland/", "https://www.basketusa.com/equipe/sacramento/",
                  "https://www.basketusa.com/equipe/san-antonio/", "https://www.basketusa.com/equipe/toronto/",
                  "https://www.basketusa.com/equipe/utah/", "https://www.basketusa.com/equipe/washington/"]
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        },
        "ROBOTSTXT_OBEY" : True,
        "CONCURRENT_REQUESTS_PER_DOMAIN":200
    }

    
    
    def parse(self, response):
        team = response.css("p").css("strong::text").extract_first()
        
        for data in response.css(".line_1, .line_2"):
            link = data.css("a::attr(href)").extract_first()
            player = data.css("a::text").extract_first()
            stats = data.css("td::text").extract()
            yield Request(link, callback=self.parse_category, meta={'team': team, 'player': player, 'stats': stats})
            
            
            
    def parse_category(self, response):
        team = response.meta['team']
        player = response.meta['player']
        stats = response.meta['stats']
        data = response.css(".player-value::text").extract()
         
        yield ArticleItem(
                player = player,
                month_born = data[0],
                year_born = data[0],
                age = data[0],
                nationality = data[1],
                size = data[2],
                weight = data[3],
                pick_draft = data[4],
                team = team,
                MJ = stats[0],
                minutes = stats[1],
                tir = stats[2],
                tir_3_pts = stats[3],
                lf = stats[4],
                rb_off = stats[5],
                rb_df = stats[6],
                rb = stats[7],
                pd = stats[8],
                bp = stats[9],
                inter = stats[10],
                ct = stats[11],
                fte = stats[12],
                pts = stats[13]
            )
            