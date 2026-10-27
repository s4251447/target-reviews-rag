from langchain_ollama.llms import OllamaLLM # directly use Ollama Model
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model = OllamaLLM(model="llama3.2") #Using Model llama3.2 from Ollama

template = """
You are an expert in answering questions about a Retail Store (Target)

Here are some relevant reviews: {reviews}

Here is the question to answer: {question}
"""
prompt = ChatPromptTemplate.from_template(template) # Pass variables reviews and question into prompt template
chain = prompt | model #gives it to the model


while True:
    print("\n\n-------------------------------")
    question = input("Write a message... (q) to quit: ")
    print("\n\n-------------------------------")
    if question == "q":
        print("Thank you hope to see you again soon!")
        break
    reviews = retriever.invoke(question)
    result = chain.invoke({"reviews": reviews, "question": question})
    print(result)