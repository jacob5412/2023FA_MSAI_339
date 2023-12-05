# Locally Hosted OSRM

Source: [OSRM through Docker](https://afi.io/blog/introduction-to-osrm-setting-up-osrm-backend-using-docker/)

Create a folder called `/osrm-backend-nyc` and `cd` into it.

1. Download Open Street Map data for NYC 2016
```zsh
wget https://download.geofabrik.de/north-america/us/new-york-160101.osm.pbf
```

2. Spin up the osrm-backend image via Docker
```zsh
docker run -t -v "${PWD}:/data" ghcr.io/project-osrm/osrm-backend osrm-extract -p /opt/car.lua /data/new-york-160101.osm.pbf || echo "osrm-extract failed"
```

3. Partition the graph
```zsh
docker run -t -v "${PWD}:/data" ghcr.io/project-osrm/osrm-backend osrm-partition /data/new-york-160101.osrm || echo "osrm-partition failed"
```

4. Contract the graph
```zsh
docker run -t -v "${PWD}:/data" ghcr.io/project-osrm/osrm-backend osrm-customize /data/new-york-160101.osrm || echo "osrm-customize failed"
```

6. Host the instance
```zsh
docker run -t -i -p 5000:5000 -v "${PWD}:/data" ghcr.io/project-osrm/osrm-backend osrm-routed --algorithm mld /data/new-york-160101.osrm
```

7. Sample CURL
```zsh
curl "http://127.0.0.1:5000/route/v1/driving/-73.7902603149414,40.643604278564446;-73.97309112548828,40.65372085571289?overview=false"
```
The output will be the driving distance within NYC.
