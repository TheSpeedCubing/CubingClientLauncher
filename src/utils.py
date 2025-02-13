import sys
import zipfile

import requests


def ext(extract, path):
    with zipfile.ZipFile(extract, "r") as zip_ref:
        zip_ref.extractall(path)


def dl(url, path):
    with open(path, "wb") as f:
        print("Downloading %s" % path)
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:  # no content length header
            f.write(response.content)
        else:
            a = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                a += len(data)
                f.write(data)
                s = str(float(a / total_length) * 100) + " %"
                sys.stdout.write('\r'+s)
                sys.stdout.flush()
