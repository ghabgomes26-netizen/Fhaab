import os
import json
import faiss
import numpy as np
from typing import List, Optional
from pathlib import Path
import openai


class EmbeddingsIndex:
    """Índice simples de embeddings usando OpenAI para vetores e FAISS para busca.

    Salva duas coisas dentro do `index_path`:
    - index.faiss: o índice FAISS binário
    - meta.json: lista de textos que correspondem às entradas do índice
    """

    def __init__(self, index_path: str = ".embeddings_index", model: str = "text-embedding-3-small"):
        self.index_path = Path(index_path)
        self.index_file = self.index_path / "index.faiss"
        self.meta_file = self.index_path / "meta.json"
        self.model = model
        self._index: Optional[faiss.IndexFlatIP] = None
        self._meta: List[str] = []

        # cria diretório se não existir
        self.index_path.mkdir(parents=True, exist_ok=True)

    def exists(self) -> bool:
        return self.index_file.exists() and self.meta_file.exists()

    def is_ready(self) -> bool:
        return self._index is not None and len(self._meta) > 0

    def load(self):
        """Carrega o índice FAISS e o arquivo de metadados."""
        if not self.exists():
            raise FileNotFoundError("Índice ou meta não encontrado")

        # carrega meta
        with open(self.meta_file, "r", encoding="utf-8") as f:
            self._meta = json.load(f)

        # carrega índice
        self._index = faiss.read_index(str(self.index_file))

    def save(self):
        """Persiste o índice e os metadados no disco."""
        if self._index is None:
            raise RuntimeError("Índice vazio, nada para salvar")

        faiss.write_index(self._index, str(self.index_file))
        with open(self.meta_file, "w", encoding="utf-8") as f:
            json.dump(self._meta, f, ensure_ascii=False)

    def _embed_texts(self, texts: List[str]) -> np.ndarray:
        """Chama a API de embeddings do OpenAI e retorna np.ndarray float32 (n x d)."""
        if not texts:
            return np.zeros((0, 0), dtype=np.float32)

        # Chamada em lote
        resp = openai.Embedding.create(model=self.model, input=texts)
        vectors = [item["embedding"] for item in resp["data"]]
        arr = np.array(vectors, dtype=np.float32)
        return arr

    def build_from_repo(self, repo_path: str = ".", file_exts: Optional[List[str]] = None, max_files: int = 500):
        """Percorre o repositório, lê arquivos de texto e cria um índice de embeddings.

        file_exts: lista de extensões (ex.: [".py", ".md"]). Se None, usa um conjunto padrão.
        """
        if file_exts is None:
            file_exts = [
                ".py", ".md", ".txt", ".js", ".ts", ".java", ".go", ".rs", ".html", ".css", ".json"
            ]

        repo = Path(repo_path)
        texts = []

        # procura arquivos
        for p in repo.rglob("*"):
            if p.is_file() and p.suffix.lower() in file_exts:
                try:
                    text = p.read_text(encoding="utf-8")
                except Exception:
                    continue

                # faz um split simples em blocos para documentos grandes
                chunks = self._chunk_text(text)
                for c in chunks:
                    texts.append(f"File: {p.relative_to(repo)}\n\n{c}")

                if len(texts) >= max_files:
                    break

        if not texts:
            raise RuntimeError("Nenhum texto encontrado para indexar")

        vecs = self._embed_texts(texts)

        # normaliza para similaridade por produto interno (use inner product com vetores L2-normalizados)
        norms = np.linalg.norm(vecs, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        vecs = vecs / norms

        dim = vecs.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(vecs)

        self._index = index
        self._meta = texts
        self.save()

    def _chunk_text(self, text: str, chunk_size: int = 1500, overlap: int = 200) -> List[str]:
        """Divide texto grande em pedaços com overlap para melhor recuperação."""
        if len(text) <= chunk_size:
            return [text]

        chunks = []
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunks.append(text[start:end])
            start = max(0, end - overlap)
            if end == len(text):
                break
        return chunks

    def query(self, query_text: str, top_k: int = 3) -> List[str]:
        """Consulta o índice e retorna os top_k textos (metadados) mais relevantes."""
        if self._index is None or not self._meta:
            return []

        vec = self._embed_texts([query_text])
        if vec.size == 0:
            return []

        # normaliza
        vec = vec / (np.linalg.norm(vec, axis=1, keepdims=True) + 1e-10)

        D, I = self._index.search(vec, top_k)
        hits = []
        for idx in I[0]:
            if idx < len(self._meta):
                hits.append(self._meta[idx])
        return hits


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Constrói um índice de embeddings para um repositório")
    parser.add_argument("--repo", default=".", help="Caminho para o repositório")
    parser.add_argument("--model", default=None, help="Modelo de embeddings (usa variável de ambiente EMBEDDING_MODEL se não informado)")
    args = parser.parse_args()

    model = args.model or os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    idx = EmbeddingsIndex(index_path=".embeddings_index", model=model)
    print("Construindo índice de embeddings (pode demorar)...")
    idx.build_from_repo(repo_path=args.repo)
    print("Índice criado com sucesso.")
