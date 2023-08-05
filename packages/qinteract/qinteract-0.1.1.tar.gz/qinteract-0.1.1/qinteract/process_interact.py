# coding:utf8
# python3

import sys
import re
import subprocess
from threading import Thread


class ProcessInteraction:
    """Interaction with a console process

    Returns:
        Instance: Instance of ProcessInteraction
    """
    process = None

    def __init__(self, command):
        """init

        Args:
            command (list): a command in the form of a list 
        """
        self.process = subprocess.Popen(
            command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def __del__(self):
        """Close process stdin/stdout
        """
        self.process.stdin.close()
        self.process.stdout.close()

    def recvline(self):
        """Get one line of content

        Returns:
            str: one line of content
        """
        return self.process.stdout.readline().decode('utf8')

    def recv_n(self, n):
        """Gets the content of the specified length

        Args:
            n (int): the specified length

        Returns:
            str: the content of the specified length
        """
        return self.process.stdout.read(n).decode('utf8')

    def recvuntil(self, want_end_str):
        """Get the content to the specific end

        Args:
            want_end_str (str): the specific end

        Returns:
            str: the content to the specific end
        """
        current_str = ''
        while True:
            current_str += self.recv_n(1)
            if current_str.endswith(want_end_str):
                return current_str

    def recvuntil_re(self, want_re_str):
        """Get the content to the specific regex end

        Args:
            want_end_str (str): the specific regex end

        Returns:
            str: the content to the specific regex end
        """
        current_str = ''
        while True:
            current_str += self.recv_n(1)
            s = re.search(want_re_str, current_str)
            if s:
                return [current_str, s]

    def send(self, send_str):
        """Send the content

        Args:
            send_str (str): the content want to send
        """
        final_bytes = send_str.encode('utf8')
        self.process.stdin.write(final_bytes)
        self.process.stdin.flush()

    def sendline(self, send_str):
        """Send the content and a linefeed

        Args:
            send_str (str): the content wat to send
        """
        self.send(send_str+'\n')
    
    def interact(self):
        """Auto get and wait input to send
        """
        def recv_loop():
            """Auto get content
            """
            while True:
                c = self.recv_n(1)
                # There will be a delay when "print" to the console. Write directly with system io
                sys.stdout.write(c)
                sys.stdout.flush()

        def send_loop():
            """Wait input and send
            """
            while True:
                send_str = input()
                self.sendline(send_str)

        recv_thread = Thread(target=recv_loop)
        send_thread = Thread(target=send_loop)

        recv_thread.start()
        send_thread.start()

        recv_thread.join()
        send_thread.join()
