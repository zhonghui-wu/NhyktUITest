import pymysql
import sshtunnel


def userSQL(sshIP, sshPort, databaseIP, databasePwd, databaseName, sshKeyAddress, data):
    '''
    :param sshIP:
    :param sshPort:
    :param databaseIP:数据库连接ip
    :param databasePwd:数据库密码
    :param databaseName: 数据库名称
    :param sshKeyAddress: sshkey的文件地址
    :param sql: sql语句
    :return:
    '''
    with sshtunnel.SSHTunnelForwarder(
            (sshIP, sshPort),
            ssh_username='rock.wu',
            ssh_pkey=sshKeyAddress,
            ssh_private_key_password='123456',
            # ssh_password='服务器的密码',
            remote_bind_address=(databaseIP, 3306),
            local_bind_address=('127.0.0.1', 13306)
    ) as tunnel:
        conn = pymysql.connect(
            user='rock.wu',
            password=databasePwd,
            host='127.0.0.1',
            port=13306,
            database=databaseName,
        )
        cursor = conn.cursor()
        sql = "update user set is_delete = 1 where user_id = (%s);"
        try:
            # 使用 execute()  方法执行 SQL 查询
            cursor.executemany(sql, data)
            # 提交到数据库
            conn.commit()
            # 使用 fetchone() 方法获取单条数据.
            # data = cursor.fetchall()
            # print(data)
        except:
            # 发生错误时回滚
            conn.rollback()
        # 关闭数据库连接
        cursor.close()

    return