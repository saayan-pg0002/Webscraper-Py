from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import random
from time import sleep


def writeToTxt(data, mode):
    tempfile = open("res_links.txt", mode)
    tempfile.write(str(data))
    tempfile.close()


def clearFile():
    tempfile = open("res_links.txt", 'w')
    tempfile.write('')
    tempfile.close()


def getbs4Response(url):
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'lxml')
    soup.prettify()
    return soup


def getUserInputs():
    print("Which restaurant?")
    searchstr = str(input() or "indian")
    if(searchstr == None):
        searchstr = "indian"
    print("Where do you want to search? (doesnt work all the time) by default search vancouver")
    resLoc = str(input() or "Vancouver").title()
    url = "https://www.yelp.com/search?find_desc=" + \
        searchstr + "&find_loc=" + resLoc
    return url, resLoc


def getListofRes(url):
    soup = getbs4Response(url)
    regex = re.compile('.*leftRailSearchResultsContainer.*')
    bodyRes = soup.find('main', class_=regex)
    regex = re.compile('.*undefined.*')
    reslist = bodyRes.find('ul', class_=regex)
    clearFile()
    regex = re.compile('.*border-color--default.*')
    for index in reslist.find_all('li', class_=regex):
        for a in index.find_all('a', href=True):
            link = a['href']
            if 'biz' in link:
                restaurantURL = "https://www.yelp.ca/" + link + "\n"
                writeToTxt(restaurantURL, 'a')


def getEachResName(links, resloc):
    soup = getbs4Response(links)
    regex = re.compile('.*css-.*')
    resTitle = soup.find('h1', class_=regex).text
    regex = re.compile('.*stickySidebar--fullHeight.*')
    resAddress = 'NaN'
    resPhn = 'NaN'
    for index in soup.find_all('div', class_=regex):
        for possibleAdds in index.find_all('p', class_=re.compile('.*css.*')):
            text = possibleAdds.getText()
            if resloc in text:
                resAddress = text
            text = text.replace('(', '').replace(
                ')', '').replace('-', '').replace(' ', '')
            if text.isnumeric():
                resPhn = text
        if (resAddress != 'NaN') & (resPhn != 'NaN'):
            break
    print("Restaurant: ", resTitle)
    print("Address: ", resAddress)
    print("Phone Number: ", resPhn)
    print("URL: ", links, "\n\n")


def main():
    url, resloc = getUserInputs()
    getListofRes(url)
    df = pd.read_csv("res_links.txt", names=["URL"])
    df = df.groupby(df.index // 3).first()
    writeToTxt(df['URL'].values,'w')
    # for index, row in df.iterrows():
    #     getEachResName(row['URL'], resloc)
    #     timeS = round(random.uniform(2, 30), 2)
    #     print("Waiting ", timeS, " seconds....\n")
    #     sleep(timeS)


if __name__ == "__main__":
    main()
