# coding: utf-8
import requests
url=''# REplace with slack webhook url
data={"text":"Hello,world!"}
requests.post(url,json=data)
