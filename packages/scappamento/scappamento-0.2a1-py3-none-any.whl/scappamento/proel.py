# --- Proel ---
# WIP, will be used to merge 2 incomplete / conflicting CSV files

import pandas as pd

from .supplier import Supplier, ScappamentoError


supplier_name = 'Proel'


def update():
    # Config
    key_list = ['csv_filename_1',
                'csv_filename_2']
    proel = Supplier(supplier_name, key_list)

    print(proel)

    [csv_filename_1,
     csv_filename_2] = proel.val_list

    # Mapping header from csv2 to csv1
    headers_map = {'Product_name': 'PRODUCT_CODE',
                   'Cat_1': 'CAT_1',
                   'Lead Time': 'LEAD_TIME'}

    # note: file 2 is the "master" one
    csv_1 = pd.read_csv(csv_filename_1, sep=';', encoding='ISO-8859-1')
    csv_2 = pd.read_csv(csv_filename_2, sep=';', encoding='utf-8')

    # DONE: create header map between the two files
    # print(csv_1.iloc[:, 31].tolist()[1:50])
    # print(csv_1.iloc[:, 0].tolist()[1:50])
    print(csv_1.columns.tolist())

    csv1_product_code = csv_1['PRODUCT_CODE'].tolist()
    print('CSV1 entries: ', len(csv1_product_code))

    csv2_product_code = csv_2['Product_name'].tolist()
    print('CSV2 entries: ', len(csv2_product_code))

    common = [x for x in csv2_product_code if x in csv1_product_code]
    print('Common entries: ', len(common), '!')

    print(csv_2['Product_name'][3])

    # TODO: use DataFrame.join(), specify common key = Product_Name, retrieve list of column names


if __name__ == '__main__':
    update()
