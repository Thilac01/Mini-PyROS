import json
import socket

HOST = "127.0.0.1"
PORT = 9000


def main():
    message = {
        "action": "publish",
        "topic": "/robot/speed",
        "data": 2.5,
    }
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        client.sendall(json.dumps(message).encode("utf-8"))
    print(f"[PUBLISHED] {message}")


if __name__ == "__main__":
    try:
        main()
    except ConnectionRefusedError:
        print("[ERROR] Start mini_broker.py first")
