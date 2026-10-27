# Target Store Reviews RAG Chatbot

A local AI chatbot that answers questions about a retail store (Target) by searching through customer reviews first, then answering based on what it finds. This technique is called **RAG** (Retrieval-Augmented Generation).

Everything runs on your own computer. There are no API keys and no cloud costs.

## How it works

1. **Load:** `vector.py` reads the reviews from a CSV file.
2. **Embed:** each review is turned into a vector (a list of numbers that captures its meaning) using the `mxbai-embed-large` model through Ollama.
3. **Store:** the vectors are saved in a local [ChromaDB](https://www.trychroma.com/) database.
4. **Retrieve:** when you ask a question, the 5 most relevant reviews are pulled from the database.
5. **Answer:** those reviews and your question are given to the `llama3.2` model, which writes the answer.

## Tech stack

- Python
- [Ollama](https://ollama.com/) (runs the language and embedding models locally)
- [LangChain](https://www.langchain.com/)
- [ChromaDB](https://www.trychroma.com/) (vector database)
- pandas

## Setup

### 1. Install Ollama

Download it from [ollama.com](https://ollama.com/) and make sure it's running.

### 2. Download the models

```bash
ollama pull llama3.2
ollama pull mxbai-embed-large
```

### 3. Clone this repo and install dependencies

```bash
git clone https://github.com/s4251447/target-reviews-rag.git
cd target-reviews-rag

python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 4. Run the chatbot

```bash
python main.py
```

The first run builds the vector database from the reviews, which may take a minute. After that it starts instantly. Type a question and press Enter, or type `q` to quit.

Example questions:
- "What do customers say about the staff?"
- "Is the store clean?"
- "Are there any complaints about the checkout?"

## Using your own reviews

The repo includes `data/sample_reviews.csv`, which contains **fictional** reviews so the project works out of the box.

To use your own data, make a CSV with these columns:

```
Title,Date,Rating,Review
```

Then point the app at it:

```bash
REVIEWS_CSV=path/to/your_reviews.csv python main.py
```

If you change the CSV, delete the `chroma_langchain_db/` folder so the database is rebuilt with the new data.

## Credit

This project was built by following the tutorial
[**How to Build a Local AI Agent With Python (Ollama, LangChain & RAG)**](https://www.youtube.com/watch?v=E4l91XKQSgw) by **Tech With Tim**.

I adapted it to answer questions about store reviews instead of the tutorial's original example.

## Ideas for improvement

- Add a simple web interface (Streamlit or Gradio)
- Show which reviews were used for each answer
- Filter reviews by rating or date
- Tighten the prompt so the model says "I don't know" when the reviews don't cover a question
- Experiment with the number of retrieved reviews (`k`) and compare answer quality

## Notes

- Built and tested with Python 3.14.
- If you get a connection error, make sure Ollama is running.
