import json
import sys
import getopt

def main(argv):

    fmap_json = sys.argv[1]
    bold_files = sys.argv[2:]
    f = open(fmap_json, "r+")
    data = json.load(f)
    data['IntendedFor'] = bold_files
    f.close()
    with open(fmap_json,"w") as out:
        json.dump(data, out, indent = 4, sort_keys=True)
    f.close()
if __name__ == "__main__":
    main(sys.argv[1:]) 

            
        
