from simplecrypt import encrypt, decrypt
ciphertext = encrypt('password', plaintext)
plaintext = decrypt('password', ciphertext)

print(ciphertext, plaintext)
