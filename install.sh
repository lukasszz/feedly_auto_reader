#!/usr/bin/env bash
git submodule update --init FeedlyClient/
cp config_sample.ini config.ini
echo "Edit config.ini and provide necessary parametres"