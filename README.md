# Scanning your Webextension

This scanner is most useful for those considering porting an existing Chrome extension to Firefox.  If you are starting a new Webextension, [web-ext] and the [documentation on MDN] is probably enough to get you started.  If you are porting an extension, you can run these scripts against your addon to get an idea of what areas you may run into issues or incompatibilities.  With this information you can evaluate if there are workarounds, or if you can remove some functionality to get your extension working on Firefox.  If there is some core functionality that you cannot port due to missing APIs, you may also consider using [hybrid extensions] to backfill some functionality using legacy bootstrap addons for Firefox, while still sharing much of your code between browsers.  You can also view http://arewewebextensionsyet.com for links to specific APIs.

# Installation

1. Install node.js and python if you do not have them
2. Install [web-ext] using `npm install --global web-ext`
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

The report generator uses schemas from the mozilla code base.  I'll update them here occassionaly, 
but if you need an update, you can get the files from the mozilla-central repository by first 
cloning that then running update.sh.  mozilla-central should be a sibling of your clone of this repository.

hg clone https://hg.mozilla.org/mozilla-central

https://developer.mozilla.org/en-US/docs/Mozilla/Developer_guide/Source_Code/Mercurial

**NOTE:** report.sh will report against the version of Firefox that the schema files are pulled from.  If you want to test against an older version of Firefox you should pull from that repository.  The schema files in this repository are from Firefox Nightly.

# report.sh output

report.sh produces a report of API usage in your addon.  It will contain a status, rank and 
description for each API call.  It also lists any bugs related to the API section.

### status

* blank means it is supported
* NO means it is not implemented.  This may mean that it is scheduled to be implemented, or 
  that it will not be implemented in Firefox.
* DEP means the API is deprecated, it should be followed by a line describing the replacement API call

### rank

Rank is based on the number of times you use the API in your addon.  Lower the rank, the more you use it.

# lint.sh output

lint.sh is a shortcut script for running [web-ext] lint on your addon.  It will produce additional output 
describing other potential problems, such as syntax errors, or problems in the manifest file.

**NOTE:** [web-ext] output may not be up-to-date with the API status, however it is usefull for scanning the code and manifest.

# Example output

## report.sh

```
creating apiusage.csv...
generating report...
Skipping: ./schemas/context_menus_internal.json
OK Rank API

======= chrome.app
NO    18 chrome.app.getDetails

======= chrome.browserAction
      41 chrome.browserAction.setTitle
      42 chrome.browserAction.setPopup
      43 chrome.browserAction.setIcon
      46 chrome.browserAction.onClicked
Bug      1207597: browserAction icon should match appearance of native Firefox toolbar buttons
Bug      1207692: provide a highlight state for browserActions
Bug      1244789: Support richer user interactions in the chrome.browserAction API

======= chrome.contextMenus
      38 chrome.contextMenus.removeAll
       3 chrome.contextMenus.create
      39 chrome.contextMenus.remove
      40 chrome.contextMenus.onClicked
Bug      1253418: Support browser_action and page_action contexts in browser.contextMenus API
Bug      1269062: [tracking] ContextMenus API support for Android WebExtensions
Bug      1280370: contextMenus do not support other protocols (ex. 'magnet:*', 'acestream:*', 'sop:*')

======= chrome.extension
      37 chrome.extension.getBackgroundPage
       1 chrome.extension.getURL
DEP   34 chrome.extension.onRequest
         Please use $(ref:runtime.onMessage).
NO    36 chrome.extension.onMessage
NO    15 chrome.extension.sendMessage
NO    33 chrome.extension.sendRequest
Bug      1213426: Complete the implementation of chrome.extension
Bug      1263900: Complete test coverage for browser.extension.inIncognitoContext

======= chrome.google
NO    32 chrome.google.com
NO    31 chrome.google.com\

======= chrome.i18n
      29 chrome.i18n.getMessage
NO    14 chrome.i18n.

======= chrome.runtime
      13 chrome.runtime.getManifest
       6 chrome.runtime.sendMessage
NO    26 chrome.runtime.onMessageExternal
      28 chrome.runtime.onMessage
NO    12 chrome.runtime.id
NO     2 chrome.runtime.lastError
Bug      1213473: Complete the implementation of chrome.runtime
Bug      1247435: Implement browser.runtime.onStartup
Bug      1252871: Implement chrome.runtime.onInstalled
Bug      1259944: runtime.sendMessage does not handle the three-argument form correctly.

======= chrome.tabs
      11 chrome.tabs.executeScript
       5 chrome.tabs.query
DEP   21 chrome.tabs.sendRequest
         Please use $(ref:runtime.sendMessage).
      24 chrome.tabs.create
      10 chrome.tabs.insertCSS
       8 chrome.tabs.remove
      25 chrome.tabs.captureVisibleTab
       7 chrome.tabs.sendMessage
      22 chrome.tabs.onUpdated
       9 chrome.tabs.onRemoved
      23 chrome.tabs.onActivated
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
      19 chrome.windows.onFocusChanged
Bug      1213484: Complete the implementation of chrome.windows
Bug      1253129: Support focused=false in the browser.windows.create
Bug      1261963: createData should be optional for browser.windows.create
Bug      1273146: WebExtensions: chrome.windows.create - callback parameter (window) does not have window.tabs property
Bug      1275275: New windows should not be animated to their final size/position

```

## lint.sh

**NOTE:** web-ext output may not be up-to-date with the API status, however it is usefull for scanning the code and manifest.

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

[web-ext]: https://github.com/mozilla/web-ext
[documentation on MDN]: https://developer.mozilla.org/en-US/Add-ons/WebExtensions
[hybrid extensions]: https://github.com/rpl/webextensions-examples/tree/examples/hybrid-addons/embedded-webextension-bootstrapped
