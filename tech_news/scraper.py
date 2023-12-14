import requests
import time
from parsel import Selector
from tech_news.database import create_news


def fetch(url):

    try:
        res = requests.get(url)
        res.raise_for_status()
        time.sleep(2)

    except (requests.ReadTimeout, requests.HTTPError):
        return None
    return res.text


# Requisito 2
def scrape_novidades(html_content):
    selector = Selector(text=html_content)
    href = selector.css(".tec--card__info h3 a::attr(href)").getall()

    if selector is None:
        return []
    return href


def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)

    if selector is None:
        return []
    next_href = selector.css(".tec--list__item ~ a::attr(href)").get()
    return next_href


def scrape_noticia(html_content):
    selector = Selector(text=html_content)
# if selector is None:
#     return ""
#  else:
#  writer = selector.css(".tec--author__info *::text ").get() or\
# selector.css(".tec--timestamp__item.z--font-bold a::text")
# return writer.strip()

    writer = selector.css(".z--font-bold *::text").get()
    # writer = None if writer is None else writer.strip()
    shares_count = selector.css(".tec--toolbar__item::text").get()
    comments_count = selector.css("#js-comments-btn::attr(data-count)").get()
    summary_new = selector.css(
        ".tec--article__body > p:first-child *::text"
        ).getall()
    string_vazia = ''
    summary = string_vazia.join(summary_new)
    sources = selector.css(".z--mb-16 h2 ~ div a::text").getall()
    categories = selector.css("#js-categories a::text").getall()

    # if shares_count is None:
    #     return 0
    # else:
    #     int(shares_count.split(" ")[0])

    # shares_count = shares_count is None else int(shares_count.split()[0])
    # int(shares_count.split(",")[0]) if shares_count else 0
    # if shares_count:
    #     shares_count = int(shares_count.split()[0])
    # else:
    #     shares_count = 0

    dicionario = {
        "url": selector.css
        ("head link[rel=canonical]::attr(href)").get(),
        "title": selector.css
        (".tec--article__header__title::text").get(),
        "timestamp": selector.css("time::attr(datetime)").get(),
        "writer": writer,
        "shares_count": int(shares_count.split(" ")[1]) if shares_count else 0,
        "comments_count": int(comments_count),
        "summary": summary,
        "sources": [source.strip() for source in sources],
        "categories": [category.strip() for category in categories],
          }

    if writer:

        dicionario["writer"] = writer.strip()
    else:
        dicionario[writer] = writer
    return dicionario


def get_tech_news(amount):
    url = "https://www.tecmundo.com.br/novidades"
    data = fetch(url)
    news_links_list = scrape_novidades(data)
    new_data = []

    while len(news_links_list) < amount:
        data = fetch(scrape_next_page_link(data))
        news_links_list.extend(scrape_novidades(data))

    for link in news_links_list[:amount]:
        data = fetch(link)
        created_scrap = scrape_noticia(data)
        new_data.append(created_scrap)

    create_news(new_data)
    return new_data
