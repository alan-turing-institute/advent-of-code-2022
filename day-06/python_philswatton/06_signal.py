from argparse import ArgumentParser

# Usage: python 00_template.py input_file_path
def get_input_file_path() -> str:
    parser = ArgumentParser(description="AOC Day 0 Function")
    parser.add_argument("input_file_path") # required (positional) arguments
    args = parser.parse_args()
    return args.input_file_path

# Function to search for first instance of 4 unique characters
def signal_search(signal: str, marker_length: int) -> int:
    start = 0
    finish = marker_length
    length = len(signal)
    while finish <= length:
        marker = signal[start:finish]
        if len(set(marker)) == marker_length:
            return finish
        start += 1
        finish += 1

# Main
def main():
    # Get file path
    file_path = get_input_file_path()
    
    # Read in input file
    with open(file_path) as input_file:
        stream = input_file.read().rstrip()
        print("Start of packet: " + str(signal_search(stream, 4)))
        print("Start of message: " + str(signal_search(stream, 14)))

# Run
if __name__ == "__main__":
    main()