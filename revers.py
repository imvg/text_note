# -*- coding: utf-8 -*-
from requests_toolbelt import MultipartEncoder
import re
import requests


def revers():
    get_id_url = "https://www.ilovepdf.com/zh-cn/pdf_to_word"
    auth = requests.get(url=get_id_url)
    data = auth.text.encode("gbk", "ignore").decode(encoding="gbk")
    taskId = re.split("=", [a for a in data.splitlines() if "ilovepdfConfig.taskId" in a][0])[-1].strip().replace("'",
                                                                                                                  "").replace(
        ";", "")
    token = eval(
        re.split("=", [a for a in data.splitlines() if "var ilovepdfConfig" in a][0])[-1].strip().replace("null",
                                                                                                          "1").replace(
            ";", ""))["token"]
    header = {
        "authorization": f"Bearer {token}",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
    }
    data = {
        "name": "2014_PDF.pdf",
        "chunk": "0",
        "chunks": "1",
        "task": taskId,
        "preview": "1",
        "pdfinfo": "0",
        "pdfforms": "0",
        "pdfresetforms": "0",
        "v": "web.0",
        "file": ("2014_PDF.pdf", open("/Users/vg/Desktop/2014_PDF.pdf", "rb"), "application/pdf")
    }
    data = MultipartEncoder(data, boundary='------WebKitFormBoundaryBd9xsvqtO8emtjc8')
    header['Content-Type'] = data.content_type
    upload_url = "https://api11o.ilovepdf.com/v1/upload"
    res = requests.post(url=upload_url, headers=header, data=data)
    dfile = eval(res.text)['server_filename']
    convers_url = "https://api7o.ilovepdf.com/v1/process"
    convers_data = {
        "convert_to": "docx",
        "output_filename": "{filename}",
        "packaged_filename": "ilovepdf_converted",
        "ocr": "0",
        "task": taskId,
        "tool": "pdfoffice",
        "files[0][server_filename]": dfile,
        "files[0][filename]": "2014_PDF.pdf"
    }
    convers_data = MultipartEncoder(convers_data, boundary='------WebKitFormBoundaryBd9xsvqtO8emtjc9')
    header['Content-Type'] = convers_data.content_type
    header['Host'] = "api24o.ilovepdf.com"
    header['Origin'] = "https://www.ilovepdf.com"
    header['Authorization'] = header['authorization']
    con_res = requests.post(url=convers_url, headers=header, data=convers_data)
    print(res.text)
    print(con_res.text)
    if con_res.status_code == 200:
        print(f"https://api8o.ilovepdf.com/v1/download/{taskId}")


if __name__ == '__main__':
    revers()
