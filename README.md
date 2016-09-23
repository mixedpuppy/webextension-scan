# Installation

1. Install node.js and python if you do not have them
2. Install web-ext [npm install --global web-ext]
   * or from https://github.com/mozilla/web-ext
3. clone this repository

# Usage

First you'll need access to your webextension addon, or an addon downloaded from the chrome store.

If you need to download from the chrome store, you can use http://chrome-extension-downloader.com/

1. unzip your addon into the empty addons directory in this repository
   * you may unzip more than one addon into the addons directory to scan a set of addons
2. run report.sh
3. run lint.sh

## updating schemas

The report generator uses schemas from the mozilla code base for each branch (nightly, aurora, beta, release).
I'll update them here occasionally,
but if you need an update, you can get the files from the mozilla-central repository by first 
cloning that then running update.sh.  mozilla-central should be a sibling of your clone of this repository.

hg clone https://hg.mozilla.org/mozilla-central

https://developer.mozilla.org/en-US/docs/Mozilla/Developer_guide/Source_Code/Mercurial

# report.sh output

report.sh produces a report of API usage in your addon.  It will contain a status for each release, rank and
description for each API call.  It also lists any bugs related to the API section.  The status columns are
titled N, A, B and R for nightly, aurora, beta and release.

### status

* blank means it is supported
* N means it is not implemented.  This may mean that it is scheduled to be implemented, or 
  that it will not be implemented in Firefox.
* D means the API is deprecated, it should be followed by a line describing the replacement API call

### rank

Rank is based on the number of times you use the API in your addon.  Lower the rank, the more you use it.

# lint.sh output

lint.sh is a shortcut script for running web-ext lint on your addon.  It will produce additional output 
describing other potential problems, such as syntax errors, or problems in the manifest file.

NOTE: web-ext output may not be up-to-date with the API status, however it is usefull for scanning the code and manifest.

# Example output

## report.sh

**NOTE**:  You can see in the example below, chrome.history.getVisits and chrome.runtime.reload are not avialable on release, but are in upcomming releases.

```
creating apiusage.csv...
generating report...
N A B R Rank API

======= chrome.app
N N N N   18 chrome.app.getDetails

======= chrome.browserAction
N N N N   46 chrome.browserAction.onClicked
          43 chrome.browserAction.setIcon
          42 chrome.browserAction.setPopup
          41 chrome.browserAction.setTitle
Bug      1207597: browserAction icon should match appearance of native Firefox toolbar buttons
Bug      1207692: provide a highlight state for browserActions
Bug      1244789: Support richer user interactions in the chrome.browserAction API

======= chrome.contextMenus
           3 chrome.contextMenus.create
N N N N   40 chrome.contextMenus.onClicked
          39 chrome.contextMenus.remove
          38 chrome.contextMenus.removeAll
Bug      1253418: Support browser_action and page_action contexts in browser.contextMenus API
Bug      1269062: [tracking] ContextMenus API support for Android WebExtensions
Bug      1280370: contextMenus do not support other protocols (ex. 'magnet:*', 'acestream:*', 'sop:*')

======= chrome.extension
          37 chrome.extension.getBackgroundPage
           1 chrome.extension.getURL
N N N N   36 chrome.extension.onMessage
N N N N   34 chrome.extension.onRequest
N N N N   15 chrome.extension.sendMessage
N N N N   33 chrome.extension.sendRequest
Bug      1213426: Complete the implementation of chrome.extension
Bug      1263900: Complete test coverage for browser.extension.inIncognitoContext

======= chrome.google
N N N N   32 chrome.google.com
N N N N   31 chrome.google.com\

======= chrome.history
      N  115 chrome.history.getVisits
          51 chrome.history.search

======= chrome.i18n
N N N N   14 chrome.i18n.
          29 chrome.i18n.getMessage

======= chrome.runtime
          13 chrome.runtime.getManifest
N N N N   12 chrome.runtime.id
N N N N    2 chrome.runtime.lastError
N N N N   28 chrome.runtime.onMessage
N N N N   26 chrome.runtime.onMessageExternal
    N N  132 chrome.runtime.reload
           6 chrome.runtime.sendMessage
Bug      1213473: Complete the implementation of chrome.runtime
Bug      1247435: Implement browser.runtime.onStartup
Bug      1252871: Implement chrome.runtime.onInstalled
Bug      1259944: runtime.sendMessage does not handle the three-argument form correctly.

======= chrome.tabs
          25 chrome.tabs.captureVisibleTab
          24 chrome.tabs.create
          11 chrome.tabs.executeScript
          10 chrome.tabs.insertCSS
N N N N   23 chrome.tabs.onActivated
N N N N    9 chrome.tabs.onRemoved
N N N N   22 chrome.tabs.onUpdated
           5 chrome.tabs.query
           8 chrome.tabs.remove
           7 chrome.tabs.sendMessage
D D D D   21 chrome.tabs.sendRequest Please use $(ref:runtime.sendMessage).
Bug      1190328: Test coverage for tabs extension API
Bug      1209869: tabs.sendMessage does not send messages to tab pages
Bug      1213477: Complete the implementation of chrome.tabs
Bug      1223254: Figure out when tabs API callbacks should fire, and make them fire at the right time
Bug      1238314: Implement browser.tabs opener functionality
Bug      1240631: Callback not called for chrome.tabs.move when tab is invalid
Bug      1260548: Basic tabs API support for Android WebExtensions
Bug      1260550: Support messaging interfaces in the tabs API on Android
Bug      1269456: Add permissions item to allow use of tabs.create/tabs.update

======= chrome.windows
          20 chrome.windows.create
N N N N   19 chrome.windows.onFocusChanged
Bug      1213484: Complete the implementation of chrome.windows
Bug      1253129: Support focused=false in the browser.windows.create
Bug      1261963: createData should be optional for browser.windows.create
Bug      1273146: WebExtensions: chrome.windows.create - callback parameter (window) does not have window.tabs property
Bug      1275275: New windows should not be animated to their final size/position
```

