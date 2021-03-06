# OnionShare Changelog

## 1.1

* OnionShare connects to Tor itself now, so opening Tor Browser in the background isn't required
* In Windows and macOS, OnionShare alerts users about updates
* Removed the menu bar, and adding a Settings button
* Added desktop notifications

## 1.0

* Fixed long-standing macOS X bug that caused OnionShare to crash on older Macs (!)
* Added settings dialog to configure connecting to Tor, including support for system Tor
* Added support for stealth onion services (advanced option)
* Added support for Whonix
* Improved AppArmor profiles
* Added progress bar for zipping up files
* Improved the look of download progress bars
* Allows developers to launch OnionShare from source tree, without building a package
* Deleted legacy code, and made OnionShare purely use ephemeral Tor onion services
* Switched to EFF's diceware wordlist for slugs

## 0.9.2 (Linux only)

* Looks for `TOR_CONTROL_PORT` environment variable, to help Tails integration
* Change how OnionShare checks to see if it's installed system-wide, to help Subgraph OS integration

## 0.9.1

* Added Nautilus extension, so you can right-click on a file and choose "Share via OnionShare", thanks to Subgraph developers
* Switch to using the term "onion service" rather than "hidden service"
* Fix CVE-2016-5026, minor security issue related to use of /tmp directory
* Switch from PyInstaller to cx_Freeze for Windows and OSX packaging
* Support CLI in Windows and OSX

## 0.9

* Slugs are now shorter and human-readable, with rate limiting to prevent URL guessing
* Uses a new slug each time the server restarts
* "Stop sharing automatically" enforces only one download
* Users get asked if they're sure they want to close OnionShare while server is running
* Added estimated time remaining progress indicator
* Fixed frozen window while waiting for hidden service to start
* Displays version number in both GUI and CLI
* Closing window causes downloads to stop immediately
* Web server listens in ports 17600-17650, for future Tails support
* Updated translations
* Ported from Python 2 to Python 3 and from Qt4 to Qt5
* Ported from py2app and py2exe to PyInstaller

## 0.8.1

* Fixed crash in Windows 7
* Fixed crash related to non-ephemeral hidden services in Linux
* Fixed minor bugs

## 0.8

* Add support for ephemeral hidden services
* Stopped leaking sender's locale on download page
* Add support for Tor Messenger as provider of Tor service
* Minor bugfixes, code cleanup, and refactoring

## 0.7.1

* Fixed critical bug in OS X binaries that caused crashes on some computers
* Added Security Design document
* Minor bug fix with Windows code signing timestamp server
* Linux version uses HS dir that is allowed by Tor Browser Launcher's AppArmor profiles

## 0.7

* Added code signing for Mac OS X
* Does not disable existing hidden services
* Uses allowZip64 to allow compressing files >5gb
* Sets HS dir to be in /var/lib/tor in Tails, to obey AppArmor rules
* Misc. minor code cleanup

## 0.6

* Brand new drag-and-drop GUI with ability to start and stop server
* Much cleaner code split into several files
* Support for sharing multiple files and folders at once, and automatically zips files before sharing
* Redesigned receiver HTML interface
* Waits for hidden service to be available before displaying URL
* Cleans up hidden service directory on exit
* Continuous integration with Travis
* Support for multiple downloads at once
* Fixed unicode-related filename and display bugs
* Warns that large files could take hours to send
* New translations
* Several misc. bugfixes
* Added code signing for Windows with Authenticode

## 0.5

* Removed webkit GUI altogether, and refactored GUI with native Qt widget
* In Tails, launches separate process as root for Tor control port and firewall stuff, everything else runs as amnesia
* Fixed itsdangerous dependency bug in Debian Wheezy and Tails
* Guesses content type of file, responds in HTTP header

## 0.4

* Fixed critical XSS bug that could deanonymize user: https://micahflee.com/2014/07/security-advisory-upgrade-to-onionshare-0-4-immediately/
* Added CSP headers in GUI to prevent any future XSS bugs from working
* Hash urandom data before using it, to avoid leaking state of entropy
* Constant time compare the slug to avoid timing attacks
* Cleaned up Tails firewall code

## 0.3

* Built a simple, featureful cross-platform GUI
* Graphical installers for Windows and OSX
* Packaged for Linux in .deb, .rpm, with desktop launcher
* Installable in Tails 1.1+, with simple "install" script
* Automatically copies URL to clipboard
* Automatically closes when download is done by default
* Shows download progress
* Limited suite of tests
* If a localized string doesn't exist, falls back to English
* New translations: Dutch, Portuguese, German, Russian, and updated translations: Norwegian, Spanish, French, Italian
