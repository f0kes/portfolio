import os
import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder, util
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
bi_encoder = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


# Define EmbeddedDoc type
class EmbeddedDoc:
    def __init__(self, path, name, html, sentences, embeddings, full_embedding):
        self.path = path
        self.name = name
        self.html = html
        self.sentences = sentences  # List of sentences
        self.embeddings = embeddings  # List of embeddings for sentences
        self.full_embedding = full_embedding  # Single embedding for the full document


def strip_markdown(text):
    html = markdown.markdown(text)
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(), html


def split_into_sentences(text):
    # Split the text into sentences using nltk's sent_tokenize
    sentences = sent_tokenize(text)
    return [s.strip() for s in sentences if s.strip()]


def embed_sentences(sentences):
    return bi_encoder.encode(sentences)
    bi_encoder.las


def convert_custom_image_syntax(match):
    image_path = match.group(1)
    return f'<img src="/static/Portfolio{image_path}">'


def load_md_files(directory="./md_files"):
    documents = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".md"):
                filepath = os.path.join(root, filename)
                with open(filepath, "r", encoding="utf-8") as file:
                    content = file.read()
                    content = re.sub(
                        r"!\[\[(.+?)\]\]", convert_custom_image_syntax, content
                    )
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
                                full_embedding=bi_encoder.encode([plain_text])[0],
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


def search(query, embedded_docs, top_k=10):
    query_embedding = bi_encoder.encode([query])[0]
    results = []
    for doc in embedded_docs:
        similarities = cosine_similarity([query_embedding], doc.embeddings)[0]
        similarity = cosine_similarity([query_embedding], [doc.full_embedding])[0][0]
        bi_encoder.similarity(query, doc.sentences)
        sentence = doc.sentences[np.argmax(similarities)]
        results.append(
            {
                "path": doc.path,
                "name": doc.name,
                "html": doc.html,
                "sentence": sentence,
                "similarity": similarity,
            }
        )

    cross_inp = [[query, result["sentence"]] for result in results[:top_k]]
    cross_scores = cross_encoder.predict(cross_inp)
    for result, score in zip(results[:top_k], cross_scores):
        result["similarity"] = score
    return sorted(results[:top_k], key=lambda x: x["similarity"], reverse=True)


# Example usage:
# embedded_docs = load_md_files()  # Load your markdown files
# search_results = search("Your query here", embedded_docs)  # Search for a query
