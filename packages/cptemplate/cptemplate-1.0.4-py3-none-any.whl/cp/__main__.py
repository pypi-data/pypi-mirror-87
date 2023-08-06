import click
import os
import platform

template = '''
#---<Libraries>---#
import os
import sys
import math
import numpy
import collections
import itertools
from io import BytesIO, IOBase

#---<Fast I/O>---#
BUFSIZE = 8192

class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None

    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)


class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")

sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)

#---<Input & Print>---#

def scanf(datatype = str):
    if datatype is not None:
        return datatype(sys.stdin.readline())
    else:
        return sys.stdin.readline()

def printf(answer):
    return sys.stdout.write(str(answer) + "\\n")

def map_input(datatype):
    return map(datatype, sys.stdin.readline().split())

def list_input(datatype):
    return list(map(datatype, sys.stdin.readline().split()))

def testcase(number: int, solve_function):
    while (number != 0):
        solve_function()
        number -= 1

#---<Mathematical Operations>---#

def gcd(num1: int, num2: int): #greatest common divisor
    if num1 == 0:
        return num2
    if num2 == 0:
        return num1
    if num1 > num2:
        return gcd(num1 % num2, num2)
    else:
        return gcd(num1, num2 % num1)

def lcm(num1: int, num2: int): #lowest common multiple
    return (num1 * num2) // gcd(num1, num2)

def big_power(num1: int, num2: int):
    result = 1
    while (num2 > 0):
        if num2 & 1:
            result = result * num1
        num1 = num1 ** 2
        num2 >>= 1
    return result

#---<Algorithms>---#

def sieve_of_eratosthenes(number: int):
    num1 = (number - 1) // 2
    arr = [True] * num1
    num2, num3, primes = 0, 3, [2]
    while (num3 * num3 < number):
        if arr[num2]:
            primes.append(num3)
            num4 = 2 * num2 * num2 + 6 * num2 + 3
            while (num4 < num1):
                arr[num4] = False
                num4 = num4 + 2 * num2 + 3
        num2 += 1
        num3 += 1
    while (num2 < num1):
        if arr[num2]:
            primes.append(num3)
        num2 += 1
        num3 += 2
    return primes

def dfs(graph, start, visited = None): #depth first search
    """
    Here 'graph' represents the adjacency list
    of the graph, and 'start' represents the
    node from which to start
    """
    if visited is None:
        visited = set()
    visited.add(start)
    for next in (graph[start] - visited):
        dfs(graph, next, visited)
    return visited

def dfs_paths(graph, start, goal):
    """
    Returns all possible paths between a
    start vertex and a goal vertex
    """
    stack = [(start, [start])]
    while (stack):
        (vertex, path) = stack.pop()
        for next in (graph[vertex] - set(path)):
            if next == goal:
                yield path + [next]
            else:
                stack.append((next, path + [next]))
    return stack

def bfs(graph, start): #breadth first search
    visited, queue = set(), [start]
    while (queue):
        vertex = queue.pop(0)
        if (vertex not in visited):
            visited.add(vertex)
            queue.extend(graph[vertex] - visited)
    return visited

def bfs_paths(graph, start, goal):
    """
    Returns all possible paths between a
    start vertex and a goal vertex, where
    the first path is the shortest path
    """
    queue = [(start, [start])]
    while (queue):
        (vertex, path) = queue.pop(0)
        for next in (graph[vertex] - set(path)):
            if (next == goal):
                yield path + [next]
            else:
                queue.append((next, path + [next]))
    return queue

#---<Testcases>---#
#sys.stdin = open('input.txt', 'r')
#sys.stdout = open('output.txt', 'w')
'''

@click.group()
def cptemplate():
    "competitive programming template for python"

@click.option("-n", "--file_name", help = "Set custom name for file")
@cptemplate.command()
def new(file_name: str):
    "create a new template file, default name new.py"

    if file_name is not None:
        file = open(f'{file_name}.py', 'w')
        file.write(template)
        file.close()

    else:
        file = open('new.py', 'w')
        file.write(template)
        file.close()

@click.option("-n", "--file_name", help = "Open .py file with custom name")
@cptemplate.command()
def test(file_name: str):
    "run and test the code, by default runs new.py"

    if file_name is not None:
        try:
            if platform.system() == 'Linux' or platform.system() == 'Darwin':
                os.system(f'cmd /k "python3 {file_name}.py"')
            elif platform.system() == 'Windows':
                os.system(f'cmd /k "python {file_name}.py"')
        except:
            print(f'An error occured, check {file_name}.py file')

    else:
        try:
            if platform.system() == 'Linux' or platform.system() == 'Darwin':
                os.system('cmd /k "python3 new.py"')
            elif platform.system() == 'Windows':
                os.system('cmd /k "python new.py"')
        except:
            print('An error occured, check new.py file')

@cptemplate.command()
def info():
    "information about the module"

    info = [
        '\ncptemplate is a python library for making a pre-defined template for competitive programming',
        'It is an open-source project, made by Devansh, available on PyPi',
        'View on GitHub: https://github.com/Devansh3712/cptemplate',
        'View on PyPi: https://pypi.org/project/cptemplate/'
    ]

    for line in info:
        print(line)

if __name__ == "__main__":
    cptemplate(prog_name = "cptemplate")