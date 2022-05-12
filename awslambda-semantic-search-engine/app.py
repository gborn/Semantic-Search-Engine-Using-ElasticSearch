import json
import boto3
import os
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth


model = tf.keras.Sequential([hub.KerasLayer("model/")])

def get_client():
    """
    Returns OpenSearch client
    """
    host = os.environ.get('ES_HOST')
    region = os.environ.get('AWS_REGION')

    credentials = boto3.Session().get_credentials()
    auth = AWSV4SignerAuth(credentials, region)
    client = OpenSearch(
        hosts = [{'host': host, 'port': 443}],
        http_auth = auth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )
    return client


def lambda_handler(event, context):
    """
    Lambda Handler to accept query and return results from elastic search
    """
    query = event['PathParameters']['query']

    client = get_client()
    query_vector = tf.make_ndarray(tf.make_tensor_proto(model([query]))).tolist()[0]

    b = {
    "size": 10,
    "query": {
        "knn": {
        "question_vector": {
            "vector": query_vector,
            "k": 10
                }
            }
        }
    }

    response = client.search(index='stackoverflow', doc_type='_doc', body=b)
    results = response['hits']['hits']

    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }