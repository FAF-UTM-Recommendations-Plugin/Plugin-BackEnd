from opensearchpy import OpenSearch
from sentence_transformers import SentenceTransformer

# Initialize OpenSearch client
client = OpenSearch(
    hosts=["https://admin:admin@localhost:9200/"],
    http_compress=True,
    use_ssl=True,
    verify_certs=False,  # DONT USE IN PRODUCTION
    ssl_assert_hostname=False,
    ssl_show_warn=False
)

# Initialize the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def search_similar_articles(index_name, article_text, top_k=10):
    """
    Search for the top_k most similar articles to the given article_text.
    
    Args:
        index_name (str): The name of the OpenSearch index.
        article_text (str): The text of the new article.
        top_k (int): The number of similar articles to retrieve.
    
    Returns:
        list: A list of the most similar articles.
    """
    # Compute the embedding for the new article
    embedding = model.encode(article_text).tolist()
    
    # Define the OpenSearch query for dense vector similarity
    query = {
        "size": top_k,
        "query": {
            "knn": {
                "embedding": {
                    "vector": embedding,
                    "k": top_k
                }
            }
        }
    }
    
    # Execute the search query
    response = client.search(index=index_name, body=query)
    
    # Extract and return the results
    similar_articles = []
    for hit in response['hits']['hits']:
        similar_articles.append({
            "title": hit["_source"]["title"],
            "url": hit["_source"]["url"],
            "score": hit["_score"]
        })
    
    return similar_articles

if __name__ == "__main__":
    # Specify the index name
    index_name = "articles"
    
    # Example article text
    new_article_text = '''

    Președintele demis al Siriei, Bashar al-Assad, a declarat că a rămas în Damasc până în dimineața zilei de 8 decembrie și a părăsit țara abia în seara acelei zile. Acest lucru este raportat de TASS, potrivit BBC. O înregistrare în acest sens a apărut pe contul biroului lui Assad în rețelele sociale.

Assad susține că „în niciun moment în timpul evenimentelor din Siria” nu s-a gândit să demisioneze și să fugă din țară.

Săptămâna trecută, Reuters a scris că acesta nu și-a avertizat susținătorii și rudele cu privire la fugă. Potrivit sursei publicației, cu câteva ore înainte de a părăsi țara, Assad a reunit înalți oficiali ai serviciilor de informații și ai armatei și le-a spus că „ajutorul militar din partea Rusiei este pe drum”.

La sfârșitul zilei de lucru, acesta i-a spus șefului său de birou că se îndreaptă spre casă, dar în realitate a mers la aeroport, au declarat interlocutorii Reuters. Potrivit sursei, el nu și-a avertizat fratele mai mic, care în cele din urmă a zburat cu elicopterul în Irak și de acolo ar fi mers la Moscova. Soția lui Assad, Asma, și cei trei copii ai lor se aflau deja în Rusia la momentul zborului său, a scris Reuters.

Anterior, Bloomberg, citându-și sursele, a relatat că evadarea lui Assad a fost organizată de serviciile secrete ruse: Moscova l-ar fi convins că va pierde lupta împotriva grupurilor armate conduse de islamiști și i-a oferit lui și familiei sale un coridor sigur dacă pleacă imediat.

    '''
    
    # Search for similar articles
    similar_articles = search_similar_articles(index_name, new_article_text, top_k=10)
    
    # Print the results
    print("Top 10 Similar Articles:")
    for i, article in enumerate(similar_articles, start=1):
        print(f"{i}. Title: {article['title']}")
        print(f"   URL: {article['url']}")
        print(f"   Similarity Score: {article['score']:.2f}")
