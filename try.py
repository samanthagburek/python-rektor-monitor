import argparse
import requests
import json
import base64
import ast
from merkle_proof import DefaultHasher, verify_consistency, verify_inclusion, compute_leaf_hash
from util import extract_public_key

def get_log_entry(log_index, debug=False):
    # verify that log index value is sane
    response = requests.get(f'https://rekor.sigstore.dev/api/v1/log/entries?logIndex={log_index}')
    data = response.json()
    print(data)
    for i in data:
        
        for x in data[i]['verification']['inclusionProof']:
            print(x)
        code_string = base64.b64decode(data[i]['body']).decode()
        #print(code_string)
        newstr = ast.literal_eval(code_string)

        signature = base64.b64decode(newstr['spec']['signature']['content'])
        print(signature)

        # code_string = base64.b64decode(data[i]['body']).decode()
        # print(newstr['spec']['signature']['content'])
        

        #print(extract_public_key(newstr['spec']['signature']['publicKey']))
        #print(newstr['dp'])

        
    
    
def main():
    get_log_entry('129593524')

if __name__ == "__main__":
    main()