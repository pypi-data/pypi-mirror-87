# -*- coding:UTF-8 -*-
import os, sys, json
import pandas as pd
import requests

curPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(curPath)

import extend.extendspace as ep

# dbid = '1710'
# chapter_code = 'all'
# mysql_config_file = os.path.join(os.path.dirname(__file__), 'mysql_config.json')


def get_result(data):
    p = ep.Alterspace(data['host'], data['user'], data['pwd'], data['dbname'])
    ret = p.createdatafile()
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",ret)
    # return (ret)
    return ret


def application(environ, start_response):
    # 加入logging
    # fileConfig(log_file_path)
    # logger = logging.getLogger(name="TimedRotatingFileHandler")

    try:
        request_body_size = int(environ.get("CONTENT_LENGTH", 0))
    except ValueError:
        request_body_size = 0
        print(f"---request_body_size---: {request_body_size}")
    request_body = environ['wsgi.input'].read(request_body_size)
    print(f"-----request_body------:  {request_body}")
    request_body = json.loads(request_body.decode().strip())
    # print(f"-----after decode,request_body------:  {request_body}")
    print(f"---request name: {request_body['methodname']}")

    ########################deal with request#########################################################
    finalresponse = None
    if request_body['methodname'] == 'hello':
        finalresponse = "Hi, there"
    elif request_body['methodname'] == "get_result":

        # 伟革错误编码可以在这里做修改
        try:
            try:
                # logger.info(request_body)
                finalresponse = get_result(request_body)
            except ValueError:
                finalresponse = {'errorString': 'Wrong formate'}
                # logger.error(finalresponse)
        except:
            finalresponse = {'errorString': 'Unknow Error'}
            # logger.error(finalresponse)

    else:
        print(f"------request_body['methodname']={request_body['methodname']}--------")

    ########################final response#########################################################
    # print(f"finalresponse: {finalresponse}")
    response_body = json.dumps(finalresponse, ensure_ascii=False).encode()
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(response_body)))
    ]
    start_response(status, response_headers)
    # return [json.dumps(finalresponse).encode()]
    # logger.info(response_body)
    return [response_body]


if __name__ == "__main__":
    print("just a test")

    host = "10.7.137.76"
    user = "zhc"
    pwd = "126315"
    dbname = "ROG"

    data = {}

    data['host'] = host
    data['user'] = user
    data['pwd'] = pwd
    data['dbname'] = dbname

    res = get_result(data)
    # print(res)
