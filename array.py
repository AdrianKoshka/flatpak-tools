import json
import requests
import os
import hashlib

locales = ["ar", "ast", "be", "bg", "bn-BD", "br", "ca", "cs", "cy", "da", "de", "dsb", "el", "en-GB", "en-US", "es-AR", "es-ES", "et", "eu", "fr", "fi", "fy-NL," "ga-IE", "gd", "gl", "he", "hr", "hsb", "hu", "hy-AM", "id", "is", "it", "ja", "kab", "ko", "lt", "nb-NO", "nn-NO", "pa-IN", "pl", "pt-BR", "pt-PT", "rm", "ro", "ru", "si", "sk", "sl", "sq", "sr", "sv-SE", "ta-LK", "tr", "uk", "vi", "zh-CN", "zh-TW"]
# Download locale extension

bigdata = []
output_file = "locales.json"

for locale in locales:
    burl = 'https://download-origin.cdn.mozilla.net/pub/thunderbird/releases/'
    tbr = '52.9.1'
    xpid = '/linux-x86_64/xpi/'
    fext = '.xpi'
    url = burl + tbr + xpid + locale + fext
    file_name = locale + fext
    
    print("Getting " + url) 
    r = requests.get(url)

    xpidata=r.content

    # Retrieve HTTP meta-data
    #print(r.status_code)  
    #print(r.headers['content-type'])  
    #print(r.encoding)

    # Generate the checksum
    sha256 = hashlib.sha256()
    sha256.update(xpidata)
    xpichecksum = sha256.hexdigest()

    # Check the 'file-size'
    file_size = len(xpidata)

    # Spit out the JSON
    data = {}
    data['type'] = 'extra-data'
    data['filename'] = file_name
    data['only-arches'] = ['x86_64']
    data['url'] = url
    data['sha256'] = xpichecksum
    data['size'] = file_size
    bigdata.append(data)
    
json_data = json.dumps(bigdata)

with open(output_file, 'w') as f:
        f.write(json_data)
