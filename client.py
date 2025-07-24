from DiffieHellman import generate_dh_keypair, compute_shared_secret
import socket
import json

# Prepare key pair and parameters
my_priv, my_pub, params = generate_dh_keypair()
p, q, g = params

# Set up TCP client
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(('localhost', 9001))

    # Send our public key and parameters to server
    data = {
        'public': my_pub,
        'p': p,
        'q': q,
        'g': g
    }
    sock.sendall(json.dumps(data).encode())

    # Wait for server’s public key
    try:
        resp = sock.recv(4096)
        other = json.loads(resp.decode())
        server_pub = other['public']
    except Exception as e:
        print("Failed to get server response:", e)
        exit(1)

    # Compute shared key
    shared = compute_shared_secret(server_pub, my_priv, (p, q, g))
    print("Shared key established.")
