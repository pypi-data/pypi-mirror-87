import argparse
from datupie.function_maps import FUNCTION_MAP
#from function_maps import FUNCTION_MAP

def main():    
#if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=FUNCTION_MAP.keys())
    args = parser.parse_args()
    func = FUNCTION_MAP[args.command]
    func()