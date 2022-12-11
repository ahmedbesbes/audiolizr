#!/bin/bash
set -euxo pipefail

echo "Downloading spacy model"
python3 -m spacy download en_core_web_md