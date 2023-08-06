# User-facing CLI
# Top-level script for scappamento usage

import sys
import argparse

from scappamento import yamaha
from scappamento import fender
from scappamento import frenexport
from scappamento import suonostore
from scappamento import mepa
from scappamento import mogar


def main():
    suppliers_list = ['yamaha', 'fender', 'frenexport', 'suonostore', 'mepa', 'mogar']
    updaters_list = [yamaha.update, fender.update, frenexport.update, suonostore.update, mepa.update, mogar.update]
    suppliers_help = 'the supplier to be updated'

    parser = argparse.ArgumentParser(description='Automate B2B provisioning.')
    parser.add_argument('supplier_name', choices=suppliers_list, help=suppliers_help)

    namespace = parser.parse_args()

    i = 0
    for supplier in suppliers_list:
        if namespace.supplier_name == supplier:
            updaters_list[i]()
        i = i + 1


if __name__ == '__main__':
    sys.exit(main())
