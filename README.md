# Target Store Reviews RAG Chatbot

A local AI chatbot that answers questions about a retail store (Target) by searching through customer reviews first, then answering based on what it finds. This technique is called **RAG** (Retrieval-Augmented Generation).

Everything runs on your own computer. There are no API keys and no cloud costs.

You can use it two ways:

- **Web GUI (recommended):** a chat interface in your browser, built with Streamlit
- **Terminal:** a simple text chat in the command line

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
- [Streamlit](https://streamlit.io/) (web GUI)
- pandas

## Project structure

```
target-reviews-rag/
├── app.py             # Streamlit web GUI
├── main.py            # Terminal version
├── vector.py          # Loads reviews, builds/loads the Chroma database, exposes the retriever
├── requirements.txt   # Python dependencies
└── data/
    └── sample_reviews.csv   # Fictional sample reviews
```

Both `app.py` and `main.py` use the same retriever from `vector.py`.

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

You should see `(venv)` at the start of your terminal prompt when the virtual environment is active.

## Running the chatbot

Make sure Ollama is running and your virtual environment is activated first.

### Option A: Web GUI (Streamlit)

```bash
streamlit run app.py
```

This opens a chat page in your browser at `http://localhost:8501`. If it doesn't open automatically, paste that address into your browser.

Features:

- Chat interface with streaming answers
- A "Reviews used" dropdown under each answer showing the rating, date and text of the reviews the answer was based on
- A "Clear chat" button in the sidebar

To stop the app, press `Ctrl + C` in the terminal.

> **Important:** Always start the GUI with `streamlit run app.py`. Running `python app.py` (or pressing a "Run" button in your editor) will not work and will print lots of `missing ScriptRunContext` warnings.

### Option B: Terminal

```bash
python main.py
```

Type a question and press Enter, or type `q` to quit.

The first run (either option) builds the vector database from the reviews, which may take a minute. After that it starts quickly.

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
REVIEWS_CSV=path/to/your_reviews.csv streamlit run app.py
```

(or `REVIEWS_CSV=path/to/your_reviews.csv python main.py` for the terminal version)

If you change the CSV, delete the `chroma_langchain_db/` folder so the database is rebuilt with the new data.

## Troubleshooting

**`streamlit: command not found`**
Your virtual environment isn't active, or Streamlit isn't installed in it. From the project folder run `source venv/bin/activate` (Windows: `venv\Scripts\activate`), then `pip install -r requirements.txt`. You need to re-activate the venv every time you open a new terminal.

**Lots of `missing ScriptRunContext` warnings**
You started the app with `python app.py`. Use `streamlit run app.py` instead.

**`Streamlit requires raw Python (.py) files, but the provided file has no extension`**
Your folder path probably contains spaces, so the terminal split it into pieces. Either run `streamlit run app.py` from inside the project folder, or wrap the full path in quotes:

```bash
streamlit run "/path/with spaces/target-reviews-rag/app.py"
```

**Connection error or "Is Ollama running?"**
Start the Ollama app (or run `ollama serve`), and check that both models are downloaded with `ollama list`.

**Answers use old or wrong data after changing the CSV**
Delete the `chroma_langchain_db/` folder and restart the app so the database is rebuilt.

## Credit

This project was built by following the tutorial [**How to Build a Local AI Agent With Python (Ollama, LangChain & RAG)**](https://www.youtube.com/watch?v=E4l91XKQSgw) by **Tech With Tim**.

I adapted it to answer questions about store reviews instead of the tutorial's original example, and added a Streamlit web interface.

## Ideas for improvement

- Add conversation memory so follow-up questions work ("what about the checkout?")
- Filter reviews by rating or date
- Add a file uploader so reviews can be added from the GUI
- Experiment with the number of retrieved reviews (`k`) and compare answer quality

## Notes

- Built and tested with Python 3.14.
- Completed from the original ideas list: web interface, showing which reviews were used for each answer, and a prompt that tells the model to say "I don't know" when the reviews don't cover a question.