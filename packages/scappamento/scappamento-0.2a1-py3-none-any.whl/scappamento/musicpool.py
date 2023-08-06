# --- MusicPool ---
# Read config file
# Log into B2B website
# Download Excel file into dataframe (no disk)
# Check column count
# Clean file content
# Convert to CSV

import sys
import re

from requests import session
from bs4 import BeautifulSoup
import pandas as pd

from .supplier import Supplier, ScappamentoError


supplier_name = 'MusicPool'


def update():
    # Credentials and URLs
    key_list = ['email',
                'password',
                'login_url',
                'form_action_url',
                'csv_filename',
                'target_path',
                'expected_columns_len']
    musicpool = Supplier(supplier_name, key_list)

    print(musicpool)

    [email,
     password,
     login_url,
     form_action_url,
     csv_filename,
     target_path,
     expected_columns_len] = musicpool.val_list

    with session() as s:
        # Login
        s.get(login_url)  # set preliminary cookies
        payload = {'email': email, 'passwd': password, 'SubmitLogin': ''}
        s.post(form_action_url, data=payload, headers={'User-Agent': 'Chrome'})

        # Parse
        musicpool_soup = BeautifulSoup(s.get(login_url).text, 'html.parser')
        intermediate_url = musicpool_soup.find(text='DOWNLOAD').parent.parent['href']

        external_host_soup = BeautifulSoup(s.get(intermediate_url).text, 'html.parser')
        # mark regular expression as a raw string to prevent <invalid unicode escape sequence> errors
        xlsx_url = external_host_soup.find(text=re.compile(r'Download[\s]*\([\d]+[.]?[\d]*[A-Z][A-Z]\)')).parent['href']

        xlsx_list = pd.read_excel(xlsx_url, header=None)

        # Check file format
        if len(xlsx_list.columns) != expected_columns_len:  # check for usual header size
            print("Unexpected datasheet header size")
            sys.exit()

        xlsx_list.drop([1], inplace=True)
        xlsx_list.to_csv(target_path + csv_filename, sep=';', index=False, header=None)


if __name__ == '__main__':
    update()
