# Python wrapper for the webis Twitter sentiment evaluation ensemble

This is a Python wrapper around the Java implementation of a Twitter sentiment evaluation framework presented by [Hagen et al. (2015)](http://www.aclweb.org/anthology/S15-2097). It uses [PyJnius](https://github.com/kivy/pyjnius/tree/master/jnius) to call the Java modules to evaluate sentiment.

If you use *python-webis* for scientific research, please cite it in your publication: <br />
Fink, C. (2019): *python-webis: Python wrapper for the webis Twitter sentiment evaluation ensemble*. [doi:10.5281/zenodo.2547461](https://doi.org/10.5281/zenodo.2547461).


### Dependencies

The script is written in Python 3 and depends on the Python modules [PyJnius](https://github.com/kivy/pyjnius/tree/master/jnius), [pandas](https://pandas.pydata.org/) and [emojientities](https://gitlab.com/christoph.fink/python-emoji-range). 

On top of that, a Java Runtime Environment (jre) is required, plus a matching Java Development Kit (jdk). We used Java 8, but other versions might work just as well. [OpenJDK](https://openjdk.java.net/) works fine.

To install all dependencies on a Debian-based system, run:

```shell
apt-get update -y &&
apt-get install -y python3-dev python3-pip python3-virtualenv cython3 openjdk-8-jdk-headless openjdk-8-jre-headless ca-certificates-java
```

(There’s an Archlinux AUR package pulling in all dependencies, see further down)


### Installation

- *using `pip` or similar:*

```shell
pip3 install webis
```

- *OR: manually:*

    - Clone this repository

    ```shell
    git clone https://gitlab.com/christoph.fink/python-webis.git
    ```

    - Change to the cloned directory    
    - Use the Python `setuptools` to install the package:

    ```shell
    cd python-webis
    python3 ./setup.py install
    ```

- *OR: (Arch Linux only) from [AUR](https://aur.archlinux.org/packages/python-webis):*

```shell
# e.g. using yay
yay python-webis
```


### Usage

Import the `webis` module. On first run, *python-webis* will download and compile the Java backend – this might take a few minutes.

Then instantiate a `webis.SentimentIdentifier` object and use its `identifySentiment()` function, passing in a list of tuples (`[(tweetId, tweetText),(tweetId, tweetText), … ]`), a dict (`{tweetId: tweetText, … }`) or a `pandas.DataFrame` (first column is treated as identifier, second as tweetText). 

The function returns a list of tuples (`[(tweetId, sentiment), … ]`), a dict (`{tweetId: sentiment, … }`) or a data frame (first column id, second column sentiment) of rows it successfully identified a sentiment of. The type of the return value matches the argument, with which the function is called. The `tweetId` values will be cast to the type of the first row’s `tweetId`.

By default messages from the Java classes (written to `System.out` and `System.err`) are suppressed. To print all messages, pass a keyword argument `suppressJavaMessages=False` to the constructor of `webis.SentimentIdentifier` or the shorthand function `webis.identifySentiment` (see further down).

```python
import webis

sentimentIdentifier = webis.SentimentIdentifier()

# list of tuples
tweets = [
    (1, "What a beautiful morning! There’s nothing better than cycling to work on a sunny day 🚲."),
    (2, "Argh, I hate it when you find seven (7!) cars blocking the bike lane on a five-mile commute")
]

tweets = sentimentIdentifier.identifySentiment(tweets)
# [(1, "positive"), (2, "negative")]

# pandas Dataframe
import pandas
tweets = pandas.DataFrame([
    (1, "What a beautiful morning! There’s nothing better than cycling to work on a sunny day 🚲."),
    (2, "Argh, I hate it when you find seven (7!) cars blocking the bike lane on a five-mile commute")
])

tweets = sentimentIdentifier.identifySentiment(tweets)
#   sentiment tweetId
# 0  positive       1
# 1  negative       2

# dict
tweets = {
    1: "What a beautiful morning! There’s nothing better than cycling to work on a sunny day 🚲.",
    2: "Argh, I hate it when you find seven (7!) cars blocking the bike lane on a five-mile commute"
}

tweets = sentimentIdentifier.identifySentiment(tweets)
# { 1: "positive", 2: "negative" }

```

`python-webis` can act as a *context manager*:

```python
with webis.SentimentIdentifier() as s:
    tweets = s.identifySentiment(tweets)
```

`webis.identifySentiment()` is a short-hand for initialising a `SentimentIdentifier` object and calling its `identifySentiment()` method:

```python
tweets = webis.identifySentiment(tweets)
```
