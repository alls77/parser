import lxml.html as html
import requests
from json import dump


URL = 'https://tproger.ru'


def get_response(url: str):
    return requests.get(url).content


def get_pages(page_count: int):
    return [get_response(f"{URL}/page/{page}") for page in range(1, page_count + 1)]


def get_articles(page: bytes):
    return html.fromstring(page).xpath("//article/a[contains(@class, 'article-link')]/@href")


def get_article_detail(article_link: str):
    article = html.fromstring(get_response(article_link))

    return {
        'title': ''.join(article.xpath("//article/div[contains(@class, 'post-title')]/h1/text() | "
                                       "//article/div/div[contains(@class, 'post-title')]/h1/text()")),
        'body': ''.join(article.xpath("//div[contains(@class, 'entry-content')]/p//text()")),
        'images': article.xpath('//article//img/@src'),
        'datePublished': ''.join(article.xpath('//time[contains(@class, "entry-date")]/@datetime')),
    }


def dump_json(data, file_name: str):
    with open(file_name, 'w') as json_file:
        dump(data, json_file, ensure_ascii=False, indent=2)


def main():
    article_details = []

    pages = get_pages(3)
    for page in pages:
        articles = get_articles(page)

        for article in articles:
            article_details.append(get_article_detail(article))

    dump_json(article_details, "articles.json")


if __name__ == '__main__':
    main()
