import argparse
import Server
import Node
from gevent import monkey

monkey.patch_all()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('host', nargs='?')
    args = parser.parse_args().host
    current_node = Node.Node(int(args))
    Server.start(int(args), current_node)
