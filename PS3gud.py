import requests
import urllib3
from xml.dom import minidom
import os
urllib3.disable_warnings()

def download_url(url):
    file_name_start_pos = url.rfind("/") + 1
    file_name = url[file_name_start_pos:]
    # creates file name from the dl
    r = requests.get(url, stream=True)
    if r.status_code == requests.codes.ok:
        with open(f"{name}/{file_name}", 'wb') as f:
            for data in r:
                f.write(data)
    return url
    # downloads the file into a directory

name = input("What is the serial number of the game?: ")
# name = "BCUS98208"
version = input("What is the current version of the game?: ")
# version = "01.28"
# inputs for info

URL = "https://a0.ww.np.dl.playstation.net/tpl/np/{}/{}-ver.xml".format(name, name)
response = requests.get(URL, verify=False)
if response.status_code != 200:
    print("Error, game ID is invalid!")
    exit(1)

path = os.path.exists(name)
if path is False:
    os.mkdir(name)
# makes directory for the name if it doesnt exist

with open(f'{name}/update.xml', 'wb') as file:
    file.write(response.content)
# downloads the xml

xmldoc = minidom.parse(f'{name}/update.xml')
elements = xmldoc.getElementsByTagName('package')
sortedel = sorted(elements, key=lambda elem: elem.getAttribute("version"))
packagelist = filter(lambda elem: elem.getAttribute("version") > version, sortedel)
packagelist = list(packagelist)
urls = [elem.getAttribute("url") for elem in packagelist]
print(f"Downloading {len(urls)} updates")
for element in packagelist:
    updateurl = element.getAttribute("url")
    size = element.getAttribute("size")
    sizemb = int(size)/1024/1024
    print(f"Size(MB): {sizemb:.2f} Downloading: {updateurl}")
    download_url(updateurl)
# parses xml and downloads the pkg files

os.remove(f'{name}/update.xml')
# removes update.xml
