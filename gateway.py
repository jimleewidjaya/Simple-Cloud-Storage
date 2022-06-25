import json
from nameko.rpc import RpcProxy
from nameko.web.handlers import http
from werkzeug.wrappers import Response
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask import Flask, send_file, current_app, send_from_directory
from os.path import join, dirname, realpath

UPLOAD_FOLDER = "uploads"
UPLOADS_PATH = join(dirname(realpath(__file__)), 'uploads/')
EXTENSION_HEADER = {
    'txt': 'text/plain',
    'pdf': 'application/pdf',
    'png': 'image/png',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'gif': 'image/gif'
}


class cloudGatewayService:
    name = 'cloud_gateway'
    user_rpc = RpcProxy('user_service')
    storage_rpc = RpcProxy('storage_service')
    session_rpc = RpcProxy('session_service')

    @http('POST', '/login')
    def login_account(self, request):
        req = request.json
        cookies = request.cookies.get('sessionID')

        if cookies is None:
            login = self.user_rpc.login(req['username'], req['password'])

            if int(login['status_code']) == 200:
                username = {
                    'id_user': int(login['id_user']),
                    'username': req['username']
                }
                session_id = self.session_rpc.set_session_data(username)
                response = Response(json.dumps(login['response'], indent=4))
                response.set_cookie('sessionID', session_id)

                return response
            else:
                return int(login['status_code']), (json.dumps(login['response'], indent=4))
        else:
            return 400, json.dumps({"status": "error", "message": "Log Out First!"}, indent=4)

    @http('GET', '/logout')
    def logout_account(self, request):
        cookies = request.cookies.get('sessionID')

        if cookies is None:
            return 400,  json.dumps({"status": "error", "message": "Log In First!"}, indent=4)
        else:
            logout = self.session_rpc.delete_session('sessionID')
            response = Response(json.dumps(logout))
            response.delete_cookie('sessionID')

            return response

    @http('POST', '/upload')
    def upload(self, request):
        cookies = request.cookies.get('sessionID')

        if cookies is None:
            return 400,  json.dumps({"status": "error", "message": "Log In First!"}, indent=4)
        else:
            session = self.session_rpc.get_session_data(cookies)

            app = Flask(__name__)
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            f = request.files.getlist('file')
            for files in f:
                file_type = (files.filename).split('.')[-1]
                filename = ''.join(
                    e for e in files.filename if e.isalnum()).replace(file_type, '')
                file_name = str(
                    hash(str(session['id_user']))) + '_' + filename + '.' + file_type
                upload_files = self.storage_rpc.upload_files(
                    file_name, session['id_user'])

                filename = secure_filename(file_name)
                files.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], filename))

            return 200,  json.dumps({"status": "success", "message": "Files uploaded successfully!"}, indent=4)

    @http('GET', '/download/<int:file_id>')
    def download_file(self, request, file_id):
        cookies = request.cookies.get('sessionID')

        if cookies is None:
            return 400,  json.dumps({"status": "error", "message": "Log In First!"}, indent=4)
        else:
            session = self.session_rpc.get_session_data(cookies)
            news = self.storage_rpc.download_file(file_id, session['id_user'])

            if news['status_code'] == 200:
                response = news['response']
                filename = response['filename']

                response = Response(
                    open(UPLOADS_PATH + '/' + filename, 'rb').read())
                file_type = filename.split('.')[-1]

                response.headers['Content-Type'] = EXTENSION_HEADER[file_type]
                response.headers['Content-Disposition'] = 'attachment; filename={}'.format(
                    filename)

                return response
            else:
                return int(news['status_code']), (json.dumps(news['response'], indent=4))

    @http('GET', '/file')
    def view_file(self, request):
        cookies = request.cookies.get('sessionID')

        if cookies is None:
            return 400,  json.dumps({"status": "error", "message": "Log In First!"}, indent=4)
        else:
            session = self.session_rpc.get_session_data(cookies)
            file = self.storage_rpc.view_file(session['id_user'])
            return int(file['status_code']), (json.dumps(file['response'], indent=4))
