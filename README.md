# canvas-files-downloader

Downloads your Canvas course files, group submissions, and user submissions

## Usage

* Requires Python 3
* Create `.env`
  * Generate an access token for testing
    * https://canvas.instructure.com/doc/api/file.oauth.html#manual-token-generation
  * ```
    ACCESS_TOKEN=
    BASE_URL=
    ```
    * Put your access token after the equals sign
    * Add your school's canvas URL. Example: `BASE_URL=https://lms.yourschool.edu`
* Create a virtual environment and activate it
  * `python3 -m venv venv`
  * `./venv/Scripts/activate`
* Install dependencies
  * `pip install -r requirements.txt`
* Run the script
  * `python canvas-files-downloader.py`
* Files will be downloaded to `files/`
