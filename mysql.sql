CREATE TABLE IF NOT EXISTS crawl_info (
    -- 自增主键，用于唯一标识每条记录
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录唯一标识',
    -- 待抓取的链接，不可为空且需唯一
    url_to_crawl VARCHAR(255) NOT NULL UNIQUE COMMENT '待抓取的链接',
    -- 标记是否抓取，默认值为 FALSE
    is_crawled BOOLEAN DEFAULT FALSE COMMENT '是否已抓取的标记',
    -- 插入数据库的时间，默认值为当前时间
    insert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录插入数据库的时间',
    -- 最后抓取时间，可为空
    last_crawl_time TIMESTAMP NULL COMMENT '最后一次抓取的时间',
    -- 抓取的标题
    crawled_title VARCHAR(255) COMMENT '抓取到的页面标题',
    -- 抓取的图像地址
    crawled_image_url VARCHAR(255) COMMENT '抓取到的页面图像地址',
    -- 抓取的名称
    crawled_name VARCHAR(255) COMMENT '抓取到的页面名称'
) COMMENT '存储网页抓取信息的表';