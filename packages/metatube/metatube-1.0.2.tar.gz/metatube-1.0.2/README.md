# Download YouTube metadata for videos relating to a search query

This is a Python script that can download metadata (including comments and likes) for YouTube videos relating to a search query. Uses the [Youtube Data API v3](https://developers.google.com/youtube/v3/docs). Metadata is saved in a PostgreSQL database.

*Metatube* is conceived in a fashion that it pauses retrieval once your daily quota is used up (the default as of this writing is 10,000 requests per day) and waits until quota refill. If interrupted, *metatube* will, upon restart, first fill gaps in the download history, then continue downloading “into the future”. Once caught up to within ten minutes of the current time, *metatube* exits.

If you use *metatube* for scientific research, please cite it in your publication: <br />
Fink, C. (2020): *metatube: Python script to download YouTube metadata*. [doi:10.5281/zenodo.3773302](https://doi.org/10.5281/zenodo.3773302).


### Dependencies

The script is written in Python 3 and depends on the Python modules [dateparser](https://dateparser.readthedocs.io/), [psycopg2](https://www.psycopg.org/), [PyYaml](https://pyyaml.org/) and [Requests](https://2.python-requests.org/en/master/).

To install dependencies on a Debian-based system, run:

```shell
apt-get update -y &&
apt-get install -y python3-dev python3-pip python3-virtualenv
```

(There’s an Archlinux AUR package pulling in all dependencies, see further down)


### Installation

- *using `pip` or similar:*

```shell
pip3 install metatube
```

- *OR: manually:*

    - Clone this repository

    ```shell
    git clone https://gitlab.com/helics-lab/metatube.git
    ```

    - Change to the cloned directory    
    - Use the Python `setuptools` to install the package:

    ```shell
    cd metatube
    python3 ./setup.py install
    ```

- *OR: (Arch Linux only) from [AUR](https://aur.archlinux.org/packages/python-metatube):*

```shell
# e.g. using yay
yay python-metatube
```

### Configuration

Copy the example configuration file [metatube.yml.example](https://gitlab.com/helics-lab/metatube/-/raw/master/metatube.yml.example) to a suitable location, depending on your operating system: 

- on Linux systems:
    - system-wide configuration: `/etc/metatube.yml`
    - per-user configuration: 
        - `~/.config/metatube.yml` OR
        - `${XDG_CONFIG_HOME}/metatube.yml`
- on MacOS systems:
    - per-user configuration:
        - `${XDG_CONFIG_HOME}/metatube.yml`
- on Microsoft Windows systems:
    - per-user configuration:
        `%APPDATA%\metatube.yml`

Adapt the configuration:

- Configure a PostgreSQL connection string (`connection_string`), pointing to an existing database
- Configure an API [access key](https://developers.google.com/youtube/registering_an_application) to the Youtube Data API v3 (`youtube_api_key`).
- Define search terms (`search_terms`)

All of these configuration options can alternatively be supplied as command line arguments to `metatube` (see [Usage](#command-line-executable)) or as a `config` `dict` directly to the constructor of `YoutubeVideoMetadataDownloader`. Command line options (see `metatube --help`) or `config` `dict` both override config file.

### Usage

#### Command line executable

```shell
metatube \
    --postgresql-connection-string "dbname=metatube" \
    --youtube-api-key "abcdefghijklmn" \
    "how to build a tallbike"

```

#### Python

Import the `metatube` module. Instantiate a `YoutubeVideoMetadataDownloader`, optionally supply a `config` dictionary. Then run the instance’s `download()` method.

```python
import metatube

# config from config file
downloader = YoutubeVideoDownloader()
downloader.download()

# config from config file, 
# overriding `search_terms`
downloader = YoutubeVideoDownloader({
    "search_terms": "Critical Mass Vladivostok"
})
downloader.download()

# entire config from dictionary
downloader = YoutubeVideoDownloader({
    "youtube_api_key": "opqrstuvwxyz",
    "connection_string": "dbname=metatube host=server1 user=bicyclelover123",
    "search_terms": "dashcam bicycle commute albuquerque"
})
downloader.download()

```
