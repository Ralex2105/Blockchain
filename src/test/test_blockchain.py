import threading
import time
import json

import src.main.Node as node
import src.main.Server as server


def test_start_node():
    server_id = 1
    current_node = node.Node(server_id)
    new_server = threading.Thread(target=server.start, args=(server_id, current_node))
    new_server.setDaemon(True)
    new_server.start()
    while current_node.block_index is None:
        time.sleep(0.4)
    assert len(current_node.list_block) == 1
    python_object = json.loads(current_node.list_block[0])
    prev_hash = python_object['prev_hash']
    index = python_object['index']
    assert prev_hash == 'GENESIS'
    assert index == 0


def test_valid_blockchain():
    node1 = node.Node(1)
    node2 = node.Node(2)
    node3 = node.Node(3)
    server1 = threading.Thread(target=server.start, args=(1, node1))
    server1.setDaemon(True)
    server2 = threading.Thread(target=server.start, args=(2, node2))
    server2.setDaemon(True)
    server3 = threading.Thread(target=server.start, args=(3, node3))
    server3.setDaemon(True)
    server3.start()
    server2.start()
    server1.start()
    while len(node1.list_block) < 50 or len(node2.list_block) < 50 or len(node3.list_block) < 50:
        time.sleep(0.1)
    for i in range(5000):
        b_node1 = json.loads(node1.list_block[i])
        b_node2 = json.loads(node2.list_block[i])
        b_node3 = json.loads(node3.list_block[i])
        assert b_node1 == b_node2 == b_node3
