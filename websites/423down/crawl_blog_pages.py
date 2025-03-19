import requests
from lxml import html
import random
def crawl_blog_pages(base_url, start_page, end_page, li_selector):
    """
    抓取博客列表页面及其子页面内容的函数

    :param base_url: 博客列表页的基础 URL，例如 'www.423down.com/page/'
    :param start_page: 起始页码
    :param end_page: 结束页码
    :param list_selector: 博客列表中文章链接的 CSS 选择器
    :param title_selector: 博客子页面标题的 CSS 选择器
    :param content_selector: 博客子页面内容的 CSS 选择器
    :return: 包含每篇博客标题和内容的列表
    """
    all_blogs = []
    # 定义请求头列表
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
    ]
    for page in range(start_page, end_page + 1):
        page_url = f"{base_url}{page}"
        print(f"Crawling page: {page_url}")
        try:
            # 随机选择一个请求头
            headers = {
                'User-Agent': random.choice(user_agents)
            }
            # 发送请求获取当前博客列表页，并带上随机请求头
            response = requests.get(page_url, headers=headers)
            response.encoding = response.apparent_encoding

            if response.status_code == 200:
                # 使用 lxml 解析 HTML
                tree = html.fromstring(response.text)
                # 找到所有文章链接
                li_elements = tree.xpath("/html/body/div[3]/div[1]/div")
                result = []
                for info in li_elements:
                    url = info.xpath('.//ul/li/a[1]/@href')
                    titles = info.xpath('.//ul/li/h2/a/text()')

                    print("result:", titles)



        except requests.RequestException as e:
            print(f"Error fetching blog list {page_url}: {e}")

if __name__ == "__main__":
    crawl_blog_pages("https://www.423down.com/page/", 1, 1, '//*[@id="hasfixed"]//ul/li/h2')
