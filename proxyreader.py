import re
import requests
import pandas as pd

def proxyIpPortValidator(ipPort):
    print("Checking ",ipPort,"...")
    url = "http://www.yelp.ca"
    proxyDict = {"http": "http://" + ipPort, "https:": "https://" + ipPort}
    try:
        req = requests.get((url),proxies=proxyDict,timeout=10)
    except:
        print("req cannot connect")
    else:
        if req.status_code == 200:
            print(req)

def main():
    proxydata = pd.read_csv("http_proxy_working.txt",header=None,names = ['ipPort'])
    proxydata['ipPort'].apply(proxyIpPortValidator)

if __name__ == "__main__":
    main()
