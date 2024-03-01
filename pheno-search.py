#!/usr/bin/env python3
import spacy

# Load the English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

# Process the natural language query
query = "Find records with Alzheimer disease, susceptibility to"
doc = nlp(query)

# Example logic to construct an Elasticsearch query (simplified)
entities = [ent.text for ent in doc.ents if ent.label_ in ['DISEASE', 'CONDITION']]
# Assuming 'DISEASE' and 'CONDITION' are custom or pre-defined labels you are interested in

# Construct the Elasticsearch query
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

