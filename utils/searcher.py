from serpapi import GoogleSearch
import arxiv
from typing import List, Dict
import time
import os
from dotenv import load_dotenv
load_dotenv()
class ResearchSearcher:
    def __init__(self):
        self.scholar_engine = "google_scholar"
        self.serpapi_key = os.getenv("SERPAPI_KEY")

    def search_scholar(self, query: str) -> List[Dict]:
        """Searches Google Scholar with rate limiting"""
        time.sleep(1)  # Avoid rate limits
        try:
            results = GoogleSearch({
                "engine": self.scholar_engine,
                "q": query,
                "api_key": self.serpapi_key,
                "num": 2
            }).get_dict().get("organic_results", [])
            return [{
                "title": r.get("title"),
                "content": r.get("snippet"),
                "source": "Google Scholar"
            } for r in results]
        except Exception:
            return []

    def search_arxiv(self, query: str) -> List[Dict]:
        """Searches arXiv repository"""
        try:
            results = arxiv.Search(
                query=query,
                max_results=2,
                sort_by=arxiv.SortCriterion.Relevance
            ).results()
            return [{
                "title": r.title,
                "content": r.summary,
                "source": "arXiv"
            } for r in results]
        except Exception:
            return []

    def search_all(self, queries: List[str]) -> List[Dict]:
        """Executes all searches"""
        return [result for query in queries 
                for result in self.search_scholar(query) + self.search_arxiv(query)]