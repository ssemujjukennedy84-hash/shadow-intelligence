import os, chromadb, random, re

class ArtOfWarRAG:
    def __init__(self, book_path="data/art_of_war.txt"):
        self.client = chromadb.PersistentClient(path="data/chroma_db")
        try:
            self.collection = self.client.get_collection(name="art_of_war")
        except:
            self.collection = self.client.create_collection(name="art_of_war")
        if self.collection.count() == 0 and os.path.exists(book_path):
            with open(book_path, 'r', encoding='utf-8') as f:
                text = f.read()
            sentences = re.split(r'(?<=[.!?])\s+', text)
            for i in range(0, len(sentences), 3):
                chunk = ' '.join(sentences[i:i+3]).strip()
                if len(chunk) > 50:
                    self.collection.add(documents=[chunk], ids=[f"c{i}"])
    
    def search(self, query: str, n_results: int = 3, domain: str = None) -> list:
        if self.collection.count() == 0:
            return [{"text": "If you know the enemy and know yourself, you need not fear the result of a hundred battles.", "relevance": 1.0}]
        try:
            results = self.collection.query(query_texts=[query], n_results=min(n_results, self.collection.count()))
            passages = [{'text': results['documents'][0][i], 'relevance': 1-(i*0.1)} for i in range(len(results['documents'][0]))]
            random.shuffle(passages)
            return passages[:n_results] if passages else [{"text": "All warfare is based on deception.", "relevance": 1.0}]
        except:
            return [{"text": "The supreme art of war is to subdue the enemy without fighting.", "relevance": 1.0}]