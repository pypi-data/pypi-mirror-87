# --- Suonostore ---
# Read config file
# Download CSV file (no disk)
# Clean file, save

from requests import Session

from .supplier import Supplier, ScappamentoError, fix_illegal_sep_quotes, switch_sep


supplier_name = 'Suonostore'


def fix_timestamp(line):
    return line.replace('00:00:00', '').replace('/  /', '')


def fix_decimals(line):
    return line.replace('.00000,', ',').replace('.000,', ',').replace('.00,', ',')


def update():
    # Credentials and URLs
    key_list = ['user',
                'password',
                'csv_url',
                'csv_filename',
                'target_path']
    suonostore = Supplier(supplier_name, key_list)

    print(suonostore)

    [user,
     password,
     csv_url,
     csv_filename,
     target_path] = suonostore.val_list

    # Download
    with Session() as s:
        print('Downloading with auth...')
        # Site uses HTTP Basic Auth
        r = s.get(csv_url, auth=(user, password), headers={'User-Agent': 'Chrome'})

    # Cleanup: numbers, separators, dates, <inches> symbols
    sep = ';'
    new_csv = ''
    line_count = 0
    problematic_line_count = 0
    problematic_field_count = 0
    fixed_problematic_line_count = 0

    print('Cleaning up...')

    for line in r.content.decode(r.encoding).splitlines():  # each line in the CSV file

        if not line_count:  # skip first line = CSV header
            new_csv = switch_sep(line, ',', sep)  # initialize
            line_count = line_count + 1
            continue

        temp_line = fix_timestamp(line)
        temp_line = fix_decimals(temp_line)
        temp_line = switch_sep(temp_line, ',', sep)

        [temp_line, sep_modified] = fix_illegal_sep_quotes(temp_line, sep, ',')  # fix illegal separators

        field_count = 0
        temp_cod_art = ''
        rebuilt_temp_line = ''
        found_problematic_field = False
        match = False
        for field in temp_line.split(';'):  # for each field in line: look for double quotes as <inches> symbols

            if field_count == 1:  # if second field
                temp_cod_art = field

            if field.count('"') % 2:  # if double quotes parity check fails
                found_problematic_field = True
                match = False
                for i in range(len(field)-1, -1, -1):  # for each char in field, inverted, greedy [0-9]" match
                    if i and field[i] == '"' and field[i-1].isdigit():
                        rebuilt_temp_line = rebuilt_temp_line + sep + field[0:i] + '″' + field[i+1:len(field)]
                        match = True
                        break  # greedy

                if not match:  # problematic fields are copied as-is for now
                    print('⚠ [ Row ', line_count, '][', temp_cod_art, ']', 'Uh oh: field ', field_count + 1)
                    problematic_field_count = problematic_field_count + 1
                    rebuilt_temp_line = rebuilt_temp_line + sep + field

            else:
                if not field_count:
                    rebuilt_temp_line = field
                else:
                    rebuilt_temp_line = rebuilt_temp_line + sep + field

            field_count = field_count + 1

        if found_problematic_field or sep_modified:  # if intervention was necessary
            if match or sep_modified:  # if a solution was found
                fixed_problematic_line_count = fixed_problematic_line_count + 1
            problematic_line_count = problematic_line_count + 1

        new_csv = new_csv + '\n' + rebuilt_temp_line.strip()
        line_count = line_count + 1

    print('⚠ ' if problematic_field_count else '✓ ',
          problematic_field_count, ' problematic field', '' if problematic_field_count == 1 else 's',
          ' in ', problematic_line_count - fixed_problematic_line_count, ' problematic line',
          '' if problematic_line_count - fixed_problematic_line_count == 1 else 's',
          ' (', problematic_line_count, ' lines total, ', fixed_problematic_line_count, ' fixed)', sep='')

    with open(target_path + csv_filename, 'w', encoding='utf-8') as f:
        f.write(new_csv)


if __name__ == '__main__':
    update()
