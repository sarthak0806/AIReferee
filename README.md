# AIReferee - Research Paper Publishability Assessor

AIReferee is an AI-powered system designed to assist in evaluating the publishability of research papers. It streamlines the process of determining whether a paper meets academic standards for conference submission by automating critical tasks such as content extraction, query generation, and publishability evaluation.

## Problem Statement

As part of the **Kharagpur Data Science Hackathon 2025**, AIReferee was developed to tackle the problem of research paper evaluation. The system aims to classify research papers as **Publishable** or **Non-Publishable** based on their content, including methodologies, arguments, and evidence. Additionally, the system provides a framework for conference selection, recommending the most appropriate conference based on the paper’s content.

## Features

- **Paper Extraction**: Automatically extracts key components like the abstract from uploaded PDF papers.
- **Query Generation**: Generates relevant queries based on the abstract to help in research paper comparison.
- **Web Search**: Searches academic databases for references using generated queries.
- **Publishability Evaluation**: Assesses the paper’s publishability, classifying it as "Publishable" or "Non-Publishable" based on a set of criteria.
- **Conference Selection (Future Enhancements)**: Recommends suitable conferences for publishable papers, using predefined benchmarks and justifications.

## Architecture Overview

1. **Paper Extraction**: 
   - Extracts the abstract from the uploaded paper.
   
2. **Query Generation**:
   - Generates search queries based on the abstract of the paper.

3. **Web Search**:
   - Uses the queries to search academic databases for relevant references.

4. **Publishability Evaluation**:
   - Evaluates the paper's quality, analyzing aspects like methodology, coherence, and the validity of claims.

5. **Debugging and Reporting**:
   - Displays real-time progress and detailed debug information, including metrics like abstract length and number of references found.

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- Streamlit (for the web interface)
- Groq API key (for academic reference search)
- Required libraries (listed below)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/sarthak0806/AIReferee.git
   cd AIReferee
   

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:

   * Create a `.env` file in the project root and add your Groq API key:

     ```
     GROQ_API_KEY=your_api_key_here
     ```

4. Run the application:

   ```
   streamlit run app.py
   ```

### Folder Structure

```
AIReferee/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # List of Python dependencies
├── .env                    # Environment variables (e.g., GROQ_API_KEY)
├── utils/                  # Utility functions for paper extraction, querying, searching, and evaluation
│   ├── extractor.py
│   ├── querier.py
│   ├── searcher.py
│   └── evaluator.py
├── data/                   # Folder to store uploaded papers
├── Workflow.png            # Workflow diagram of the processing pipeline
└── README.md               # Project documentation
```

## How It Works

### 1. **Upload Paper**:

* The user uploads a PDF research paper using the file uploader in the Streamlit interface.

### 2. **Paper Extraction**:

* The system extracts the abstract from the uploaded PDF for further processing.

### 3. **Query Generation**:

* Based on the abstract, relevant search queries are generated.

### 4. **Web Search**:

* The system performs a web search to retrieve academic references that can be compared against the paper.

### 5. **Publishability Evaluation**:

* The system evaluates whether the paper is **Publishable** or **Non-Publishable** by analyzing the quality of arguments, methods, and evidence.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
