from scrapy.spiders import Spider


def generate_url_list_for_song_pages(pages: int):
    counter = 0
    while counter <= pages:
        yield f"https://guitarflash.com/custom/lista.asp?pag={str(counter)}"
        counter += 1


class MainSpider(Spider):
    name = "guitarflashcrawler"
    allowed_domains = ["guitarflash.com"]
    start_urls = list(generate_url_list_for_song_pages(85))

    def __init__(self, search_string: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search_string = search_string

    def parse(self, response, **kwargs):
        for table_row in response.css("tr")[1:]:
            if self.search_string in table_row.css("td a::text").get():
                yield {
                    "song_name": table_row.css("td a::text").get(),
                    "song_url": table_row.css("td a").xpath("@href").get()
                }
