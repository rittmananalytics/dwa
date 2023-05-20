import argparse

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='A simple argparse program')

    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Subparser for 'input' command
    input_parser = subparsers.add_parser('input', help='Process input')
    input_parser.add_argument('path', type=str, help='Input file path')

    # Subparser for 'test' command
    test_parser = subparsers.add_parser('test', help='Run tests')
    test_parser.add_argument('example', type=str, help='Test example')

    # Subparser for 'build' command
    build_parser = subparsers.add_parser('build', help='Build something')
    build_parser.add_argument('example', type=str, help='Build example')

    # Parse the arguments
    args = parser.parse_args()

    # Process based on the command
    if args.command == 'input':
        process_input(args.path)
    elif args.command == 'test':
        run_tests(args.example)
    elif args.command == 'build':
        build_something(args.example)
    else:
        print('Invalid command')

def process_input(path):
    print(f'Processing input: {path}')

def run_tests(example):
    print(f'Running tests for: {example}')

def build_something(example):
    print(f'Building: {example}')

if __name__ == "__main__":
    main()