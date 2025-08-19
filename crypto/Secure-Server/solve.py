import argparse

def xor_hex_strings(*hex_strings: str) -> bytes:
    """
    Accepts multiple hex-encoded strings, decodes them to bytes,
    and cumulatively XORs them together.

    Args:
        *hex_strings: A variable number of hex-encoded strings.

    Returns:
        A bytes object representing the final XORed result.
    
    Raises:
        ValueError: If any of the input strings are not valid hex.
    """
    if not hex_strings:
        raise ValueError("At least one hex string must be provided.")

    # Initialize the result with the first decoded hex string
    try:
        result_bytes = bytes.fromhex(hex_strings[0])
    except ValueError:
        raise ValueError(f"Invalid hex string provided: {hex_strings[0]}")

    # Cumulatively XOR the remaining strings
    for hex_str in hex_strings[1:]:
        try:
            next_bytes = bytes.fromhex(hex_str)
            # XOR byte-by-byte. zip() stops at the shortest length, which is
            # the standard behavior for this type of CTF challenge.
            result_bytes = bytes(a ^ b for a, b in zip(result_bytes, next_bytes))
        except ValueError:
            raise ValueError(f"Invalid hex string provided: {hex_str}")
            
    return result_bytes

def main():
    """
    Main function to parse arguments and run the XOR tool.
    """
    parser = argparse.ArgumentParser(
        description="A tool to cumulatively XOR multiple hex strings. "
                    "Can be run with hex strings as arguments or in interactive mode.",
        epilog="Example CLI use: python xor_tool.py <hex1> <hex2> <hex3>"
    )
    parser.add_argument(
        'hex_strings',
        nargs='*',  # Allows for zero or more arguments
        help="One or more hex-encoded strings to XOR together."
    )
    args = parser.parse_args()

    input_strings = []
    if args.hex_strings:
        # --- CLI Mode ---
        print("Running in Command-Line Mode...")
        input_strings = args.hex_strings
    else:
        # --- Interactive Mode ---
        print("Running in Interactive Mode (no arguments detected).")
        print("Please provide the hex strings for the Secure-Server challenge.")
        try:
            enc = input("Enter the first client hex string (enc):  ").strip()
            enc2 = input("Enter the server hex string (enc2):      ").strip()
            dec = input("Enter the second client hex string (dec): ").strip()
            if not (enc and enc2 and dec):
                print("\nError: All three strings are required. Aborting.")
                return
            input_strings = [enc, enc2, dec]
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled by user. Exiting.")
            return

    try:
        print("\n--- Processing ---")
        final_result_bytes = xor_hex_strings(*input_strings)
        
        print("\n--- Result ---")
        print(f"Raw Hex Output: {final_result_bytes.hex()}")

        try:
            decoded_string = final_result_bytes.decode('utf-8')
            print(f"Decoded (UTF-8): {decoded_string}")
            # Automatically format for the specific challenge
            if "scriptCTF" not in decoded_string:
                 print(f"Formatted Flag:  scriptCTF{{{decoded_string}}}")
        except UnicodeDecodeError:
            print("Decoded (UTF-8): Failed. Result contains non-UTF-8 bytes.")
            
    except ValueError as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()