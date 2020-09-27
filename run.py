import web
import json
import requests
import traceback
import jwt, time
import casbin
import os, configparser
from logger.logger import logger

urls = (
    "/powerFactor", "PowerFactor",
)
    
app = web.application(urls, globals())
parent_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
config = configparser.ConfigParser()
full_path = parent_dir + '/confs/config.ini'
config.read(full_path)
dom = config.get('acs', 'domain')
# dom = 'rde'
obj = 'rde'

class PowerFactor:
    def POST(self):
        try:
            web.header("Access-Control-Allow-Origin", "*")
            token = web.input().token
            try:
                parse_token = jwt.decode(token, 'secret', algorithms='HS256')
            except Exception as e:
                logger.error(e)
                logger.error(traceback.format_exc())
                return json.dumps({'status': 'fail', 'code': 402, 'message': 'token expired'})

            username = parse_token['username']
            e = casbin.Enforcer("confs/model.conf", "confs/policy.csv")
            sub = username
            act = 'read'
            if e.enforce(sub, dom, obj, act):
                trans_code = web.input().trans_code
                start_time = web.input().start_time
                end_time = web.input().end_time
                url = 'https://ginkgo.bjrde.cn/baiducloud-webapi/select_max_power_factor_on_week?trans_code=' + trans_code + \
                        '&start_time=' + start_time + '&end_time=' + end_time
                logger.debug(url)
                con = requests.get(url).text
                return con
            else:
                return json.dumps({'status': 'fail', 'code': 401, 'message': 'unauthorization operation'})

        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            return json.dumps({'code': 500, 'message': 'fail'})

if __name__ == "__main__":
    logger.debug('start run app ...')
    app.run()