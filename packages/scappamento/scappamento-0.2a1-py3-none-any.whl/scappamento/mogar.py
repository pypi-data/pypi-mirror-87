# Convert CSV file from UCS-2 encoding to UTF-8

import os.path

from .supplier import Supplier


supplier_name = 'Mogar'


def update():
    key_list = ['csv_filename',
                'target_path']
    mogar = Supplier(supplier_name, key_list)

    print(mogar)

    [csv_filename,
     target_path] = mogar.val_list

    csv_file_path = os.path.join(target_path, csv_filename)
    csv_bak_path = csv_file_path + '.bak'

    if os.path.isfile(csv_bak_path):
        os.remove(csv_bak_path)

    os.rename(csv_file_path, csv_bak_path)

    with open(csv_bak_path, 'r', encoding='utf_16_le') as old_f:
        with open(csv_file_path, 'w', encoding='utf-8') as new_f:
            contents = old_f.read()
            new_f.write(contents)
