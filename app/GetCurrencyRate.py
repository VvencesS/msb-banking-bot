import xml.etree.ElementTree as ET
import requests
from datetime import datetime

class CurrencyRate:

    @staticmethod
    def getCurrencyRate():
        # Call api và lưu data vào file currentrate.xml
        response = requests.get("https://portal.vietcombank.com.vn/Usercontrols/TVPortal.TyGia/pXML.aspx")
        data = response.content

        file = open('./CurrentRate/currentrate.xml', 'wb')
        file.write(data)
        file.close()

        # Đọc file xml
        root = ET.parse('./CurrentRate/currentrate.xml').getroot()
        # dateTime = root[0].text
        dateTime = datetime.strptime(root.find('DateTime').text, '%m/%d/%Y %I:%M:%S %p')
        formatDate = dateTime.strftime("%d/%m/%Y %H:%M:%S")
        # print(formatDate)

        exrateList = []
        for exrate_tag in root.findall('Exrate'):
            currencyCode = exrate_tag.get('CurrencyCode')
            currencyName = exrate_tag.get('CurrencyName').strip()
            buy = exrate_tag.get('Buy')
            transfer = exrate_tag.get('Transfer')
            sell = exrate_tag.get('Sell')

            exrate = {}
            exrate['currencyCode'] = currencyCode
            exrate['currencyName'] = currencyName
            exrate['buy'] = buy
            exrate['transfer'] = transfer
            exrate['sell'] = sell
            exrateList.append(exrate)

        return formatDate, exrateList
# CurrencyRate.getCurrencyRate()
