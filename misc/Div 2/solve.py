import socket

def recvuntil(s, delim):
    """Reads from the socket until a delimiter is found."""
    data = b''
    while delim not in data:
        chunk = s.recv(1)
        if not chunk:
            break
        data += chunk
    return data

# Server information - use either hostname or IP
HOST = "play.scriptsorcerers.xyz"
# HOST = "34.70.16.23" # Use if DNS fails
PORT = 10290

try:
    # Establish connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    # Initial range for the 128-bit secret
    low = 2**127
    high = 2**128

    # Perform binary search for approximately 128 iterations
    for i in range(130):
        if high - low <= 1:
            break

        recvuntil(s, b"Choice: ")
        s.sendall(b"1\n")

        recvuntil(s, b"Enter a number: ")

        # The number to send is the midpoint of the current range
        n = (low + high) // 2
        s.sendall(str(n).encode() + b"\n")

        # Read the integer division result
        response = recvuntil(s, b"\n").strip()
        d = int(response)

        # Narrow the range based on the result
        low = max(low, d * n)
        high = min(high, (d + 1) * n)

    # The secret is the final value of 'low'
    secret_guess = low
    print(f"Secret found: {secret_guess}")

    # Send the guess to the server to get the flag
    recvuntil(s, b"Choice: ")
    s.sendall(b"2\n")

    recvuntil(s, b"Enter secret number: ")
    s.sendall(str(secret_guess).encode() + b"\n")

    # Receive and print the flag
    flag = s.recv(4096).decode().strip()
    print(f"\nFlag: {flag}")

    s.close()

except (socket.gaierror, OSError) as e:
    print(f"Could not connect to the server due to a network error: {e}")
    print("Please run this script from a machine with network access to the challenge server.")