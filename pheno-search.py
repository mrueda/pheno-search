#!/usr/bin/env python3
import spacy
from elasticsearch import Elasticsearch
import json

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Load the English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

# Process the natural language query
query_text = "Alzheimer disease, susceptibility to"
doc = nlp(query_text)

# Example logic to construct an Elasticsearch query (simplified)
entities = [ent.text for ent in doc.ents if ent.label_ in ['DISEASE', 'CONDITION']]
# Assuming 'DISEASE' and 'CONDITION' are custom or pre-defined labels you are interested in

# Simply query
query = {
   "_source": ["id"],  # Specify the fields to include in the response
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

# Correctly construct the Elasticsearch query based on identified entities
es_query = {
    "query": {
        "nested": {
            "path": "diseases",
            "query": {
                "bool": {
                    "must": [
                        {"match": {"diseases.diseaseCode.label": " ".join(entities)}}
                    ]
                }
            }
        }
    }
}

# Perform the search with the correctly constructed query
response = es.search(index="dataset1", body=query)
#response = es.search(index="dataset1", body=es_query)

# Pretty print the response
print(json.dumps(response, indent=2))

# Extract 'id' from each hit
ids = [hit['_id'] for hit in response['hits']['hits']]

print(ids)
