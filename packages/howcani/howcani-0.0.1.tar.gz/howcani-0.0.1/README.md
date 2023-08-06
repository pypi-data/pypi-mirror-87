# howcani

Command Line Utility to search for coding related queries.

howcani is inspired by [howdoi](https://github.com/gleitz/howdoi).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install howcani 
```

## Usage

```
$ howcani  upgrade pip
--------------------------------

pip is just a PyPI package like any other; you could use it to upgrade itself the same way you would upgrade any package:
pip install --upgrade pip

On Windows the recommended command is:
python -m pip install --upgrade pip


--------------------------------
$ howcani --help

usage: howcani [-h] [--count [COUNT]] [--plugin [PLUGIN]] q [q ...]

Command Line Utility to search for basic programming related queries.

positional arguments:
  q                  Query String to Search.

optional arguments:
  -h, --help         show this help message and exit
  --count [COUNT]    Number of Search Results to be entered.
  --plugin [PLUGIN]  Plugin to use: stackoverflow(s/default)


```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)