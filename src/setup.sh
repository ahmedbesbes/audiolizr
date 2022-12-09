#!/bin/bash
set -euxo pipefail

echo "Downloading spacy model"
python -m spacy download en_core_web_md