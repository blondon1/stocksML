from elasticsearch import Elasticsearch
from config import elasticsearch_host, elasticsearch_port, elasticsearch_index

def setup_elasticsearch():
    es = Elasticsearch(
        [{"host": elasticsearch_host, "port": elasticsearch_port}]
    )

    # Create the index if it doesn't exist
    if not es.indices.exists(index=elasticsearch_index):
        es.indices.create(index=elasticsearch_index)
    
    return es
