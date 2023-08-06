# Common functionality to be shared across modules
# This is not a stand-alone module
# Supplier class for init stuff

import configparser

import chromedriver_binary
from selenium import webdriver

default_config_path = 'C:\\Ready\\ReadyPro\\Archivi\\'
default_config_name = 'scappamento.ini'


class Supplier:
    name = ''
    val_list = []

    def __init__(self, name, key_list=None, config_path=None):
        self.name = name
        if key_list:
            if config_path:
                self.load_config(key_list, config_path)
            else:
                self.load_config(key_list)

    def __str__(self):
        return '-- ' + self.name + ' --\n'

    def load_config(self, key_list, config_path=default_config_path+default_config_name):
        config = configparser.ConfigParser()

        with open(config_path) as f:
            config.read_file(f)

            for key in key_list:
                self.val_list.append(config[self.name][key])


class ScappamentoError(Exception):
    pass


# scan line by double-quotes pairs
# look for separator characters inside quote pairs
# replace separator with sub
# return fixed line, is_modified
def fix_illegal_sep_quotes(line, sep, sep_replacement):
    is_modified = False
    in_quotes = False
    new_line = ''
    for char in line:
        if char == '"':
            in_quotes = not in_quotes  # toggle
            new_line = new_line + char
            continue

        if in_quotes and char == sep:
            new_line = new_line + sep_replacement
            is_modified = True
        else:
            new_line = new_line + char

    return new_line, is_modified


# change from one separator character to another
def switch_sep(line, sep_old, sep_new):
    return line.replace(sep_old, '%temp%').replace(sep_new, sep_old).replace('%temp%', sep_new)  # flip old and new


# login into AJAX websites
def browser_login(login_url, user_css_selector, user, password_css_selector, password, butt_css_selector,
                  pop_css_selector=None):
    chromedriver_path = chromedriver_binary.chromedriver_filename

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    with webdriver.Chrome(options=options) as driver:
        # Login
        print('ChromeDriver path:', chromedriver_path)
        driver.get(login_url)

        if pop_css_selector:
            pop_up_butt = driver.find_element_by_css_selector(pop_css_selector)
            pop_up_butt.click()

        user_input = driver.find_element_by_css_selector(user_css_selector)
        user_input.send_keys(user)

        pass_input = driver.find_element_by_css_selector(password_css_selector)
        pass_input.send_keys(password)

        login_butt = driver.find_element_by_css_selector(butt_css_selector)
        login_butt.click()

        return driver.get_cookies()
