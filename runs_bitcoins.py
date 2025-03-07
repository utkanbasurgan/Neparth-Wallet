#
# Copyright © 2024 by Neparth
#
#---------------------------------------------------------------------------------------------------------------------------------

import sys
import requests

def get_bitcoin_balance(address):
    url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        balance_satoshis = data['balance']
        final_balance_satoshis = data['final_balance']
        balance_btc = balance_satoshis / 100_000_000
        final_balance_btc = final_balance_satoshis / 100_000_000
        print(f"{final_balance_btc:.5f} BTC")
    else:
        print(f"Failed to retrieve balance for address {address}. Error code: {response.status_code}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_balance.py <bitcoin_address>")
    else:
        address = sys.argv[1]
        get_bitcoin_balance(address)

#---------------------------------------------------------------------------------------------------------------------------------

import ecdsa
import hashlib
import base58

def private_key_to_public_address(private_key_hex):
    # Step 1: Convert private key from hex to bytes
    private_key_bytes = bytes.fromhex(private_key_hex)
    
    # Step 2: Derive the public key using ECDSA (secp256k1)
    sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    public_key_bytes = b'\x04' + vk.to_string()
    
    # Step 3: Perform SHA-256 hash on the public key
    sha256_bpk = hashlib.sha256(public_key_bytes).digest()
    
    # Step 4: Perform RIPEMD-160 hash on the result of the SHA-256 hash
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256_bpk)
    public_key_hash = ripemd160.digest()
    
    # Step 5: Add version byte (0x00 for mainnet) in front of the public key hash
    versioned_payload = b'\x00' + public_key_hash
    
    # Step 6: Perform SHA-256 twice on the extended hash
    checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]
    
    # Step 7: Add the 4 checksum bytes at the end of the extended hash
    full_payload = versioned_payload + checksum
    
    # Step 8: Encode the result in Base58
    bitcoin_address = base58.b58encode(full_payload)
    
    return bitcoin_address.decode()

# Example usage
private_key_hex = '83ad24fc2857de9e46a5d37c0657adb95b30e19cf4c2f128032f3d4592904d5fes'
public_address = private_key_to_public_address(private_key_hex)
print("Bitcoin Address:", public_address)

#---------------------------------------------------------------------------------------------------------------------------------