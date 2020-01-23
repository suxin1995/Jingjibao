# -*- coding:utf-8 -*-
import requests
import json
from requests.cookies import RequestsCookieJar
from datetime import datetime
import requests

requests.packages.urllib3.disable_warnings()

class FightBaby:
    def __init__(self,username,password,changeparam):
        self.username = username
        self.password = password
        self.loginurl = "https://www.%s.com/Index/Index/Login.html"%changeparam
        self.signurl =  "https://www.%s.com/UserAjax/SignInDay"%changeparam
        self.taskurl = "https://www.%s.com/User/getDateTask.html"%changeparam
        self.solvetaskurl = "https://www.%s.com/User/getTaskprize.html"%changeparam
        self.logouturl = "https://www.%s.com/Index/Index/Logout.html" % changeparam
        self.moneyurl = "https://www.%s.com/UserAjax/getVirtual.html"%changeparam
        self.headers =  {"Content-Type":"application/x-www-form-urlencoded",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
                         "Connection": "close"}

    #模拟登陆
    def login(self):
        data = {'username': self.username, 'password': self.password,"verify_code":""}
        response = requests.post(url=self.loginurl, data=data, headers=self.headers, verify=False)
        responseJson = json.loads(response.text)
        cookie_jar = RequestsCookieJar()
        cookie_dict = requests.utils.dict_from_cookiejar(response.cookies)
        cookie_jar.set([key for key in cookie_dict][0], cookie_dict[[key for key in cookie_dict][0]])
        return responseJson["status"],cookie_jar

    #签到
    def sign(self,cookie_jar):
        res = requests.get(self.signurl, self.headers, cookies=cookie_jar, verify=False)
        res2 = self.assets(cookie_jar)
        self.push("竞技宝每日自动签到任务反馈",self.username+'\n'+res.text.encode("utf-8").decode("unicode-escape")+'\n'+res2)

        print (res.text.encode("utf-8").decode("unicode-escape"))

    #获取任务
    def Task(self,cookie_jar):
        res = requests.get(self.taskurl, self.headers, cookies=cookie_jar, verify=False)
        task = json.loads(res.text)
        tasklist = []
        for m in task["data"]["list"]:
            if m["status"] == "1":
                tasklist.append(m['task_id'])
        if len(tasklist) == 0:
            print ("暂无可完成任务")
        else:
            for id in tasklist:
                self.SolveTask(id,cookie_jar)
            print ("完成任务",len(tasklist))

    #完成任务
    def SolveTask(self,id,cookie_jar):
        iddata = {"task_id":id}
        res = requests.post(url=self.solvetaskurl, headers=self.headers, cookies=cookie_jar,data=iddata, verify=False)
        print (res.text.encode("utf-8").decode("unicode-escape"))

    #登出
    def logout(self,cookie_jar):
        res = requests.get(self.logouturl, self.headers, cookies=cookie_jar, verify=False)
        print(res.text.encode("utf-8").decode("unicode-escape"))

    #当前账户资产(宝币)
    def assets(self,cookie_jar):
        res = requests.post(self.moneyurl, self.headers, cookies=cookie_jar, verify=False)
        print(res.text.encode("utf-8").decode("unicode-escape"))
        return res.text.encode("utf-8").decode("unicode-escape")

    #微信方糖监控提醒
    def push(self,title, content):
        api = "https://sc.ftqq.com/*************.send"  #专属绑定的微信公众号api
        data = {
            "text": title,
            "desp": content
        }
        requests.post(api, data=data)

if __name__ == '__main__':
        #遍历 已填写的多个账号的用户名与密码
        Accountlist = [{"username":"","password":""},{"username":"","password":""}]
        while Accountlist:
            account = Accountlist.pop(0)
            print ("执行账户操作:",account["username"])
            #网站域名变动 需调整更改 changeparam字段
            fightbaby = FightBaby(username=account['username'],password=account['password'],changeparam="jingjibao8")
            if fightbaby.login()[0] == 1:
                print ("登陆成功")
                fightbaby.sign(fightbaby.login()[1])
                fightbaby.Task(fightbaby.login()[1])
                fightbaby.logout(fightbaby.login()[1])
                print("登出成功")
            else:
                print ("登陆失败")
            print ("此账户执行完毕:", account["username"])
