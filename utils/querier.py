from typing import List
import os
from groq import Groq

class QueryGenerator:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def generate_queries(self, abstract: str) -> List[str]:
        """Generates 2-3 precise search queries for context retrieval"""
        response = self.client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{
                "role": "system",
                "content": """You are an academic search assistant. Generate 2-3 precise search queries 
                to find papers that could validate or contradict this research. Return ONLY a JSON array 
                of query strings, with no additional text or numbering."""
            }, {
                "role": "user",
                "content": f"Abstract:\n{abstract}"
            }],
            temperature=0.3,  # Lower for more focused results
            response_format={"type": "json_object"}
        )
        
        try:
            queries = eval(response.choices[0].message.content)["queries"]
            return [q.strip('"') for q in queries][:3]  # Ensure max 3 queries
        except:
            # Fallback if JSON parsing fails
            return [
                "novel approaches to " + abstract.split()[0] + " " + abstract.split()[1],
                "state-of-the-art techniques in " + abstract[:50].split(",")[0],
                "limitations of " + abstract[:30]
            ]