import argparse

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='A simple argparse program')

    # Add arguments
    parser.add_argument('input', type=str, help='Input file path')

    # Parse the arguments
    args = parser.parse_args()

    # Use the arguments
    print(f'Input file: {args.input}')

if __name__ == "__main__":
    main()
