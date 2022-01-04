from server import handler
from picklelib import loads, dumps
from time import sleep

if __name__ == '__main__':
    with open('/data/dumped.txt', 'r') as f:
        dumped = f.read()
    event = {'dumped': dumped}
    print(loads(handler(event)))
