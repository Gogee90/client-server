import socket
import sys
import _thread

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)

client.connect(("127.0.0.1", 1234))

print(
    """
________
| |__| |
|  ()  |
|______|

Please enter command number 
and a word 
you want to change, 
e.g.: 1, your_text 

Commands:
1 - flip_letters_backwards;
2 - flip_letters;
3 - multiply_letters;

"""
)


def listen_server():
    while True:
        data = client.recv(2048)
        print(data.decode("utf-8"))


def send_server():
    _thread.start_new_thread(listen_server, ())

    while True:
        try:
            client.send(input().encode("utf-8"))
        except KeyboardInterrupt:
            client.shutdown(socket.SHUT_RDWR)
            client.close()
            sys.exit()


if __name__ == "__main__":
    send_server()
