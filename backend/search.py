import os
import numpy as np
import torch
from sentence_transformers import SentenceTransformer, CrossEncoder, util
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import sent_tokenize
import markdown
from bs4 import BeautifulSoup
import re

# Download the punkt tokenizer for sentence splitting
nltk.download("punkt")

# Load pre-trained Sentence BERT model
bi_encoder = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


# Define EmbeddedDoc type
class EmbeddedDoc:
    def __init__(self, path, name, html, paragraphs, embeddings):
        self.path = path
        self.name = name
        self.html = html
        self.paragraphs = paragraphs  # List of paragraphs
        self.embeddings = embeddings  # List of embeddings for paragraphs


def strip_markdown(text):
    html = markdown.markdown(text)
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(), html


def split_into_paragraphs(text):
    # Split the text into paragraphs based on newlines
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    return paragraphs


def embed_paragraphs(paragraphs):
    return bi_encoder.encode(paragraphs)


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
                        paragraphs = split_into_paragraphs(plain_text)
                        embeddings = embed_paragraphs(paragraphs)
                        documents.append(
                            EmbeddedDoc(
                                path=filepath,
                                name=filename,
                                html=html_content,
                                paragraphs=paragraphs,
                                embeddings=embeddings,
                            )
                        )
    return documents


def mark_paragraph_with_class(
    html_content, paragraph, class_name="highlighted-paragraph"
):
    # Escape special characters in the paragraph for regex
    escaped_paragraph = re.escape(paragraph.strip())
    # Replace the paragraph with its marked version in the HTML content
    marked_html = re.sub(
        f"({escaped_paragraph})",
        f'<span class="{class_name}">\g<1></span>',
        html_content,
        flags=re.IGNORECASE,
    )
    return marked_html


def search(query, embedded_docs, top_k=3):
    query_embedding = bi_encoder.encode([query])[0]
    results = []
    for doc in embedded_docs:
        similarities = cosine_similarity([query_embedding], doc.embeddings)[0]
        for paragraph, similarity in zip(doc.paragraphs, similarities):
            results.append(
                {
                    "path": doc.path,
                    "name": doc.name,
                    "html": doc.html,
                    "paragraph": paragraph,
                    "similarity": similarity,
                }
            )

    cross_inp = [[query, result["paragraph"]] for result in results[:top_k]]
    cross_scores = cross_encoder.predict(cross_inp)
    for result, score in zip(results[:top_k], cross_scores):
        result["score"] = score
    return sorted(results[:top_k], key=lambda x: x["score"], reverse=True)
