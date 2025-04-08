import streamlit as st
import tempfile
import os
import re
from dotenv import load_dotenv
from groq import Groq
from utils.extractor import PaperExtractor
from utils.querier import QueryGenerator
from utils.searcher import ResearchSearcher
from utils.evaluator import PaperEvaluator

# Load environment variables
load_dotenv()

def initialize_groq_client():
    """Handle API key initialization with proper error messages"""
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        st.error("""
        API key not found. Please:
        1. Create a .env file in your project root
        2. Add: GROQ_API_KEY=your_key_here
        3. Restart the app
        """)
        st.stop()
    
    try:
        return Groq(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize Groq client: {str(e)}")
        st.stop()

def main():
    st.set_page_config(page_title="Research Assessor", layout="wide")
    st.title("📄 Academic Paper Publishability Assessor")
    
    # Initialize client
    client = initialize_groq_client()
    
    # File upload
    uploaded_file = st.file_uploader("Upload research paper (PDF)", type="pdf")
    if not uploaded_file:
        return
    
    # Temporary file handling
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name
    
    try:
        # Initialize components
        extractor = PaperExtractor()
        querier = QueryGenerator()
        searcher = ResearchSearcher()
        evaluator = PaperEvaluator()
        
        # Processing pipeline
        progress = st.progress(0)
        status_text = st.empty()
        
        # 1. Extract content
        status_text.text("🔍 Extracting paper content...")
        abstract = extractor.extract_abstract(tmp_path)
        progress.progress(25)
        st.session_state['debug_abstract'] = abstract
        
        # 2. Generate queries
        status_text.text("💡 Generating search queries...")
        queries = querier.generate_queries(abstract)
        progress.progress(50)
        st.session_state['debug_queries'] = queries
        
        # 3. Web search
        status_text.text("🌐 Searching academic databases...")
        search_results = searcher.search_all(queries)
        progress.progress(75)
        st.session_state['debug_results'] = search_results
        
        # 4. Evaluation
        status_text.text("🧠 Evaluating publishability...")
        evaluation = evaluator.evaluate({"abstract": abstract}, search_results)
        progress.progress(100)
        status_text.success("✅ Analysis complete!")
        
        # Display verification and assessment
        st.subheader("🔬 Reference Verification")
        for check in evaluation['verification']['checks']:
            with st.expander(f"vs. {check['reference'][:30]}..."):
                st.markdown(f"**Reference Source**: {check.get('source', 'Unknown')}")
                st.markdown(f"**Analysis**:\n{check['analysis']}")

        st.subheader("📝 Final Assessment")
        st.markdown(evaluation['assessment'])
        
        # Debug info
        with st.expander("🔧 Debug Information"):
            st.subheader("Processing Pipeline")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Abstract Length", f"{len(abstract.split())} words")
                st.write("### Generated Queries")
                st.write(queries)
                
            with col2:
                st.metric("References Found", len(search_results))
                st.write("### Sample References")
                if search_results:
                    st.json(search_results[0])
            
            st.write("### Full Abstract")
            st.text(abstract[:500] + "...")

    except Exception as e:
        st.error(f"Processing error: {str(e)}")
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

if __name__ == "__main__":
    main()