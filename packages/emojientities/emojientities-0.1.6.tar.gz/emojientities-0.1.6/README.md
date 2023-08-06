# emoji entities

This module downloads the latest list of emoji characters from unicode.org and adds `string.emojis`, a concatenated `str` containing all characters, to be used just as the other string entities (e.g. `string.letters`).

## Dependencies

    requests

## Installation

- *using `pip` or similar:*

```shell
pip install emojientities
```

- *manually:*

    - Clone this repository

    ```shell
    git clone https://gitlab.com/christoph.fink/python-emojientities.git
    ```

    - Change to the cloned directory    
    - Use the Python `setuptools` to install the package:

    ```shell
    python ./setup.py install
    ```
## Usage

This module extends the character classes provided by the `string` standard library to include an `emoji` range. To use it, import `emojientities` and `string` and use `string.emojis` to, for instance, filter emojis in a text:

```python
import emojientities
import string

# example string from: Hiippala et al. (2018) Exploring the linguistic landscape of 
# geotagged social media content in urban environments. Digital Scholarship in the Humanities.
photoCaption = "Great weather in Helsinki!!! On holiday with @username.:-) #helsinki #visitfinland 🤓☀️🛳️"

emojisOnly = "".join(
    [c for c in photoCaption if c in string.emojis]
)
# '🤓☀️🛳️'

photoCaptionWithoutEmojis = "".join(
    [c for c in photoCaption if c not in string.emojis]
)
# 'Great weather in Helsinki!!! On holiday with @username.:-) #helsinki #visitfinland '

```

