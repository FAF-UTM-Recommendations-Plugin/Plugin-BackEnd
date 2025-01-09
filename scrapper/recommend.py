from opensearchpy import OpenSearch

CLUSTER_URL = 'https://localhost:9200'

def get_client(cluster_url = CLUSTER_URL,
                  username='admin',
                  password='admin'):

    client = OpenSearch(
        hosts=[cluster_url],
        http_auth=(username, password),
        verify_certs=False
    )
    return client

client = get_client()

from sentence_transformers import SentenceTransformer

model_name = "all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)

EMBEDDING_DIM = model.encode(["Sample sentence"])[0].shape[0]


index_name = "articles"


""" Example query text """
user_query = "Război in Ucraina"

""" Embedding the query by using the same model """
query_embedding = model.encode((user_query))


query_body = {
    "query": {"knn": {"embedding": {"vector": query_embedding, "k": 3}}},
    "_source": False,
    "fields": ["url", "title", "text"],
}

results = client.search(
    body=query_body,
    index=index_name
)

for i, result in enumerate(results["hits"]["hits"]):
    url = result['fields']['url'][0]
    title = result['fields']['title'][0]
    score = result['_score']
    print(f"{i+1}. Title: {title}, Score: {score}, URL: {url}")