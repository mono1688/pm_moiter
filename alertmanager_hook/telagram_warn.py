import telegram, json, logging,os
from dateutil import parser
from flask import Flask
from flask import request
from flask_basicauth import BasicAuth
import time;



app = Flask(__name__)
app.secret_key = 'lAlAlA123'
basic_auth = BasicAuth(app)


chatID = int(os.getenv("CHATID"))
token = os.getenv("TOKEN")



app.config['BASIC_AUTH_FORCE'] = False
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = '123456'


bot = telegram.Bot(token=token)

@app.route('/', methods = ['GET'])
def index():
    #bot.sendMessage(chat_id=chatID, text="test warn")
    return "success"
    
    
    
@app.route('/alert', methods = ['POST'])
def postAlertmanager():
    
    try:
        content = json.loads(request.get_data())
        app.logger.info("\t%s",content)
        f = open('aa.log','a+')
        f.write(str(content) + "\n" )
        #print(content);

        for alert in content['alerts']:
            message = "状态: "+alert['status']+"\n"
            instance = alert['labels']['instance']
            message += "实例: "+ instance + "\n"
            annotations = alert['annotations']
            if str(annotations).find('域名')<0:

                if 'summary' in alert['annotations']:
                    message += "名称: "+alert['annotations']['summary'].replace(f"Instance {instance}",'')+"\n"



                if 'description' in alert['annotations']:
                    message += "描述: "+alert['annotations']['description'].replace(f"{instance} of job ",'')+"\n"

                if alert['status'] == "resolved":
                    correctDate = parser.parse(alert['endsAt']).strftime('%Y-%m-%d %H:%M:%S')
                    currenTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(time.mktime(time.strptime(correctDate, "%Y-%m-%d %H:%M:%S"))) + 8*3600 ))
                    message += "时间: "+ currenTime

                if alert['status'] == "firing":
                    correctDate = parser.parse(alert['startsAt']).strftime('%Y-%m-%d %H:%M:%S')
                    currenTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(time.mktime(time.strptime(correctDate, "%Y-%m-%d %H:%M:%S"))) + 8*3600 ))
                    message += "时间: " + currenTime

                print(message)
                bot.sendMessage(chat_id=chatID, text=message)
            return "Alert OK", 200

    except Exception as error:
        print(str(error));
        app.logger.info("\t%s",error)
        
        return "Alert fail", 200
        
app.run(host='0.0.0.0',port=9119)
