import json
import pkg_resources


x = pkg_resources.resource_filename('aidenbots', 'labware/' + "eppendorf_96_well_lobind_plate_500ul" +'.json')

def main():
    print(x)