from tech_news.database import search_news
import datetime


def search_by_title(title):
    news = search_news({"title": {"$regex": title, "$options": "i"}})
    search_result = []
    for new in news:
        search_result.append((new["title"], new["url"]))
    return search_result


def search_by_date(date):
    """Seu código deve vir aqui"""
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Data inválida")

    result_search = []
    results = search_news({'timestamp': {'$regex': date}})
    for result in results:
        result_search.append((result["title"], result["url"]))
    return result_search


def search_by_source(source):
    result = search_news({"sources": {"$regex": source, "$options": "i"}})

    search_result = []
    for res in result:
        search_result.append((res["title"], res["url"]))
    return search_result


# Requisito 9
def search_by_category(category):
    result = search_news({"categories": {"$regex": category, "$options": "i"}})

    search_result = []
    for res in result:
        search_result.append((res["title"], res["url"]))
    return search_result
