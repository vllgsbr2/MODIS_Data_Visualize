#!/bin/bash

band_index=0
lat=43.6532
lon=-79.3832

python PTA_Subset.py << EOF
$band_index
$lat
$lon
EOF
