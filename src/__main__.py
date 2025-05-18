# Allows running the package with `python -m src` if desired
from .cli import parse_args
from .organizer import process_file
from .duplicates import find_duplicates
from .utils import BANNER

def main():
    print(BANNER)
    # ...main logic here...

if __name__ == "__main__":
    main()
