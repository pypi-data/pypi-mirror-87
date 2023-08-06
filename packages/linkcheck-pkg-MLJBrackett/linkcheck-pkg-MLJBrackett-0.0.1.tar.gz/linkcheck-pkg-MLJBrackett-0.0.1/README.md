# Link Check

Link Check is a Python program for finding good/dead links in any file type.

![Link Check](https://i.gyazo.com/4e7e46ca83fc24950ad70194ab222b63.gif)

## Usage
**Install the program requirements prior to use**

```bash
pip install -r requirements.txt
```

**For the program to run with a file you must either use the -f or -r flag**

Use the -h/--help flags to see arguements
```bash
python link_check.py -h
```
![Help](https://i.gyazo.com/5eccaf4307f1a95f7db199f82141d992.png)

Check URLs **without** redirect support
```bash
python link_check.py -f links.txt
```
![File](https://i.gyazo.com/4e7e46ca83fc24950ad70194ab222b63.gif)

Check URLs **with** redirect support (Redirection causes the program to run slower)
```bash
python link_check.py -r links.txt
```
![Redirect](https://i.gyazo.com/a5642797c002d9bd04b3dd59d4824d5c.gif)

Output only good URLS
```bash
python link_check.py -g -f links.txt
```
![GoodURLS](https://i.gyazo.com/f46decc645eaff347d99cd7ee94c5e43.gif)

Output only bad URLS
```bash
python link_check.py -b -f links.txt
```
![BadURLS](https://i.gyazo.com/e4983e267a6dcf10b54d8b4b7f553efc.gif)

JSON formatted output of URLS
```bash
python link_check.py -j -f links.txt
```
![JSON](https://i.gyazo.com/d41916822039f8fac2e60ba4c1afb6f5.png)

Check version of tool
```bash
python link_check.py -v
```
![Version](https://i.gyazo.com/23be09cff4fb01dccc2ba4178802db2c.png)

**You can use -j & -g/-b to get an JSON output of only good/bad URLS**
```bash
python link_check.py -j -g -f links.txt
```

## Contributing
Contributions are welcomed please check [CONTRIBUTING.md](CONTRIBUTING.md), if you think you have a good idea or see an improvement that you can make, create an issue or submit a pull request.

## License
Distributed under the [MIT](https://choosealicense.com/licenses/mit/) License. See LICENSE for more information.
