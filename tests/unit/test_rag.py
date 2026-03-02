"""Unit tests for RAG pipeline — embedding, search, RRF merge."""


from src.rag.embedder import EMBEDDING_DIMENSION, Embedder
from src.rag.indexer import DocumentIndexer
from src.rag.search import RAGDocument, RAGSearch


class TestEmbedder:
    """Test text embedding."""

    def test_pseudo_embedding_dimension(self):
        embedding = Embedder._pseudo_embedding("test query")
        assert len(embedding) == EMBEDDING_DIMENSION

    def test_pseudo_embedding_deterministic(self):
        e1 = Embedder._pseudo_embedding("same text")
        e2 = Embedder._pseudo_embedding("same text")
        assert e1 == e2

    def test_pseudo_embedding_different_for_different_text(self):
        e1 = Embedder._pseudo_embedding("text one")
        e2 = Embedder._pseudo_embedding("text two")
        assert e1 != e2

    def test_pseudo_embedding_normalized(self):
        embedding = Embedder._pseudo_embedding("test normalized output")
        for val in embedding:
            assert -1.0 <= val <= 1.0


class TestRRFMerge:
    """Test Reciprocal Rank Fusion merge."""

    def test_rrf_merge_combines_results(self):
        vector_results = [
            RAGDocument(id="a", content="doc a", title="A", score=0.9),
            RAGDocument(id="b", content="doc b", title="B", score=0.8),
        ]
        keyword_results = [
            RAGDocument(id="b", content="doc b", title="B", score=0.85),
            RAGDocument(id="c", content="doc c", title="C", score=0.7),
        ]

        merged = RAGSearch._rrf_merge(vector_results, keyword_results, k=60)

        assert len(merged) == 3
        # "b" appears in both lists, should have highest RRF score
        assert merged[0].id == "b"

    def test_rrf_merge_empty_lists(self):
        merged = RAGSearch._rrf_merge([], [])
        assert merged == []

    def test_rrf_merge_one_empty(self):
        vector_results = [
            RAGDocument(id="a", content="doc a", title="A", score=0.9),
        ]
        merged = RAGSearch._rrf_merge(vector_results, [], k=60)
        assert len(merged) == 1
        assert merged[0].id == "a"


class TestDocumentChunking:
    """Test document chunking for indexing."""

    def test_short_text_single_chunk(self):
        chunks = DocumentIndexer._chunk_text("Short text", chunk_size=100)
        assert len(chunks) == 1
        assert chunks[0] == "Short text"

    def test_long_text_multiple_chunks(self):
        text = "a" * 2500
        chunks = DocumentIndexer._chunk_text(text, chunk_size=1000, overlap=200)
        assert len(chunks) >= 3

    def test_chunk_overlap(self):
        text = "abcdefghij" * 100  # 1000 chars
        chunks = DocumentIndexer._chunk_text(text, chunk_size=400, overlap=100)
        # Verify overlap exists
        if len(chunks) > 1:
            end_of_first = chunks[0][-100:]
            start_of_second = chunks[1][:100]
            assert end_of_first == start_of_second
