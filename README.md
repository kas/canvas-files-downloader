# canvas-files-downloader

Downloads your Canvas course files, group submissions, and user submissions

## Usage

* Requires Python 3
* Create `.env`
  * Generate an access token for testing
    * https://canvas.instructure.com/doc/api/file.oauth.html#manual-token-generation
  * ```
    ACCESS_TOKEN=
    ```
    * Put your access token after the equals sign
* Create a virtual environment and activate it
  * `python3 -m venv venv`
  * `source venv/bin/activate`
* Install dependencies
  * `pip install -r requirements.txt`
* Run the script
  * `python canvas-files-downloader.py`
* Files will be downloaded to `files/`
