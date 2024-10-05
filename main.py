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
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    

def get_verification_proof(log_index, debug=False):
    if isinstance(log_index, int):
        return True
    return False

def inclusion(log_index, artifact_filepath, debug=False):
    # verify that log index and artifact filepath values are sane
    entry = get_log_entry(log_index)
    for i in entry:
        #extract body and decode it
        code_string = base64.b64decode(entry[i]['body']).decode()
        newstr = ast.literal_eval(code_string) 

        #extract signature and certificate, decode again
        signature = newstr['spec']['signature']['content']
        certificate = base64.b64decode(newstr['spec']['signature']['publicKey']['content'])

        #obtain info to verify merkle proof 
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
    if get_verification_proof(log_index): 
        try:
            verify_artifact_signature(signature, public_key, artifact_filepath)
            verify_inclusion(DefaultHasher, index, tree_size, leaf_hash, hashes, root_hash)
            print("Offline root hash calculation for inclusion verified.")
        except Exception as e:
            print(e)
    else:
        print("Invalid log index")

#fetches checkpoint from transparency log 
def get_latest_checkpoint(debug=False):
    try:
        url = 'https://rekor.sigstore.dev/api/v1/log'
        response = requests.get(url)
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

def consistency(prev_checkpoint, debug=False):
    # verify that prev checkpoint is not empty
    if prev_checkpoint:
        #p_tree_id = prev_checkpoint["treeID"]
        p_tree_size = prev_checkpoint["treeSize"]
        p_root = prev_checkpoint["rootHash"]
    else:
        print("Previous checkpoint is empty")

    data = get_latest_checkpoint()
    c_tree_id = data['treeID']
    c_tree_size = data['treeSize']
    c_root = data['rootHash']

    #get consistency proof from Rekor server
    response = requests.get(f'https://rekor.sigstore.dev/api/v1/log/proof?firstSize={p_tree_size}&lastSize={c_tree_size}&treeID={c_tree_id}')
    consistency_proof = response.json()
    proof = consistency_proof['hashes']

    #verify new checkpoint is consistent with old checkpoint
    try:
        verify_consistency(DefaultHasher, p_tree_size, c_tree_size, proof, p_root, c_root)
        print("Consistency verification successful.")
    except Exception as e:
        print(e)

def main():
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
        json_object = json.dumps(checkpoint, indent=4)
        print(json_object)
        if debug:
            with open("checkpoint.json", "w") as outfile:
                outfile.write(json_object)
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