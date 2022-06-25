from nameko.extensions import DependencyProvider
import mysql.connector
from mysql.connector import Error
import mysql.connector.pooling
import json
import os

UPLOAD_FOLDER = "/uploads/"


class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection

    def login(self, username, password):
        result = {}
        response = {}
        cursor = self.connection.cursor()
        sql = "SELECT * FROM `user` WHERE username = %s AND password = %s"
        cursor.execute(sql, [username, password])
        row = cursor.fetchall()
        row_count = cursor.rowcount

        if row_count == 1:
            response['status'] = 'success'
            response['message'] = 'Login Success!'
            result['id_user'] = row[0][0]
            result['status_code'] = 200
        else:
            response['status'] = 'error'
            response['message'] = 'Your Username and Password are Not Defined!'
            result['status_code'] = 404

        cursor.close()
        result['response'] = response
        return result

    def upload_files(self, filename, id_user):
        result = {}
        cursor = self.connection.cursor()
        sql = "INSERT INTO `files`(`id`, `filepath`, `access_user`) VALUES (NULL, %s, %s)"
        cursor.execute(sql, [filename, int(id_user)])
        self.connection.commit()

        result['status_code'] = 200
        result['status'] = "success"
        cursor.close()
        return result

    def download_file(self, file_id, user_id):
        result = {}
        response = {}
        cursor = self.connection.cursor()
        sql = "SELECT * FROM `files` WHERE id = %s AND access_user = %s"
        cursor.execute(sql, [int(file_id), int(user_id)])
        row = cursor.fetchall()
        row_count = cursor.rowcount

        if row_count == 1:
            result['status_code'] = 200
            response['status'] = "success"
            response['filename'] = row[0][1]
        else:
            result['status_code'] = 404
            response['status'] = "error"
            response['message'] = 'File not found'

        cursor.close()
        result['response'] = response
        return result

    def view_file(self, id_user):
        result = {}
        response = {}
        cursor = self.connection.cursor()
        sql = "SELECT * FROM `files` WHERE access_user = %s "
        cursor.execute(sql, [int(id_user)])
        row = cursor.fetchall()
        row_count = cursor.rowcount

        if row_count > 0:
            result['status_code'] = 200
            response['status'] = "success"
            response['files'] = []

            cursor.execute(sql, [int(id_user)])
            for row in cursor.fetchall():
                response['files'].append(
                    {"id_file": row[0], "filename": row[1]})
        else:
            result['status_code'] = 404
            response['status'] = "error"
            response['message'] = 'There are still no file'

        cursor.close()
        result['response'] = response
        return result


class DatabaseProvider(DependencyProvider):

    connection_pool = None

    def setup(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=32,
                pool_reset_session=True,
                host='127.0.0.1',
                database='soa_cloud_storage',
                user='root',
                password=''
            )
        except Error as e:
            print("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())
