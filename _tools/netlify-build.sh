#!/usr/bin/env bash
# Netlify-build: zet alleen de gegenereerde HTML in dist/ (geen generator, scripts of notities online).
# De HTML staat al in de repo (python _generator/build.py lokaal draaien vóór je pusht),
# dus Netlify hoeft geen Python te draaien.
set -euo pipefail
cd "$(dirname "$0")/.."

rm -rf dist
mkdir -p dist
cp curelytics-gids.html index.html dist/
cp -r 00-Algemeen 01-BI-Specialist 02-Data-Engineer 03-Data-Analist dist/

echo "dist/: $(find dist -name '*.html' | wc -l | tr -d ' ') HTML-bestanden"
