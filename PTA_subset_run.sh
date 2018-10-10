#!/bin/bash

band_index=0
lat=74
lon=94

python PTA_Subset.py << EOF
$band_index
$lat
$lon
EOF
