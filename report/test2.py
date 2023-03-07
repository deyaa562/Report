import requests

url = "http://localhost:8080/api/v1/enair-system-test/log"

payload={'json_request_part': '[{"launchUuid": "7e72866f-830f-45c1-97d8-19f38f079d49", "itemUuid": "3a3fda02-2da3-4654-8965-1b74ee0034ee", "time": "1677680073888", "message": "Screenshot", "level": "INFO", "file": {"name": "20ee33716a07729b.png"}}]'}
files=[
  ('file',('20ee33716a07729b.png',open('/mnt/c/Users/deyaah/Downloads/Report-main/Report-main/report/20ee33716a07729b.png','rb'),'image/png'))
]
headers = {
  'Authorization': 'Bearer 8cc58ff3-890e-4047-835c-05981dbbad2b'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)