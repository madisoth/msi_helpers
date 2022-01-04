# zimmermann_nhp_json_sanitize.py
# intended use is to sanitize dcm2niix-generated JSONs of 10.5T macaque data to be usable with DCAN nhp-abcd-bids-pipeline
# usage: python3 json_sanitize_escape_fix.py <input> <output>


import json
import sys
import getopt
import re
from typing import Union

class LazyDecoder(json.JSONDecoder):
    def decode(self, s, **kwargs):
        regex_replacements = [
            (re.compile(r'([^\\])\\([^\\])'), r'\1\\\\\2'),
            (re.compile(r',(\s*])'), r'\1'),
        ]
        for regex, replacement in regex_replacements:
            s = regex.sub(replacement, s)
        return super().decode(s, **kwargs)

def json_sanitize(value: Union[str, dict, list], is_value=True) -> Union[str, dict, list]:
    """
    Adapted from 
    
    https://stackoverflow.com/a/45526935/2635443
    https://stackoverflow.com/questions/65910282/jsondecodeerror-invalid-escape-when-parsing-from-python

    Recursive function that allows to remove any special characters from json, especially unknown control characters
    Also fixes invalid escapes
    """
    if isinstance(value, dict):
        value = {json_sanitize(k, False):json_sanitize(v, True) for k, v in value.items()}
    elif isinstance(value, list):
        value = [json_sanitize(v, True) for v in value]
    elif isinstance(value, str):
        if not is_value:
            # Remove double backslash, asterisk, caret, whitespace with underscore
            value = re.sub(r"\\", '_', value)
            value = re.sub(r'[*^]', '_', value)
            value = re.sub('\s', '_', value)
        else:
            # Remove all control characters
            value = re.sub(r'[\x00-\x1f\x7f-\x9f]', ' ', value)
    return value

def main(argv):
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    f = open(inputfile, "r+")
    data = json.load(f, cls=LazyDecoder, strict=False)
    f.close()
    outData = {}
    data.pop('ReconstructionMethod', None)
	
    for (k, v) in data.items():
        if "WipMemBlock" not in k:
            print("Key: " + k)
            print("Old value: " + str(v))	 
            outV = json_sanitize(v, False)
            print("New value: " + str(outV))
            outData[k] = outV
    with open(outputfile, 'w') as out:
        json.dump(outData, out, indent = 4, sort_keys=True)
if __name__ == "__main__":
    main(sys.argv[1:])





