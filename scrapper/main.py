import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import time
from opensearchpy import OpenSearch

# Connect to OpenSearch
client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    http_auth=("admin", "admin"), 
)

# Index name
index_name = "news"

# Create the index with mappings if it doesn't exist
if not client.indices.exists(index=index_name):
    mapping = {
        "mappings": {
            "properties": {
                "url": {"type": "keyword"},
                "title": {"type": "text"},
                "text": {"type": "text"},
                "embedding": {"type": "dense_vector", "dims": 384},  # Adjust "dims" based on your model
            }
        }
    }
    client.indices.create(index=index_name, body=mapping)
    print(f"Index '{index_name}' created.")

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_articles(url):
    # Send a GET request to the webpage
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article_links = soup.find_all('a', href=True, class_='list-item__link-image')  # Adjust class as needed
        links = [link['href'] for link in article_links]
        return links
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")

def prep_article(url):
    # Send a GET request to the webpage
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article = soup.find('div', class_='single-post__content wpb_text_column')  # Adjust class name as needed
        title = soup.find('span', class_='inner-title').get_text(strip=True)

        if article:
            text = article.get_text(strip=True, separator="\n")
            edited_text = text.replace(",", "").replace(".", "").replace("\n", "")
            embedding = model.encode([edited_text]).tolist()

            return {
                "url": url,
                "title": title,
                "text": edited_text,
                "embedding": embedding,
            }
        else:
            print("Could not find the article content.")
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")

def article_exists(url):
    # Check if the article with the given URL already exists
    query = {"query": {"term": {"url": url}}}
    response = client.search(index=index_name, body=query)
    return response["hits"]["total"]["value"] > 0

def index_article(article):
    # Index the article into OpenSearch
    client.index(index=index_name, body=article)
    print(f"Indexed article: {article['title']}")

if __name__ == "__main__":
    # URL of the news listing page
    url = "https://www.zdg.md/stiri/"
    articles = get_articles(url)

    for link in articles:
        print(f"Processing: {link}")
        if not article_exists(link):
            prepped_article = prep_article(link)
            if prepped_article:
                index_article(prepped_article)
            else:
                print(f"Failed to process article: {link}")
        else:
            print(f"Article already exists: {link}")

        time.sleep(2)  # Sleep to avoid overwhelming the server
