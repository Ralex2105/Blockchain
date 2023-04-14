from flask import Flask, request
import time
import threading
import grequests
import json
import Block


def start(host, current_node):
    current_server = Flask(__name__)
    if host == 1:
        current_port = 5000
        port2 = 5001
        port3 = 5002
    elif host == 2:
        current_port = 5001
        port2 = 5000
        port3 = 5002
    else:
        current_port = 5002
        port2 = 5000
        port3 = 5001
    servers_urls = [f'http://localhost:{current_port}/', f'http://localhost:{port2}/', f'http://localhost:{port3}/']

    def new_blocks_generator():
        while True:
            if len(current_node.list_block) != 0:
                prev_hash = json.loads(current_node.list_block[-1])['hash']
                new_block = Block.create_new_block(current_node.block_index + 1, prev_hash, current_node.host, host)
                if new_block.index > current_node.block_index:
                    grequests.map((grequests.post(u, json=new_block.block_to_json()) for u in servers_urls))
            time.sleep(0.4)

    @current_server.route("/", methods=['POST'])
    def server_handler():
        if not current_node.block_handler(request.get_json()):
            return "Error"
        return "new Block"
    current_server = threading.Thread(target=current_server.run, args=('localhost', current_port))
    server_generator = threading.Thread(target=new_blocks_generator)
    current_server.setDaemon(False)
    server_generator.setDaemon(False)
    current_server.start()
    server_generator.start()
    if host == 1:
        time.sleep(1)
        genesis_block = Block.create_genesis()
        rs = (grequests.post(u, json=genesis_block) for u in servers_urls)
        grequests.map(rs)