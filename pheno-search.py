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
entities = [ent.text for ent in doc.ents if ent.label_ in ['DISEASE', 'CONDITION']]

# Simply queries
query = {
    "query": {
        "term": {
            "sex.id": {
                "value": "NCIT:C20197"  # Adjust this value as needed
            }
        }
    }
}

_query = {
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

# Example logic to construct an Elasticsearch query with fuzzy search
fs_query = {
    "query": {
        "nested": {
            "path": "diseases",  # Specify the path to the nested object
            "query": {
                "match": {
                    "diseases.diseaseCode.label": {
                        "query": "Alzheimer disease",  # The search text
                        "fuzziness": 2,  # Allow for some fuzziness in the match
                        "prefix_length": 1,
                        "max_expansions": 100
                    }
                }
            },
            "score_mode": "avg"  # How to score matches for multiple nested objects
        }
    }
}

# Perform the search with the correctly constructed query
response = es.search(index="dataset1", body=query)
#response = es.search(index="dataset1", body=es_query)
#response = es.search(index="dataset1", body=fs_query)

# Pretty print the response
print(json.dumps(response, indent=2))

# Extract 'id' from each hit
#ids = [hit['_id'] for hit in response['hits']['hits']]
#print(ids)
