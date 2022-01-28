#!/usr/bin/env bash
set -e
set -v
python3 src/CSE447_proj.py test --work_dir work --test_data $1 --test_output $2
