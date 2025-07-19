from scrapy.spiders import Spider


def generate_url_list_for_song_pages(pages: int):
    counter = 0
    while counter <= pages:
        yield f"https://guitarflash.com/custom/lista.asp?pag={str(counter)}"
        counter += 1


class MainSpider(Spider):
    name = "guitarflashcrawler"
    allowed_domains = ["guitarflash.com"]
    start_urls = list(generate_url_list_for_song_pages(86))

    def __init__(self, search_string: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search_string = search_string
        self.already_parsed_songs = set()

    def parse(self, response, **kwargs):
        for table_row in response.css("tr")[1:]:
            song_name = table_row.css("td a::text").get()
            song_url = table_row.css("td a").xpath("@href").get()

            if (
                song_name
                and self.search_string.lower() in song_name.lower()
                and song_url
                and song_url not in self.already_parsed_songs
            ):
                self.already_parsed_songs.add(song_url)
                yield {
                    "song_name": song_name,
                    "song_url": song_url
                }
