from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

def index_sentiment(index_name: str, document: dict):
    try:
        response = es.index(index=index_name, document=document)
        print("Document indexé ", response["_id"])
        return response
    except Exception as e:
        print("Erreur d'indexation : ", e)
        return None

def test_connection():
    try:
        info = es.info()
        print("Connexion a ES réussie, version : ", info["version"]["number"])
    except Exception as e:
        print("Problème de connexion a elasticsearch, erreur : ", e)