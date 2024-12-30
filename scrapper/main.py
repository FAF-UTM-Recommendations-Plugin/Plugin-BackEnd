
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import json
import time
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_articles(url):

    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all links to articles (adjust the selector based on the structure of the website)
        article_links = soup.find_all('a', href=True, class_='list-item__link-image') 
        
        # Extract the href attributes and store them in a list
        links = [link['href'] for link in article_links]
        
        return links

        # Print the extracted links
        #print("Article Links:")
        #for i, link in enumerate(links, start=1):
            #print(f"{i}: {link}")

    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")


def prep_article(url):
    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the article content (this selector depends on the website's structure)
        article = soup.find('div', class_='single-post__content wpb_text_column')  # Update the class name as needed

        # Find title of the article
        title = soup.find('span', class_='inner-title').get_text(strip=True)

        #print(article)
        # Extract text from the article
        if article:
            text = article.get_text(strip=True, separator="\n")
            # Remove commas, dots, and newline characters
            edited_text = text.replace(",", "").replace(".", "").replace("\n", "")
            
            # Embedding the article text
            embedding = model.encode([edited_text]).tolist()

            return {
                "url": url,
                "title": title,
                "text": edited_text,
                "embedding": embedding
            }
            
            #print("Edited Article Text:")
            #print(edited_text)
        else:
            print("Could not find the article content.")
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")


if __name__ == "__main__":
    # URL of the news listing page
    url = "https://www.zdg.md/stiri/"
    articles = get_articles(url)

    for link in articles:
        
        print(link)
        prepped_article = prep_article(link)

        # Index the article in Elasticsearch
        #es.index(index="news", body=prepped_article)

        
        time.sleep(2)  # Sleep for 2 seconds to avoid overwhelming the server
        
