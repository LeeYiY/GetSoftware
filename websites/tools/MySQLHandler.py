import pymysql
import yaml

class MySQLHandler:
    def __init__(self,config_yml):
        """
        初始化 MySQL 数据库连接

        :param host: 数据库主机地址
        :param user: 数据库用户名
        :param password: 数据库用户密码
        :param database: 要使用的数据库名
        :param port: 数据库端口，默认为 3306
        :param charset: 字符集，默认为 utf8mb4
        """
        try:
            with open(config_yml, 'r') as f:
                config = yaml.safe_load(f)
                host = config['mysql']['host']
                user = config['mysql']['user']
                password = config['mysql']['password']
                database = config['mysql']['database']
                port = config['mysql']['port']
                charset = config['mysql']['charset']
                self.conn = pymysql.connect(host=host, user=user, password=password, database=database, port=port,
                                            charset=charset)
                self.cursor = self.conn.cursor()
        except FileNotFoundError:
            print(f"配置文件 {config} 未找到。")
        except yaml.YAMLError as e:
            print(f"解析 YAML 文件时出错: {e}")
        except pymysql.Error as e:
            print(f"数据库连接出错: {e}")


    def insert(self, table, data):
        """
        插入数据到指定表

        :param table: 要插入数据的表名
        :param data: 要插入的数据，字典类型，键为列名，值为列值
        :return: 插入成功返回 True，失败返回 False
        """
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        try:
            self.cursor.execute(sql, tuple(data.values()))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Insert error: {e}")
            return False

    def select(self, table, columns='*', where=None):
        """
        从指定表中查询数据

        :param table: 要查询数据的表名
        :param columns: 要查询的列名，默认为查询所有列
        :param where: 查询条件，字符串类型，例如 "id = 1"
        :return: 查询结果，列表类型，每个元素为一个元组
        """
        sql = f"SELECT {columns} FROM {table}"
        if where:
            sql += f" WHERE {where}"
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Select error: {e}")
            return []

    def update(self, table, data, where):
        """
        更新指定表中的数据

        :param table: 要更新数据的表名
        :param data: 要更新的数据，字典类型，键为列名，值为列值
        :param where: 更新条件，字符串类型，例如 "id = 1"
        :return: 更新成功返回 True，失败返回 False
        """
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where}"
        try:
            self.cursor.execute(sql, tuple(data.values()))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Update error: {e}")
            return False

    def delete(self, table, where):
        """
        从指定表中删除数据

        :param table: 要删除数据的表名
        :param where: 删除条件，字符串类型，例如 "id = 1"
        :return: 删除成功返回 True，失败返回 False
        """
        sql = f"DELETE FROM {table} WHERE {where}"
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Delete error: {e}")
            return False

    def close(self):
        """
        关闭数据库连接
        """
        self.cursor.close()
        self.conn.close()

