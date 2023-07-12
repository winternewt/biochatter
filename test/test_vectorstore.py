from biochatter.vectorstore import (
    DocumentEmbedder,
    DocumentReader,
    Document,
)

import os
print(os.getcwd())

def test_document_summariser():
    # runs long, requires OpenAI API key and local milvus server
    # uses ada-002 for embeddings
    pdf_path = "test/bc_summary.pdf"
    with open(pdf_path, "rb") as f:
        doc_bytes = f.read()
    assert isinstance(doc_bytes, bytes)

    reader = DocumentReader()
    doc = reader.document_from_pdf(doc_bytes)
    docsum = DocumentEmbedder()
    docsum.set_document(doc)
    docsum.split_document()
    assert isinstance(docsum.split, list)
    assert isinstance(docsum.split[0], Document)

    docsum.store_embeddings()
    assert docsum.vector_db is not None

    query = "What is BioCypher?"
    results = docsum.similarity_search(query)
    assert len(results) == 3
    assert all(["BioCypher" in result.page_content for result in results])


def test_load_txt():
    reader = DocumentReader()
    text_path = "test/bc_summary.txt"
    document = reader.load_document(text_path)
    assert isinstance(document, list)
    assert isinstance(document[0], Document)


def test_load_pdf():
    reader = DocumentReader()
    pdf_path = "test/bc_summary.pdf"
    document = reader.load_document(pdf_path)
    assert isinstance(document, list)
    assert isinstance(document[0], Document)


def test_byte_txt():
    text_path = "test/bc_summary.txt"
    with open(text_path, "rb") as f:
        document = f.read()
    assert isinstance(document, bytes)

    reader = DocumentReader()
    doc = reader.document_from_txt(document)
    assert isinstance(doc, list)
    assert isinstance(doc[0], Document)
    # do we want byte string or regular string?


def test_byte_pdf():
    pdf_path = "test/bc_summary.pdf"
    # open as type "application/pdf"
    with open(pdf_path, "rb") as f:
        document = f.read()
    assert isinstance(document, bytes)

    reader = DocumentReader()
    doc = reader.document_from_pdf(document)
    assert isinstance(doc, list)
    assert isinstance(doc[0], Document)
    assert "numerous attempts at standardising KGs" in doc[0].page_content

CHUNK_SIZE = 100
CHUNK_OVERLAP = 10
def test_split_by_characters():
    docsum = DocumentEmbedder(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    pdf_path = "test/bc_summary.pdf"
    docsum._load_document(pdf_path)
    docsum.split_document()
    assert len(docsum.split) == 197

    text_path = "test/bc_summary.txt"
    docsum._load_document(text_path)
    docsum.split_document()
    assert 104 == len(docsum.split)

def test_split_by_tokens_tiktoken():
    docsum = DocumentEmbedder(
        split_by_tokens=True,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    pdf_path = "test/bc_summary.pdf"
    docsum._load_document(pdf_path)
    docsum.split_document()
    assert len(docsum.split) == 46

    text_path = "test/bc_summary.txt"
    docsum._load_document(text_path)
    docsum.split_document()
    assert 20 == len(docsum.split)

def test_split_by_tokens_tokenizers():
    docsum = DocumentEmbedder(
        split_by_tokens=True, 
        model="bigscience/bloom",
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    pdf_path = "test/bc_summary.pdf"
    docsum._load_document(pdf_path)
    docsum.split_document()
    assert len(docsum.split) == 49

    text_path = "test/bc_summary.txt"
    docsum._load_document(text_path)
    docsum.split_document()
    assert 44 == len(docsum.split)

