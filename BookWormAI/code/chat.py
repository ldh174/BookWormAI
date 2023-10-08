import os

import datetime
from flask import request
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain

import json
import PyPDF2
import numpy as np
import threading
import csv

os.environ["OPENAI_API_KEY"] = "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"

def get_review2(file, public=True):
    writer = csv.writer(open('data/reviews.csv', 'a'))
    # File, Title, Author, Time, review
    #writer.writerow("sample")
    final_review = "this book was ok"
    arr = [request.files['file'].filename, request.form.get('title'), request.form.get('author'), str(datetime.datetime.now()), ("\"" + final_review +"\"")]

    writer.writerow(arr)
    return None

def get_review(file, public):
    print("start")

    if(file.filename.rsplit('.', 1)[1].lower() == 'pdf'):
        contents = text_from_pdf(request.files['file'].content)
    else:
        contents = request.files['file'].read().decode('utf-8')

    contents = contents.replace("\n", "").replace(";", "")

    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator=' ',
        encoding_name="cl100k_base",
        chunk_size=16000,
        chunk_overlap=10
    )

    # Splits the text file into chunks
    chunks = text_splitter.split_text(contents)

    # Define prompt
    focus = ["pacing", "length", "vocabulary", "readability", "plot"]

    selected = []

    for i in range(4):
        temp = focus[np.random.randint(len(focus))]
        focus.remove(temp)
        selected.append(temp)

    prompt_template = """Write a unique review with both positives and negatives of the following focusing on %s and %s with 
    minor details about %s and %s in one line and without mentions of chapters:
    "{text}"
    DETAILED REVIEW:""" % (selected[0], selected[1], selected[2], selected[3])

    prompt = PromptTemplate.from_template(prompt_template)

    # Create chains
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    reviews = ""
    if len(chunks) == 1:
        final_review = llm_chain.run(chunks[0])
        writer = csv.writer(open('data/reviews.csv', 'a'))
        arr = [request.files['file'].filename, request.form.get('title'), request.form.get('author'), str(datetime.datetime.now()), final_review]
        writer.writerow(arr)

        return final_review
    # Synthesizes reviews if more than one chunk
    else:
        threads = []

        lock = threading.Lock()

        reviews = ""
        # Send multiple API calls at the same time with threading
        def run_chain(item):
            nonlocal reviews
            current_review = llm_chain.run(item) + '\n'
            with lock:
                reviews += current_review

        for chunk in chunks:
            thread = threading.Thread(target=run_chain, args=(chunk,))
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
            print("threads have been joined")

        # Change prompts
        new_prompt = PromptTemplate.from_template("""Make a new comprehensive review based on the following without mentioning chapter names:
        "{reviews}" NEW COMPREHENSIVE REVIEW:""")

        llm_chain.prompt = new_prompt
        final_review = llm_chain.run(''.join(str(review) for review in reviews))

        #if public:
        # File, Title, Author, Time, review
        #writer.writerow("sample")
        writer = csv.writer(open('data/reviews.csv', 'a'))
        # File, Title, Author, Time, review
        #writer.writerow("sample")
        arr = [request.files['file'].filename, request.form.get('title'), request.form.get('author'), str(datetime.datetime.now()), final_review]
        writer.writerow(arr)

        print("done")
        return final_review

def text_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as pdf:
        reader = PyPDF2.PdfFile