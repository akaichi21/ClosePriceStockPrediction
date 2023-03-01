# Định nghĩa các thư viện cần thiết
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup # Thư viện để lấy dữ liệu ra khỏi các tệp HTML và XML

# Chọn mã chứng khoán của công ty VINAMILK (VNM) để thu thập giá đóng cửa
stock_symbol = 'VNM'

# Các hàm hỗ trợ việc xử lý dữ liệu
def transform_data(row):
    return row.text.strip()

def remove_empty_data(arr):
    return [row for row in arr if row != []]

# Tạo danh sách thời gian từ 3/2019 đến 2/2023
data = {}
time_line = []

for i in range(1, 14):
    html_text = requests.get(f'https://www.cophieu68.vn/historyprice.php?currentPage={i}&id={stock_symbol}', verify=False).text
    soup = BeautifulSoup(html_text, 'html.parser')
    table = soup.find('table', {'class': 'stock'})
    for row in table.find_all('tr'):
        stocks = row.findAll('td', class_='td_bottom3')
        time_line.append(list(map(transform_data, stocks[1:2])))

timeline = remove_empty_data(time_line)
data['Date'] = np.array(timeline[:1000]).flatten()

# Tạo danh sách giá đóng cửa của mã chứng khoán VNM theo như thời gian trên
close_price = []

for j in range(1, 14):
    html_text = requests.get(f'https://www.cophieu68.vn/historyprice.php?currentPage={i}&id={stock_symbol}', verify=False).text
    soup = BeautifulSoup(html_text, 'html.parser')
    table = soup.find('table', {'class': 'stock'})
    for row in table.find_all('tr'):
        stocks = row.findAll('td', class_='td_bottom3')
        close_price.append(list(map(transform_data, stocks[5:6])))

close_price = remove_empty_data(close_price)
data['Close_Price'] = np.array(close_price[:1000]).flatten()

# Kết hợp thời gian và giá đóng cửa thành một bảng và lưu thành tệp csv
df = pd.DataFrame(data)
df.set_index(['Date', 'Close_Price'],inplace=True)

df.to_csv('data.csv', mode='w')