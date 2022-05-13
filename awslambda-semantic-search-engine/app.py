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
        connection_class = RequestsHttpConnection,
        timeout=60,
        max_retries=10,
        retry_on_timeout=True
    )
    return client


def lambda_handler(event, context):
    """
    Lambda Handler to accept query and return results from elastic search
    """
    # query to search
    query = event['queryStringParameters']['query']

    # Number of neighbors
    k = event['queryStringParameters']['k']

    # Number of search results
    n = event['queryStringParameters']['n']

    print('Recieved query', query, 'K', k, 'n', n)

    client = get_client()
    query_vector = tf.make_ndarray(tf.make_tensor_proto(model([query]))).tolist()[0]

    b = {
    "size": n,
    "query": {
        "knn": {
        "question_vector": {
            "vector": query_vector,
            "k": k
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