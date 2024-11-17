import json
import asyncio
from fake_useragent import UserAgent
from loguru import logger
import os
import requests
os.system("clear")
banner = """\033[36m
██████╗ ██╗      ██████╗  ██████╗██╗  ██╗███╗   ███╗███████╗███████╗██╗  ██╗
██╔══██╗██║     ██╔═══██╗██╔════╝██║ ██╔╝████╗ ████║██╔════╝██╔════╝██║  ██║
██████╔╝██║     ██║   ██║██║     █████╔╝ ██╔████╔██║█████╗  ███████╗███████║
██╔══██╗██║     ██║   ██║██║     ██╔═██╗ ██║╚██╔╝██║██╔══╝  ╚════██║██╔══██║
██████╔╝███████╗╚██████╔╝╚██████╗██║  ██╗██║ ╚═╝ ██║███████╗███████║██║  ██║
╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝ Node
---------------------------------------------------------------------------------
                            Author : Sahal Pramudya
---------------------------------------------------------------------------------
"""
print(banner)
mail = input("Masukkan Email : ")
pwd = input("Masukkan Password : ")
os.system("clear")
print(banner)
#url_report = f"https://app.blockmesh.xyz/api/report_uptime?email={email}&api_token={api_token}&ip={ip}"
#url_submit_task = f"https://app.blockmesh.xyz/api/report_uptime?email={email}&api_token={api_token}&ip={ip}"
user_agent = UserAgent().random
url = {
    "login": "https://api.blockmesh.xyz/api/get_token",
    "websocket": "https://feature-flags.blockmesh.xyz/read-flag/use_websocket",
    "ws_percent": "https://feature-flags.blockmesh.xyz/read-flag/use_websocket_percent",
    "poll_interval": "https://feature-flags.blockmesh.xyz/read-flag/polling_interval",
    "get_task": "https://app.blockmesh.xyz/api/get_task"
}
def login(email, password, url):
    global api_token
    headers = {
    "accept": "application/json",
    "User-Agent": user_agent
    }
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=data, headers=headers)
    if response and response.status_code == 200:
        api = response.json()
        api_token = api['api_token']
        logger.info("Login Successfull!")
        time.sleep(1)
        use_websocket()
        time.sleep(1)
        ws_percent()
        time.sleep(1)
        poll_interval()
        time.sleep(1)
        while True:
            get_task()
            time.sleep(60)
    else :
        logger.error("Login Failed!")
def use_websocket():
    header = {
        "accept": "application/json",
        "User-Agent": user_agent
    }
    response = requests.get(url["websocket"], headers=header)
    if response.json() == True:
        logger.info("Use Websocket Success!")
    else:
        logger.error("Use Websocket Failed!")
def ws_percent():
    header = {
        "accept": "application/json",
        "User-Agent": user_agent
    }
    response = requests.get(url["ws_percent"], headers=header)
    if response.json() == True:
        logger.info("Websocket Percent Success!")
    else:
        logger.error("Websocket Percent Failed!")
def poll_interval():
    headers = {
        "accept": "application/json",
        "User-Agent": user_agent
    }
    response = requests.get(url["poll_interval"], headers=headers)
    if response.status_code == 200:
        poll_int = str(response.json())
        logger.info(f"Set polling interval {poll_int}")
    else:
        logger.debug("Failed getting polling interval, set to dafault!")
        pass
def get_task():
    headers = {
        "accept": "application/json",
        "User-Agent": user_agent
    }
    data = {
        "api_token": api_token,
        "email": mail
    }
    response = requests.post(url["get_task"], headers=headers, json=data, timeout=10)
    if response.status_code == 200:
        try:
            task_data = response.json()
            task_id = task_data["id"]
            logger.info(f"Task ID {task_id}")
            time.sleep(1)
            report_uptime()
            def submit_task():
                headers = {
                    "accept": "application/json",
                    "User-Agent": user_agent
                }
                ip = requests.get('https://api.ipify.org').content.decode('utf8')
                data = {
                    "email": mail,
                    "api_token": api_token,
                    "task_id": task_id,
                    "response_code": "200",
                    "ip": ip,
                    "colo": "CGK"
                }
                response = requests.post(f"https://app.blockmesh.xyz/api/submit_task?email={mail}&api_token={api_token}&task_id={task_id}&response_code=200&ip={ip}&colo=CGK", headers=headers, json=data)
                if response.status_code == 200:
                    logger.info(f"Task ID : {task_id} submit successfull!")
                else:
                    logger.error(f"Task ID : {task_id} submit failed")
                    pass
            submit_task()
        except:
            logger.error("Task ID not ready yet, Waiting for 120 seconds...")
            time.sleep(120)
            pass
    else:
        logger.error("Failed getting task id")
    
def report_uptime():
    headers = {
        "accept": "application/json",
        "User-Agent": user_agent
    }
    ip = requests.get('https://api.ipify.org').content.decode('utf8')
    data = {
        "email": mail,
        "api_token": api_token,
        "ip": ip
    }
    response = requests.post(f"https://app.blockmesh.xyz/api/report_uptime?email={mail}&api_token={api_token}&ip={ip}", headers=headers, json=data)
    if response.status_code == 200:
        logger.info(f"Uptime submit success!")
    else:
        logger.error("Failed submit uptime!")


async def main():
    login(mail, pwd, url["login"])

if __name__ == '__main__':
    asyncio.run(main())
