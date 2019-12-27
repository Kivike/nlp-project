# Examples

This directory contains examples of the JSON schema on the data sourced from [University of Edinburgh](https://datashare.is.ed.ac.uk/handle/10283/2597). Each of the files represents a **feature** object in GeoJSON files that are parsed from the shapefile data. Below is an example of a whole GeoJSON file without any features.

```json
{
    "type": "FeatureCollection",
    "name": "PostalArea",
    "features": []
}
```

## Details

The data is containing shapes for post code areas in UK. The areas are divided on three different levels.

### Area

Area is the highest abstraction of the post code area (called _post code area_), and it consists of internal districts.

Example area code in London: **E** for _East_

### District

District is the medium-level abstraction of post code area (called _post code district_). Each post code area contains arbitrary number of districts, that can be further divided into sectors.

Example district in London: **E1** for _East 1_

### Sector

Sectors are the smallest areas that post codes can define. Each district contains arbitrary number of sectors.

Example sector in London: **E1 0** for _East 1 sector 0_

## Copyright notice

The data is released under [OGL licence](http://geolytix.co.uk/geodata/postal-boundaries/postal-licence).

The data can be used without a charge given that the following is attributed:

```
Postal Boundaries © GeoLytix copyright and database right 2012 Contains Ordnance Survey data © Crown copyright and database right 2012 Contains Royal Mail data © Royal Mail copyright and database right 2012 Contains National Statistics data © Crown copyright and database right 2012. GIS vector data. This dataset was first accessioned in the EDINA ShareGeo Open repository on 2014-03-14 and migrated to Edinburgh DataShare on 2017-02-22
```
