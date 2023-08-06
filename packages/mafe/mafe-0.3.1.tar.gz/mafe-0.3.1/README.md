# Music Audio Feature Extractor

## Installation
```shell script
$ pip install mafe
```

## Typical usages
```shell script
# scan music tracks to extract raw set of features
$ mafe -t scanned.csv.bz2 scan -f [MUSIC_DIR]
# run normalization on extracted features
$ mafe -t scanned.csv.bz2 -o normalized.csv.bz2 normalize
# create table of distances between tracks
$ mafe -t normalized.csv.bz2 -o distances.csv.bz2 distance
# find clusters of similar tracks
$ mafe -t normalized.csv.bz2 -o clustered.csv.bz2 cluster -n 4
# run dimensionality reduction, keeping only the most distinctive features
$ mafe -t normalized.csv.bz2 -o reduced.csv.bz2 pca
# run clustering on distinct features, creating a visualization of the clusters
$ mafe -t reduced.csv.bz2 -o clustered_reduced.csv.bz2 cluster -n 4 -V -I cluster.png
```

## Command line options
```shell script
$ mafe --help
Usage: mafe [OPTIONS] COMMAND [ARGS]...

Options:
  -t, --tracks-csv TEXT  CSV file containing tracks  [required]
  -o, --output TEXT      CSV file containing distances between the tracks
                         [required]
  --help                 Show this message and exit.

Commands:
  cluster
  distance
  normalize
  pca
  scan
```
