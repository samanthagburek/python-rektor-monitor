import argparse
import requests
import json
import ast
import base64

from util import extract_public_key, verify_artifact_signature
from merkle_proof import DefaultHasher, verify_consistency, verify_inclusion, compute_leaf_hash

def get_log_entry(log_index, debug=False):
    # verify that log index value is sane
    try:
        response = requests.get(f'https://rekor.sigstore.dev/api/v1/log/entries?logIndex={log_index}')
        data = response.json()
        #print(data)
        return data
    except:
        raise KeyError
    

def get_verification_proof(log_index, debug=False):
    return False

def inclusion(log_index, artifact_filepath, debug=False):
    # verify that log index and artifact filepath values are sane
    entry = get_log_entry(log_index)
    for i in entry:
        code_string = base64.b64decode(entry[i]['body']).decode()
        newstr = ast.literal_eval(code_string)
        signature = newstr['spec']['signature']['content']
        certificate = base64.b64decode(newstr['spec']['signature']['publicKey']['content'])
        leaf_hash = compute_leaf_hash(entry[i]['body'])
        tree_size = entry[i]['verification']['inclusionProof']['treeSize']
        root_hash = entry[i]['verification']['inclusionProof']['rootHash']
        #hash of every single value in the tree
        hashes = entry[i]['verification']['inclusionProof']['hashes']
        index = entry[i]['verification']['inclusionProof']['logIndex']

    #extracts signature and public key
    signature = base64.b64decode(signature)
    public_key = extract_public_key(certificate)

    #function calls for checking
    verify_artifact_signature(signature, public_key, artifact_filepath)
    get_verification_proof(log_index)
    verify_inclusion(DefaultHasher, index, tree_size, leaf_hash, hashes, root_hash)

def get_latest_checkpoint(debug=False):
    pass

def consistency(prev_checkpoint, debug=False):
    # verify that prev checkpoint is not empty
    # get_latest_checkpoint()
    pass

def main():
    inclusion('129593524', 'artifact.md')
    debug = False
    parser = argparse.ArgumentParser(description="Rekor Verifier")
    parser.add_argument('-d', '--debug', help='Debug mode',
                        required=False, action='store_true') # Default false
    parser.add_argument('-c', '--checkpoint', help='Obtain latest checkpoint\
                        from Rekor Server public instance',
                        required=False, action='store_true')
    parser.add_argument('--inclusion', help='Verify inclusion of an\
                        entry in the Rekor Transparency Log using log index\
                        and artifact filename.\
                        Usage: --inclusion 126574567',
                        required=False, type=int)
    parser.add_argument('--artifact', help='Artifact filepath for verifying\
                        signature',
                        required=False)
    parser.add_argument('--consistency', help='Verify consistency of a given\
                        checkpoint with the latest checkpoint.',
                        action='store_true')
    parser.add_argument('--tree-id', help='Tree ID for consistency proof',
                        required=False)
    parser.add_argument('--tree-size', help='Tree size for consistency proof',
                        required=False, type=int)
    parser.add_argument('--root-hash', help='Root hash for consistency proof',
                        required=False)
    args = parser.parse_args()
    if args.debug:
        debug = True
        print("enabled debug mode")
    if args.checkpoint:
        # get and print latest checkpoint from server
        # if debug is enabled, store it in a file checkpoint.json
        checkpoint = get_latest_checkpoint(debug)
        print(json.dumps(checkpoint, indent=4))
    if args.inclusion:
        inclusion(args.inclusion, args.artifact, debug)
    if args.consistency:
        if not args.tree_id:
            print("please specify tree id for prev checkpoint")
            return
        if not args.tree_size:
            print("please specify tree size for prev checkpoint")
            return
        if not args.root_hash:
            print("please specify root hash for prev checkpoint")
            return

        prev_checkpoint = {}
        prev_checkpoint["treeID"] = args.tree_id
        prev_checkpoint["treeSize"] = args.tree_size
        prev_checkpoint["rootHash"] = args.root_hash

        consistency(prev_checkpoint, debug)

if __name__ == "__main__":
    main()

