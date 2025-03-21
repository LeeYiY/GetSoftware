import hashlib
import random
import requests
from datetime import datetime
from websites.tools.MySQLHandler import MySQLHandler
def solution():
    dbconn = MySQLHandler("../../config.yml")
    sql = "select url_to_crawl from crawl_info where is_crawled = 0 limit 20"
    dbconn.cursor.execute(sql)
    results = dbconn.cursor.fetchall()

    for result in results:
        url = result[0]
        hash_url = hashlib.md5(url.encode('utf-8')).hexdigest()
        content = get_blog_info(url)
        sql = "update crawl_info set down_content = %s,is_crawled = 1,last_crawl_time = %s where hash_url = %s"
        dbconn.cursor.execute(sql, (content, datetime.now(),hash_url))
        dbconn.conn.commit()
        print("update success")
    dbconn.close()
def get_blog_info(url):
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
    ]
    try:
            # 随机选择一个请求头
        headers = {
            'User-Agent': random.choice(user_agents)
        }
        response = requests.get(url, headers=headers)
        response.encoding = response.apparent_encoding
        print(response.status_code)
        if response.status_code == 200:
            html_text = response.text
            start_str = '下载地址'
            end_str = '</div>'
            start_index = html_text.find(start_str)
            if start_index != -1:
                start_index += len(start_str)
                # 查找结束字符串的位置
                end_index = html_text.find(end_str, start_index)
                if end_index != -1:
                    # 截取两个字符串之间的内容
                    middle_content = html_text[start_index:end_index]
                    # 查找第一个 <p> 标签的位置
                    p_start_index = middle_content.find('<p>')
                    if p_start_index!= -1:
                        middle_content = middle_content[p_start_index:]
                    print(middle_content)
                else:
                    print("未找到结束字符串")
            else:
                print("未找到起始字符串")
        return middle_content
    except Exception as e:
        print('error',e)

if __name__ == '__main__':
    solution()
