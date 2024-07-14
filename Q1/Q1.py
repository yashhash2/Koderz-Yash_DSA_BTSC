import hashlib

def compute_sha256_hash(message):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(message.encode('utf-8'))
    return sha256_hash.hexdigest()

# Alice's message
message = "Hello Bob, let's meet at 5 PM."
# Compute the hash of the message
message_hash = compute_sha256_hash(message)

print(f"Message: {message}")
print(f"Hash: {message_hash}")

def verify_message(received_message, received_hash):
    computed_hash = compute_sha256_hash(received_message)
    if computed_hash == received_hash:
        print("The message is authentic and has not been tampered with.")
    else:
        print("The message integrity is compromised.")

# Received message and hash from Alice
received_message = "Hello Bob, let's meet at 5 PM."
received_hash = "21cfebaff8a7cb6c7a6b47b4de9874849dc1178231f78b439ed48e2ca8ff5bb0"

# Verify the received message
verify_message(received_message, received_hash)




