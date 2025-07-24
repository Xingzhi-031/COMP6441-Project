import socket
import json
from DiffieHellman import generate_dh_keypair, compute_shared_secret

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 9001))
sock.listen()
print("Waiting for connection on port 9001...")

client_sock, client_addr = sock.accept()
print(f"[+] Incoming from {client_addr[0]}:{client_addr[1]}")

raw = client_sock.recv(4096)
data = json.loads(raw.decode())
peer_pub = data.get("public")
params = (data.get("p"), data.get("q"), data.get("g"))

# Create local DH key pair (matching parameters)
priv, pub, _ = generate_dh_keypair()

# Send our public key
client_sock.sendall(json.dumps({'public': pub}).encode())

# Compute the shared key
session_key = compute_shared_secret(peer_pub, priv, params)
print("✔️ Secure key exchange complete (server).")
client_sock.close()
sock.close()
