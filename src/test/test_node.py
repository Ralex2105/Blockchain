import random

import src.main.Node as node
import src.main.Block as block


def test_node():
    test_node_1()
    test_node_2()


def test_node_1():
    for i in range(10):
        host = random.randint(1, 3)
        new_node = node.Node(host)
        assert new_node is not None
        assert new_node.host == host
        assert new_node.block_index is None

        host = random.randint(1, 3)
        current_node = node.Node(host)
        genesis_block = block.create_genesis()
        assert current_node.host == host
        assert current_node.block_index is None

        current_node.block_handler(genesis_block)
        assert current_node.host == host
        assert current_node.block_index == 0


def test_node_2():
    node_host = random.randint(1, 3)
    current_node = node.Node(node_host)

    for i in range(10):
        block_server_id = random.randint(1, 3)
        last_index = random.randint(1, 1000)
        prev_hash = 'This is Last block in Node'
        nonce_type = random.randint(1, 3)

        last_block_in_node_array = block.create_new_block(last_index, prev_hash, nonce_type,
                                                          block_server_id).block_to_json()
        current_node.block_index = last_index
        current_node.list_block.append(last_block_in_node_array)

        answer_false = current_node.block_handler(last_block_in_node_array)
        assert answer_false is False

        last_block_array_length = len(current_node.list_block)
        new_index = random.randint(1, 1000)
        new_prev_hash = 'This is new Received block'
        new_received_block = block.create_new_block(new_index, new_prev_hash, nonce_type,
                                                    block_server_id).block_to_json()
        answer_block_handler = current_node.block_handler(new_received_block)

        if new_index > last_index:
            assert answer_block_handler is True
            assert current_node.block_index == new_index
            assert len(current_node.list_block) == last_block_array_length + 1
        else:
            assert answer_block_handler is False
            assert current_node.block_index == last_index
            assert len(current_node.list_block) == last_block_array_length
