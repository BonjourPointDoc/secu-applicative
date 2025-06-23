import socket
import ssl
import threading
from cryptography import x509
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

HOST = '0.0.0.0'
PORT = 8443

# --- Chargement certificat et clés ---
with open("cert.pem", "rb") as f:
    cert_data = f.read()
cert = x509.load_pem_x509_certificate(cert_data, default_backend())
public_key = cert.public_key()
pem_public_key = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
with open("key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None,
        backend=default_backend()
    )

# --- Contexte TLS ---
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

def handle_client(conn, addr):
    print(f"New client: {addr}")
    try:
        # Envoyer clé publique
        conn.sendall(pem_public_key)
        print(f"Public key sent to {addr}")

        while True:
            alea_data = b""
            while len(alea_data) < 256:
                chunk = conn.recv(256 - len(alea_data))
                if not chunk:
                    print(f"Client {addr} disconnected")
                    return
                alea_data += chunk
            print(f"[+] Received {len(alea_data)} bytes from {addr}")

            signature = private_key.sign(
                alea_data,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            conn.sendall(signature)
            print(f"Signature sent to {addr} ({len(signature)} bytes)")

    except Exception as e:
        print(f"Error whit client {addr}: {e}")
    finally:
        conn.close()
        print(f"Connexion closed with {addr}")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))
        sock.listen(5)
        print(f"TLS ready on {HOST}:{PORT}")

        while True:
            try:
                client_sock, addr = sock.accept()
                tls_conn = context.wrap_socket(client_sock, server_side=True)
                # A thread by client
                client_thread = threading.Thread(target=handle_client, args=(tls_conn, addr), daemon=True)
                client_thread.start()

            except KeyboardInterrupt:
                print("\n[*] Server stop")
                break
            except Exception as e:
                print(f"[-] Server error : {e}")
                continue

if __name__ == "__main__":
    main()
