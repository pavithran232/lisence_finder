import sys
import re
import requests
from bs4 import BeautifulSoup, SoupStrainer

home_url = 'https://parivahan.gov.in/rcdlstatus/?pur_cd=102'
post_url = 'https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml'
plate=input('Enter License Plate:')
first = plate[:-4]
second = plate[-4:]
r = requests.get(url=home_url)
cookies = r.cookies
soup = BeautifulSoup(r.text, 'html.parser')
viewstate = soup.select('input[name="javax.faces.ViewState"]')[0]['value']
i = 0
for match in soup.find_all('button', id=re.compile("form_rcdl")):
  if i ==  0:
    button_id= match.get('id')
  i = 1

data = {
    'javax.faces.partial.ajax':'true',
    'javax.faces.source':button_id,
    'javax.faces.partial.execute':'@all',
    'javax.faces.partial.render':'form_rcdl:pnl_show form_rcdl:pg_show form_rcdl:rcdl_pnl',
    button_id:button_id,
    'form_rcdl':'form_rcdl',
    'form_rcdl:tf_reg_no1': first,
    'form_rcdl:tf_reg_no2': second,
    'javax.faces.ViewState': viewstate,
}

r = requests.post(url=post_url, data=data, cookies=cookies)
soup = BeautifulSoup(r.text, 'html.parser')
table = SoupStrainer('tr')
soup = BeautifulSoup(soup.get_text(), 'html.parser', parse_only=table)
print(soup.get_text())
