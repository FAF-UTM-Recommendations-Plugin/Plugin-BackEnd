from bs4 import BeautifulSoup
import requests
from sentence_transformers import SentenceTransformer
import time

model_name = "all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)


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
            embedding = model.encode(edited_text).tolist()

            return {
                "url": url.rstrip('/'),  # Remove trailing slash to avoid duplicates
                "title": title,
                "text": edited_text,
                "embedding": embedding,
            }
        else:
            print("Could not find the article content.")
            return None
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return None



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

# Create the index if it doesn't exist
if not client.indices.exists(index=index_name):
    response = client.indices.create(index=index_name, body=index_body)
    print(f"Index '{index_name}' created:", response)
else:
    print(f"Index '{index_name}' already exists.")





def article_exists(client, index_name, url):
    """Checks if an article with the given URL already exists in the index."""
    query = {
        "query": {
            "term": {
                "url.keyword": url.rstrip('/')  # Match URL exactly
            }
        }
    }
    response = client.search(index=index_name, body=query)
    return response['hits']['total']['value'] > 0

# Initialize OpenSearch client
client = get_client()

# Date ranges for scraping articles
years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

article_data = []
for year in years:
    for month in months:
        url = f"https://www.zdg.md/{year}/{month}/?cat=4"
        article_links = get_articles(url)
        print(f"Year: {year}, Month: {month}, Articles found: {len(article_links)}")
        time.sleep(2)  # Avoid overwhelming the server

        for link in article_links:
            print(f"Processing: {link}")
            # Check if the article already exists
            if article_exists(client, index_name, link):
                print(f"Article already exists in the index: {link}")
                continue

            # Prepare and add the article if it doesn't exist
            article = prep_article(link)
            if article:
                res = client.index(
                    index=index_name,
                    body=article,
                    refresh=True
                )
                print(f"Indexed article: {link}")