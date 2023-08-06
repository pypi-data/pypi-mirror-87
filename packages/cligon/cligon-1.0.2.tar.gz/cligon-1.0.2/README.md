# C.L.I.G.O.N

## Introduction

C.L.I.G.O.N or Cligon is an acronym that stands for Check if Link Is Good Or Not.
It is designed to check all website links inside a file. This program was written in Python 3.8.2.
It will return a list of good, bad, or unknown URL statuses.
- good urls are status code 200.
- bad urls are status codes 400 or 404.
- unknowns are status codes that aren't bad or good.

## Usage
For prerequisites please see [CONTRIBUTING](./CONTRIBUTING.md).

To use Cligon, please run in a terminal of your choice:
```bash
python3 cligon.py [file name]
```
Or, if executable privileges are invoked in a Linux environment (chmod +x cligon):
```bash
./cligon [file name]
```
Ensure you make a copy of cligon.py (cp cligon.py cligon) to execute the command above.

Additionally, instructions and options can be viewed by running Cligon without any arguments.

## Features
- Colorized output: good = green, red = back, grey/white = unknown
- Version number argument
- Parallelism / Multi-threading (It's fast-ish)
- Grabs HEAD only
- URL timeout (default 2.5 milliseconds)
- Output JSON format
- Output only good or bad urls

## License

MIT
