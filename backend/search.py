import os
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import sent_tokenize
import markdown
from bs4 import BeautifulSoup
import re

# Download the punkt tokenizer for sentence splitting
nltk.download("punkt")
nltk.download("punkt_tab")
# Load pre-trained Sentence BERT model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Define EmbeddedDoc type
class EmbeddedDoc:
    def __init__(self, path, name, html, sentences, embeddings):
        self.path = path
        self.name = name
        self.html = html
        self.sentences = sentences
        self.embeddings = embeddings  # List of embeddings for sentences


def strip_markdown(text):
    html = markdown.markdown(text)
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(), html


def split_into_sentences(text):
    return sent_tokenize(text)


def embed_sentences(sentences):
    return model.encode(sentences)


def load_md_files(directory="./md_files"):
    documents = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".md"):
                filepath = os.path.join(root, filename)
                with open(filepath, "r", encoding="utf-8") as file:
                    content = file.read()
                    plain_text, html_content = strip_markdown(content)
                    if plain_text:
                        sentences = split_into_sentences(plain_text)
                        embeddings = embed_sentences(sentences)
                        documents.append(
                            EmbeddedDoc(
                                path=filepath,
                                name=filename,
                                html=html_content,
                                sentences=sentences,
                                embeddings=embeddings,
                            )
                        )
    return documents


def mark_sentence_with_class(html_content, sentence, class_name="highlighted-sentence"):
    # Escape special characters in the sentence for regex
    escaped_sentence = re.escape(sentence.strip())
    # Replace the sentence with its marked version in the HTML content
    marked_html = re.sub(
        f"({escaped_sentence})",
        f'<span class="{class_name}">\g<1></span>',
        html_content,
        flags=re.IGNORECASE,
    )
    return marked_html


def search(query, embedded_docs, top_k=5):
    query_embedding = model.encode([query])[0]
    results = []

    for doc in embedded_docs:
        similarities = cosine_similarity([query_embedding], doc.embeddings)[0]
        top_sentence_index = similarities.argmax()

        # Mark the chosen sentence with a CSS class in the HTML content

        results.append(
            {
                "path": doc.path,
                "name": doc.name,
                "html": doc.html,
                "sentence": doc.sentences[top_sentence_index],
                "similarity": similarities.mean().item(),
            }
        )

    return sorted(results, key=lambda x: x["similarity"], reverse=True)[:top_k]
