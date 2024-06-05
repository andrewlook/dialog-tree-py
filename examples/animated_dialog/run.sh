#!/usr/bin/env bash

directory=$(dirname "$0")

python3 -m dialog_tree.runners.dialog_app "$directory/wikipedia.json" --sound_dir "$directory/data" --image_dir "$directory/data"
