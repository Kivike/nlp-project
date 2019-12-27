#!/bin/zsh

# Wrapper for gdal package running in Docker container
# 
# Example usage:
# cd <directory-on-host-with-shp-files>
# sh ../<path-to-this-script>/ogr2ogr.sh -f GeoJSON -t_srs crs:84 [name].geojson [name].shp
# 
# Actual example:
# sh ../../geoutils/ogr2ogr.sh -f GeoJSON -t_srs crs:84 PostalSector.geojson PostalSector.shp
# 
# Any arguments being passed to the script will be passed to the ogr2ogr tool on the container.
# Use --help command for help (or --long-usage for full help)

HOST_DIR=$(pwd)         # Current directory on the host
CONTAINER_DIR=/var/tmp  # Working dir on the container

# Bind volume from host to container, set working directory and remove container afterwards
docker run \
    -v $HOST_DIR:$CONTAINER_DIR \
    -w="$CONTAINER_DIR" \
    --rm \
    osgeo/gdal:alpine-small-latest ogr2ogr "$@"
