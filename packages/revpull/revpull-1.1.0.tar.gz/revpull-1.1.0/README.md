# revpull

**revpull** is a tool for pulling data from IBM eReview.

## Description

This tool allows you to download content that is allowed for you from eReview using its API. As a result, you get a local copy of the eReview content with the original data structure.

## Environment
* Languages: Python
* Interface: CLI
* Supported OS: Linux, OS X

## Installation

**Requirements:**

 * Python (>=3.6)

**Linux:**
~~~
 $ pip install revpull
~~~

**OS X:**
~~~
 $ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
 $ python3 get-pip.py revpull
~~~

## Usage

```
Usage:
    revpull --dir=TARGET_DIR_PATH --auth=W3ID_AUTH
    revpull -h | --help
    revpull -v | --version

Options:
    --dir=TARGET_DIR_PATH           Set the path to the directory where the content will be saved
    --auth=W3ID_AUTH                Set the uername:password value for authentication
    -h, --help                      Show this help message.
    -v, --version                   Show the version.
```

## Additional info
>The app is currently under development. The app may contain bugs. **Use at your own risk**.

## Contributing

1.  Fork it.
2.  Create your feature branch:  `git checkout -b my-new-feature`
3.  Commit your changes:  `git commit -am 'Add some feature'`
4.  Push to the branch:  `git push origin my-new-feature`
5.  Submit a pull request

## License
The MIT License (MIT)

Copyright (c) 2020 Mikalai Lisitsa

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
