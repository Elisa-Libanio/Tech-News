from tech_news.database import get_collection


def top_5_news():
    news = []

    db_news = get_collection()

    pipeline = [
        {
            '$project': {
                '_id': False,
                'title': '$title',
                'url': '$url',
                'popularity': {
                    '$sum': ['$shares_count', '$comments_count']},
            }
        },
        {'$sort': {'popularity': -1}},
        {'$limit': 5}
    ]

    for artic in db_news.aggregate(pipeline):
        news.append((artic['title'], artic['url']))

    return news


def top_5_categories():
    news = []
    db_news = get_collection()
    pipeline = [
        {'$unwind': '$categories'},
        {'$group': {'_id': '$categories', 'total': {'$sum': 1}}},
        {'$sort': {'total': -1, "_id": 1}},
        {'$limit': 5}
    ]
    for artic in db_news.aggregate(pipeline):
        news.append(artic['_id'])
    return news
