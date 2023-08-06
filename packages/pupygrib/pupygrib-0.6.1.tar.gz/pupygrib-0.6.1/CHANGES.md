# Change log

## 0.6.1

* Fix unpacking messages with an odd number of 12-bit values.
* Add official support for NumPy 1.19


## 0.6.0

* Add support for 24 bits per value packing (contributed by @uranix in !1).


## 0.5.1

* Fix edge cases in zero-padded GRIB files.
* Add official support for Python 3.8 and NumPy 1.18.


## 0.5.0

* Added support for grib files with zero-padded messages.


## 0.4.1

* Disabled universal wheel


## 0.4.0

* Dropped support for Python 3.5 and older.
* Added support for 12 bits per value packing.
* Moved the code repo to gitlab.com for CI facilities.


## 0.3.0

* Fixed a silent overflow error on unpacking simple grid data (PR #1)
* Formatted the code with the [black](https://black.readthedocs.io/en/stable/).


## 0.2.0

* Added a filename attribute to `Message` instances.
* Added official support for Python 3.6.
* Changed home page to repo at notabug.org.


## 0.1.0

* Initial release.
