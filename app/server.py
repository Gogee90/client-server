import json
import socket
import time
from utils import flip_letters, multiply_letters, flip_letters_backwards, is_valid_uuid
import uuid
import _thread


server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)


server.bind(("127.0.0.1", 1234))

server.listen(5)
print("Server is listening")

users = []

tasks = []


def check_status(status_id):
    status = ""
    for task in tasks:
        status = task["status"]
        if task["status"] == "Done" and task["id"] == status_id:
            return json.dumps(task).encode("utf-8")
    return status.encode("utf-8")


def create_task(data, result):
    global tasks
    data = data.decode("utf8").split(", ")
    result["status"] = "In Progress"
    tasks.append(result)
    for command in data:
        if command == "1":
            time.sleep(30)
            result["new_word"] = flip_letters_backwards(data[-1])
            result["status"] = "Done"
        if command == "2":
            time.sleep(5)
            result["new_word"] = flip_letters(data[-1])
            result["status"] = "Done"
        if command == "3":
            time.sleep(7)
            result["new_word"] = multiply_letters(data[-1])
            result["status"] = "Done"
    tasks.append(result)
    return


def start_task(data):
    print(data)
    result = {}
    result["id"] = str(uuid.uuid4())
    result["status"] = "Pending"
    _thread.start_new_thread(
        create_task,
        (
            data,
            result,
        ),
    )
    return result["id"]


def send_all(data):
    for user in users:
        user.send(data)


def listen_user(user):
    print("Listening user")

    while True:
        data = user.recv(2048)
        print(f"User sent {data}")

        if not data:
            users.remove(user)
            break

        if is_valid_uuid(data.decode("utf8")):
            send_all(check_status(data.decode("utf8")))
        else:
            send_all(start_task(data).encode("utf8"))


def start_server():
    while True:
        user_socket, address = server.accept()
        print(f"User <{address[0]}> connected!")

        users.append(user_socket)
        _thread.start_new_thread(listen_user, (user_socket,))


if __name__ == "__main__":
    start_server()
