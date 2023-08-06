from flask import Flask
from flask import request
import time
import hashlib
import requests
import hmac
import json
import zipfile
import os
import shutil

app = Flask(__name__)


@app.route('/get-download-url')
def hello_wordl():
    app_key = '11942a38d88089ed545a6a9d867ef7f7'
    app_token = 'app-e3778c96-9ba4-467b-a73e-2079f94db857'
    url = 'https://jua.cloudpnr.com/file/v6/files'
    is_private = '0'
    is_random_name = '0'
    is_encrypt = '0'
    env = 'test'
    startdir = "./coverage_report_data_new.html"  # 要压缩的文件夹路径
    if (os.path.exists(startdir)):
        zip_ya()
    else:
        return 'report file not exist'
    # file_name = './coverage_report_data_new.html/index.html'
    file_name = startdir + '.zip'
    # 拼接请求参数
    file_info = {
        'app_token': app_token,
        'timestamp': str(int(time.time() * 1000)),
        'private': is_private,
        'random_name': is_random_name,
        'encryption': is_encrypt
    }
    hash_md5 = hashlib.md5()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    md5_file = hash_md5.hexdigest()
    param_dict = {
        'app_token': app_token,
        'timestamp': file_info['timestamp'],
        'files': md5_file,
        'password': '',
        'path': '',
        'private': file_info['private'],
        'random_name': file_info['random_name'],
        'encryption': file_info['encryption']
    }
    keys = param_dict.keys()
    keys = sorted(keys, reverse=False)
    # 拼接 key 和 value 值
    values = ''
    for key in keys:
        value = str(param_dict.get(key))
        if len(value) == 0:
            continue
        values = values + '&' + str(key) + '=' + value

    plain_text = 'POST' + values[1:]
    try:
        ak = bytes(app_key, 'utf8')
        pt = bytes(plain_text, 'utf8')
    except:
        ak = app_key
        pt = plain_text
    signature = hmac.new(ak, pt, digestmod=hashlib.sha256)
    file_info['signature'] = signature.hexdigest()
    files = open(file_name, 'rb')
    # 上传文件
    response = requests.Session().post(url,
                                       headers={'env': env},
                                       files={'files': files},
                                       data=file_info, verify=True, timeout=99999)  # 发送请求
    print(response.headers)
    if response.status_code != 200:
        try:
            reason = json.loads(response.text)['message']
            return reason
        except Exception as e:
            ee = str(e)
            reason = 'System Error'
            return ee
        raise ConnectionError(response.status_code, reason)
    shutil.rmtree(startdir)
    # 返回 file-token
    ret_dict = json.loads(response.text)
    # file_token = ret_dict['file_token']
    download_url = ret_dict['download_url']
    return download_url


@app.route("/zip")
def zip_ya():
    startdir = "./coverage_report_data_new.html"
    file_news = startdir + '.zip'  # 压缩后文件夹的名字
    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(startdir):
        for filename in filenames:
            if (filename.__eq__('index.html') or filename.endswith('.xml')
                    or os.path.exists(filename.replace('_py.html', '') + '.py')):
                z.write(os.path.join(dirpath, filename), filename)
                print('压缩成功')
    z.close()
    return '压缩成功'


if __name__ == '__main__':
    app.run(host='172.31.30.222',port=5000)
