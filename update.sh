#!/bin/sh
if [[ -d ../mozilla-central ]]; then
  cp -f ../mozilla-central/browser/components/extensions/schemas/*.json schemas/nightly/
  cp -f ../mozilla-central/toolkit/components/extensions/schemas/*.json schemas/nightly/
fi
if [[ -d ../mozilla-aurora ]]; then
  cp -f ../mozilla-aurora/browser/components/extensions/schemas/*.json schemas/aurora/
  cp -f ../mozilla-aurora/toolkit/components/extensions/schemas/*.json schemas/aurora/
fi
if [[ -d ../mozilla-beta ]]; then
  cp -f ../mozilla-beta/browser/components/extensions/schemas/*.json schemas/beta/
  cp -f ../mozilla-beta/toolkit/components/extensions/schemas/*.json schemas/beta/
fi
if [[ -d ../mozilla-release ]]; then
  cp -f ../mozilla-release/browser/components/extensions/schemas/*.json schemas/release/
  cp -f ../mozilla-release/toolkit/components/extensions/schemas/*.json schemas/release/
fi
