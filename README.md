# Pheno-Search
<p align="center">
    <em>Streamlined Searching in GA4GH-Standard Phenotypic and Clinical Data Repositories and Beyond</em>
</p>

[![Build and Test](https://github.com/mrueda/pheno-search/actions/workflows/build-and-test.yml/badge.svg)](https://github.com/mrueda/pheno-search/actions/workflows/build-and-test.yml)
[![Coverage Status](https://coveralls.io/repos/github/CNAG-Biomedical-Informatics/pheno-search/badge.svg?branch=main)](https://coveralls.io/github/CNAG-Biomedical-Informatics/pheno-search?branch=main)
![version](https://img.shields.io/badge/version-0.04_beta-orange)
[![Docker Build](https://github.com/mrueda/pheno-search/actions/workflows/docker-build.yml/badge.svg)](https://github.com/mrueda/pheno-search/actions/workflows/docker-build.yml)
[![Docker Pulls](https://badgen.net/docker/pulls/manuelrueda/pheno-search?icon=docker&label=pulls)](https://hub.docker.com/r/manuelrueda/pheno-search/)
[![Docker Image Size](https://badgen.net/docker/size/manuelrueda/pheno-search?icon=docker&label=image%20size)](https://hub.docker.com/r/manuelrueda/pheno-search/)
[![Documentation Status](https://github.com/mrueda/pheno-search/actions/workflows/documentation.yml/badge.svg)](https://github.com/mrueda/pheno-search/actions/workflows/documentation.yml)
[![License: Artistic-2.0](https://img.shields.io/badge/License-Artistic%202.0-0298c3.svg)](https://opensource.org/licenses/Artistic-2.0)

**Documentation**: <a href="https://mrueda.github.io/pheno-search" target="_blank">https://mrueda.github.io/pheno-search</a>

**Docker Hub Image**: <a href="https://hub.docker.com/r/manuelrueda/pheno-search/tags" target="_blank">https://hub.docker.com/r/manuelrueda/pheno-search/tags</a>


# Download and Installation

## Installing Elasticsearch

ElasticSearch [LICENSE](https://www.elastic.co/pricing/faq/licensing). 

### From Docker Image:

To pull the Docker image, use the following command:

```bash
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.10.0
```

### Running the Image

To run the image, execute:

```bash 
docker run -d --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.10.0
```

## Installing jq

To install jq, run:

```bash
sudo apt-get install jq
```

# Data Ingestion

Suppose you have a file named `individuals.json` containing 100 entries. First, you'll need to process it to make it compatible with the Elasticsearch API:

```bash
jq -c '.[] | {"index": {"_index": "dataset1"}}, .' individuals.json > dataset1.json
```

This command flattens the data, potentially losing its nested structure. If maintaining nestedness is crucial, you'll need to use a `mapping.json` file to inform Elasticsearch of the data's structure.

### Deleting the Old Index

First, delete the old index:

```bash
curl -X DELETE "http://localhost:9200/dataset1"
```

### Sending the Right Parameters

Then, create the index with the correct structure:

```bash
curl -X PUT "http://localhost:9200/dataset1_nested" -H 'Content-Type: application/json' -d'@mapping.json'
```

# Data Query

To query for "Alzheimer disease, susceptibility to", use `curl`:

```bash
curl -X GET "http://localhost:9200/dataset1/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "nested": {
      "path": "diseases",
      "query": {
        "bool": {
          "must": [
            { "match": { "diseases.diseaseCode.label": "Alzheimer disease, susceptibility to" }}
          ]
        }
      }
    }
  }
}
```

# Pheno-Search

To install the required modules, run:

```bash
pip install -r requirements.txt
```

To execute the code, run:

```bash
python3 pheno-search.py
```

