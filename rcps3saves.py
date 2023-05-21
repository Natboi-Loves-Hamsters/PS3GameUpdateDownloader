import requests
import urllib3
from urllib.parse import urlparse
from xml.dom import minidom
urllib3.disable_warnings()


def download_url (url):
    file_name_start_pos = url.rfind("/") + 1
    file_name = url[file_name_start_pos:]

    r = requests.get(url, stream=True)
    if r.status_code == requests.codes.ok:
        with open(file_name, 'wb') as f:
            for data in r:
                f.write(data)
    return url

name = input("What is the serial number of the game?: ")
# name = "BCUS98208"
version = input("What is the current version of the game?: ")
# version = "01.28"

URL = "https://a0.ww.np.dl.playstation.net/tpl/np/{}/{}-ver.xml".format(name, name)
response = requests.get(URL, verify=False)
if response.status_code != 200:
    print ("Error, game ID is invalid!")
    exit(1)
with open('update.xml', 'wb') as file:
   file.write(response.content)

xmldoc = minidom.parse('update.xml')
elements = xmldoc.getElementsByTagName('package')
sortedel = sorted(elements, key=lambda elem: elem.getAttribute("version"))
packagelist = filter(lambda elem: elem.getAttribute("version") > version, sortedel)
packagelist = list(packagelist)
urls = [elem.getAttribute("url") for elem in packagelist]
print(f"Downloading {len(urls)} updates")
for element in packagelist:
    updateurl = element.getAttribute("url")
    size = element.getAttribute("size")
    sizekb = int(size)/1024
    sizemb = sizekb/1024
    print(f"Size(MB): {sizemb:.2f} Downloading: {updateurl}")
    download_url(updateurl)