## lint.sh

NOTE: web-ext output may not be up-to-date with the API status, however it is usefull for scanning the code and manifest.

```
Validation Summary:

errors          0
notices         1
warnings        11

NOTICES:

Code                     Message                        Description                                                  File            Line   Column
MANIFEST_UNUSED_UPDATE   The "update_url" property is   The "update_url" is not used by Firefox in the root of a     manifest.json
                         not used by Firefox.           manifest; your add-on will be updated via the Add-ons site
                                                        and not your "update_url". See: https://mzl.la/25zqk4O
WARNINGS:

Code                    Message                         Description                                                  File                            Line   Column
MANIFEST_PERMISSIONS    /permissions: Unknown           See https://mzl.la/1R1n1t0 (MDN Docs) for more               manifest.json
                        permissions                     information.
                        "unlimitedStorage" at 0.
MANIFEST_CSP            "content_security_policy" is    A custom content_security_policy needs additional review.
                        defined in the manifest.json
EVAL_STRING_ARG         setTimeout or setInterval       setTimeout and setInterval functions should be called only   third_party/jquery-1.12.3.mi…   2      30510
                        must have function as 1st arg   with function expressions as their first argument            n.js
EVAL_STRING_ARG         setTimeout or setInterval       setTimeout and setInterval functions should be called only   third_party/jquery-1.12.3.mi…   4      8205
                        must have function as 1st arg   with function expressions as their first argument            n.js
TABS_SENDREQUEST        "tabs.sendRequest" is           This API has been deprecated by Chrome and has not been      js/common/Browser.js            2      940
                        deprecated or unimplemented     implemented by Firefox.
EXT_SENDREQUEST         "extension.sendRequest" is      This API has been deprecated by Chrome and has not been      js/common/Browser.js            2      1336
                        deprecated or unimplemented     implemented by Firefox.
EXT_ONREQUEST           "extension.onRequest" is        This API has been deprecated by Chrome and has not been      js/common/Browser.js            2      3181
                        deprecated or unimplemented     implemented by Firefox.
APP_GETDETAILS          "app.getDetails" is             This API has been deprecated by Chrome and has not been      js/main/VersionDetect.js        2      462
                        deprecated or unimplemented     implemented by Firefox.
APP_GETDETAILS          "app.getDetails" is             This API has been deprecated by Chrome and has not been      js/main/VersionDetect.js        2      488
                        deprecated or unimplemented     implemented by Firefox.
MOZINDEXEDDB_PROPERTY   mozIndexedDB used as an         mozIndexedDB has been removed; use indexedDB instead.        skitch/js/skitch.js             5      10601
                        object key/property
NO_DOCUMENT_WRITE       Use of document.write           document.write will fail in many circumstances when used     skitch/js/skitch.js             17     1952
                        strongly discouraged.           in extensions, and has potentially severe security
                                                        repercussions when used improperly. Therefore, it should
                                                        not be used.
```
