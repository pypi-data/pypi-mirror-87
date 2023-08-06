# --- Fender ---
# Read config file
# Log into B2B website
# Download pre-made inventory Excel file (no disk)
# Download custom-selected "specs" Excel file (no disk)
# Convert both files to CSV

from requests import session
import pandas as pd

from .supplier import Supplier, ScappamentoError, browser_login


supplier_name = 'Fender'


def update():
    # Credentials and URLs
    key_list = ['email',
                'email_css_selector',
                'password',
                'password_css_selector',
                'butt_css_selector',
                'login_url',
                'xlsx_inventory_url',
                'xlsx_specs_url',
                'csv_inventory_filename',
                'csv_specs_filename',
                'target_path']
    fender = Supplier(supplier_name, key_list)

    print(fender)

    [email,
     email_css_selector,
     password,
     password_css_selector,
     butt_css_selector,
     login_url,
     xlsx_inventory_url,
     xlsx_specs_url,
     csv_inventory_filename,
     csv_specs_filename,
     target_path] = fender.val_list

    cookies = browser_login(login_url, email_css_selector, email, password_css_selector, password, butt_css_selector)

    with session() as s:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36 "
                   }
        s.headers.update(headers)
        for cookie in cookies:  # port session cookies over
            c = {cookie['name']: cookie['value']}
            s.cookies.update(c)

        print('Downloading inventory...')
        r_inventory = s.get(xlsx_inventory_url)  # download inventory Excel file

        print('Downloading specs...')
        r_specs = s.get(xlsx_specs_url)  # download specs Excel file

        # TODO: https://dealer.fender.com/logout POST

    # Convert to CSV and save
    # TODO: check header size and column names
    inventory_list_xlsx = pd.read_excel(r_inventory.content, header=None)
    inventory_list_xlsx.to_csv(target_path + csv_inventory_filename, sep=';', header=None, index=False)

    specs_list_xlsx = pd.read_excel(r_specs.content, header=None)
    specs_list_xlsx.to_csv(target_path + csv_specs_filename, sep=';', header=None, index=False)


if __name__ == '__main__':
    update()
