import json
import socket

HOST = "127.0.0.1"
PORT = 9000
TOPIC = "/robot/speed"


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        request = {"action": "subscribe", "topic": TOPIC}
        client.sendall(json.dumps(request).encode("utf-8"))
        print(f"[SUBSCRIBED] {TOPIC}")
        print("[WAITING] Run publisher.py in another terminal...")

        raw = client.recv(1024)
        if raw:
            message = json.loads(raw.decode("utf-8"))
            print(f"[RECEIVED] {message}")
        else:
            print("[DISCONNECTED] Broker closed connection without sending data")


if __name__ == "__main__":
    try:
        main()
    except ConnectionRefusedError:
        print("[ERROR] Start mini_broker.py first")
    except KeyboardInterrupt:
        print("\n[SUBSCRIBER] Stopped")
