import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from opensearchpy import OpenSearch, helpers

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

model_name = "all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)

EMBEDDING_DIM = model.encode(["Sample sentence"])[0].shape[0]

index_name = "articles"

index_body = {
  "settings": {
    "index": {
      "knn": True,
      "knn.algo_param.ef_search": 100
    }
  },
  "mappings": { #how do we store, 
    "properties": {
        "embedding": {
          "type": "knn_vector", #we are going to put 
          "dimension": EMBEDDING_DIM,
          "method": {
            "name": "hnsw",
            "space_type": "l2",
            "engine": "nmslib",
            "parameters": {
              "ef_construction": 128,
              "m": 24
            }
         }
     }
    }
}
}

response = client.indices.create(index=index_name, body=index_body)


def get_articles(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article_links = soup.find_all('a', href=True, class_='list-item__link-image') 
        return [link['href'] for link in article_links]
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return []

def prep_article(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article = soup.find('div', class_='single-post__content wpb_text_column')  
        title = soup.find('span', class_='inner-title').get_text(strip=True)

        if article:
            text = article.get_text(strip=True, separator="\n")
            edited_text = text.replace(",", "").replace(".", "").replace("\n", "")
            embedding = model.encode([edited_text]).tolist()

            return {
                "_index": index_name,
                "_source": {
                    "url": url.rstrip('/'),  # Remove trailing slash to avoid duplicate issues
                    "title": title,
                    "text": edited_text,
                    "embedding": embedding,
                },
            }
        else:
            print("Could not find the article content.")
            return None
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return None

if __name__ == "__main__":
    # URL of the page listing articles
    url = "https://www.zdg.md/stiri/"
    article_links = get_articles(url)
    article_data = []

    for link in article_links:
        print(f"Processing: {link}")
        article = prep_article(link)
        article_data.append(article)

    if article_data:
        print(f"Indexing {len(article_data)} articles into OpenSearch...")
        helpers.bulk(client, article_data, index=index_name, raise_on_error=True, refresh=True)
    else:
        print("No new articles to index.")


'''if not client.indices.exists(index=index_name):
    response = client.indices.create(index=index_name, body=mapping)
    print(f"Index '{index_name}' created:", response)
else:
    print(f"Index '{index_name}' already exists.")

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_articles(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article_links = soup.find_all('a', href=True, class_='list-item__link-image') 
        return [link['href'] for link in article_links]
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return []

def prep_article(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article = soup.find('div', class_='single-post__content wpb_text_column')  
        title = soup.find('span', class_='inner-title').get_text(strip=True)

        if article:
            text = article.get_text(strip=True, separator="\n")
            edited_text = text.replace(",", "").replace(".", "").replace("\n", "")
            embedding = model.encode([edited_text]).tolist()

            return {
                "_index": index_name,
                "_source": {
                    "url": url.rstrip('/'),  # Remove trailing slash to avoid duplicate issues
                    "title": title,
                    "text": edited_text,
                    "embedding": embedding,
                },
            }
        else:
            print("Could not find the article content.")
            return None
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return None

if __name__ == "__main__":
    # URL of the page listing articles
    url = "https://www.zdg.md/stiri/"
    article_links = get_articles(url)
    article_data = []

    for link in article_links:
        print(f"Processing: {link}")
        article = prep_article(link)

        if article:
            # Check if the article already exists in the index
            query = {
                "query": {
                    "term": {
                        "url.keyword": article["_source"]["url"]
                    }
                }
            }
            existing = client.search(index=index_name, body=query)
            if existing['hits']['total']['value'] == 0:
                article_data.append(article)

    if article_data:
        print(f"Indexing {len(article_data)} articles into OpenSearch...")
        helpers.bulk(client, article_data, raise_on_error=True, refresh=True)
    else:
        print("No new articles to index.")


# Count the number of documents in the index
response = client.count(index=index_name)
print(f"Total number of articles: {response['count']}")'''