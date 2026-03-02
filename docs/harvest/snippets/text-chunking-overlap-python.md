# Snippet: Text Chunking with Sliding Window Overlap (Python)

## Maturity: Alpha v1.0
## Extracted: 2026-03-02
## Version: v1.0

---

## Description

Splits text into overlapping chunks using a sliding window approach. Each chunk has a configurable maximum size (in characters), and consecutive chunks overlap by a configurable number of characters. This prevents information loss at chunk boundaries, which is critical for RAG pipelines where relevant context may span a chunk boundary.

## Dependencies

None (Python standard library only).

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `chunk_size` | `1000` | Maximum number of characters per chunk. |
| `overlap` | `200` | Number of overlapping characters between consecutive chunks. |

## Code

```python
def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200,
) -> list[str]:
    """Split text into overlapping chunks using a sliding window.

    Args:
        text: The input text to split.
        chunk_size: Maximum characters per chunk.
        overlap: Number of characters shared between consecutive chunks.

    Returns:
        List of text chunks. Empty input returns an empty list.

    Raises:
        ValueError: If overlap >= chunk_size.
    """
    if not text:
        return []
    if overlap >= chunk_size:
        raise ValueError(f"overlap ({overlap}) must be less than chunk_size ({chunk_size})")

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks
```

## Usage Example

```python
document = "A" * 2500  # 2500 characters of text

chunks = chunk_text(document, chunk_size=1000, overlap=200)
# Returns 4 chunks:
#   chunk 0: characters 0-999    (1000 chars)
#   chunk 1: characters 800-1799 (1000 chars, overlaps 200 with chunk 0)
#   chunk 2: characters 1600-2499 (900 chars, overlaps 200 with chunk 1)
#   chunk 3: characters 2400-2499 (100 chars, overlaps 200 with chunk 2)

# With real text:
text = "The quick brown fox jumps over the lazy dog. " * 50
chunks = chunk_text(text, chunk_size=500, overlap=100)
for i, chunk in enumerate(chunks):
    print(f"Chunk {i}: {len(chunk)} chars")
```

## Notes

- This implementation chunks by character count. For token-aware chunking (needed when feeding into LLMs with token limits), replace `len(text)` with a tokenizer (e.g., tiktoken) and slice by token boundaries.
- The overlap should be large enough to capture a complete sentence or paragraph at the boundary. A common heuristic is 10-20% of `chunk_size`.
- For better chunk quality, consider splitting on sentence or paragraph boundaries instead of raw character positions. This simple version prioritizes correctness and predictability.
- The last chunk may be smaller than `chunk_size`. This is expected and correct.

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction and decontextualization |
