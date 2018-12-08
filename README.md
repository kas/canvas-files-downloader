# canvas-files-downloader

Downloads your Canvas files

## Usage

* Requires Python 3
* Create `.env`
  * Get your access token from https://canvas.instructure.com/doc/api/file.oauth.html
  * Put your access token after the equals sign
  * ```
    ACCESS_TOKEN=
    ```
* Create a virtual environment
  * `python3.7 -m venv venv`
  * `source venv/bin/activate`
* Install dependencies
  * `pip install -r requirements.txt`
* `python canvas-files-downloader.py`
* Files will be downloaded to `files/`
