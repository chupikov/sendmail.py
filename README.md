# sendmail.py

**sendmail.py** is a sendmail-like application for testing purposes with pipelining messages processing for Linux developed in Python 3.

**sendmail.py** developed for usage in the Debian based Linux distributions.

Successfullty tested in the following OS:

1. [Xubuntu 14.04 LTS "Trusty Tahr"](http://xubuntu.org/news/14-04-release/).
2. [Elementary OS Freya](https://elementary.io/).

## Features

Application provides two applications:

1. **sendmail.py** - reads email messages from standard input and then process it according to your settings using one of available processors:
  1. **FilesystemProcessor** - saves messages to files in the specified directory.
  2. **NotifyProcessor** - displays desktop notifications when message sent. Does not works if sendmail.py used in the Apache2 environment; in this case **watch.py** need to be used.
  3. **SmtpProcessor** - sends messages using SMTP server.
2. **watch.py** - watches filesystems and displays desktop notifications whan new message file created.

## Dependencies

* python3-notify2
* python3-pyinotify

Installation:

```sh
sudo apt-get install \
  python3-notify2 \
  python3-pyinotify
```
