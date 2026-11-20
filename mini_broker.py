import json
import socket

HOST = "127.0.0.1"
PORT = 9000


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"[BROKER] Listening on {HOST}:{PORT}", flush=True)

        subscriber, address = server.accept()
        with subscriber:
            print(f"[SUBSCRIBER CONNECTED] {address}", flush=True)
            request = subscriber.recv(1024).decode("utf-8")
            subscription = json.loads(request)

            if subscription.get("action") != "subscribe":
                print("[ERROR] First client must subscribe")
                return
            topic = subscription.get("topic")
            if not isinstance(topic, str):
                print("[ERROR] Invalid subscription topic")
                return
            print(f"[SUBSCRIBE] {topic}", flush=True)


          
            publisher, address = server.accept()
            with publisher:
                print(f"[PUBLISHER CONNECTED] {address}", flush=True)
                request = publisher.recv(1024).decode("utf-8")
                message = json.loads(request)

                if message.get("action") != "publish":
                    print("[ERROR] Second client must publish")
                    return

                published_topic = message.get("topic")
                print(f"[PUBLISH] {published_topic}: {message.get('data')}", flush=True)
                if published_topic == topic:
                    subscriber.sendall(json.dumps(message).encode("utf-8"))
                    print("[FORWARDED] Message sent to subscriber", flush=True)
                else:
                    print("[SKIPPED] Topics do not match", flush=True)

    print("[BROKER] Finished. Restart to test another message.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[BROKER] Stopped")
