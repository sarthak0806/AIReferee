from groq import Groq
import os
from typing import Dict, List

class PaperEvaluator:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def evaluate(self, paper: Dict, references: List[Dict]) -> Dict:
        """Returns structured validation results using references"""
        verification = self._verify_against_references(paper['abstract'], references)
        
        assessment = self.client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{
                "role": "system",
                "content": f"""
                Analyze paper publishability using these reference checks:
                {verification['summary']}
                """
            }, {
                "role": "user",
                "content": f"Paper Abstract:\n{paper['abstract']}"
            }],
            temperature=0.2
        ).choices[0].message.content

        return {
            "verification": verification,
            "assessment": assessment
        }

    def _verify_against_references(self, abstract: str, references: List[Dict]) -> Dict:
        """Checks novelty, methodology, and contradictions"""
        checks = []
        for ref in references[:5]:  # Use top 5 references
            response = self.client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{
                    "role": "system",
                    "content": f"""
                    Compare reference with new paper:
                    REFERENCE: {ref['title']}
                    {ref['content'][:500]}
                    """
                }, {
                    "role": "user",
                    "content": f"""
                    Does this NEW PAPER ABSTRACT:
                    {abstract}
                    
                    1. Show NOVELTY beyond reference? (Y/N + reason)
                    2. Have BETTER METHODOLOGY? (Y/N + reason)
                    3. CONTRADICT reference? (Y/N + reason)
                    """
                }],
                temperature=0.3
            )
            checks.append({
                "reference": ref['title'],
                "analysis": response.choices[0].message.content,
                "source": ref.get('source', 'Unknown')
            })
        
        return {
            "checks": checks,
            "summary": "\n".join(
                f"Ref {i+1}: {check['reference']}\n{check['analysis']}" 
                for i, check in enumerate(checks)
            )
        }