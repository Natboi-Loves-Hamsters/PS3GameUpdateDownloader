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

URL = "https://a0.ww.np.dl.playstation.net/tpl/np/{}/{}-ver.xml".format(name, name)
response = requests.get(URL, verify=False)
with open('update.xml', 'wb') as file:
   file.write(response.content)

xmldoc = minidom.parse('update.xml')
packagelist = xmldoc.getElementsByTagName('package')
urls = [elem.getAttribute("url") for elem in packagelist]
print(f"Downloading {len(urls)} updates")
for element in packagelist:
    updateurl = element.getAttribute("url")
    size = element.getAttribute("size")
    sizekb = int(size)/1024
    sizemb = sizekb/1024
    print(f"Size(MB): {sizemb:.2f} Downloading: {updateurl}")
    download_url(updateurl)