# Giải Thích Chi Tiết File `document_chunker.py`

Tài liệu này giải thích **từng dòng code** trong file [src/document_chunker.py](src/document_chunker.py) cho người **chưa biết lập trình Python**. Sau khi đọc xong, bạn sẽ hiểu:

1. Mục đích của từng đoạn code.
2. Vì sao tác giả viết nó như vậy.
3. Khi chương trình chạy, mỗi dòng làm gì với dữ liệu thật.

---

## 1. Bối Cảnh: "Chunking" Là Gì Và Tại Sao Cần?

Trong hệ thống **RAG (Retrieval-Augmented Generation)**, ta phải đưa các tài liệu dài (sách, PDF, file Markdown...) vào một cơ sở dữ liệu vector để LLM có thể tra cứu. LLM không đọc hết cả cuốn sách được — nó cần các **mẩu văn bản nhỏ** (gọi là **chunk**) vừa đủ ngắn để xử lý, vừa đủ dài để giữ ngữ nghĩa.

File này dùng kỹ thuật **Parent–Child Chunking**:

- **Parent chunk** (chunk cha): đoạn dài (~2000–4000 ký tự), giữ ngữ cảnh đầy đủ.
- **Child chunk** (chunk con): đoạn ngắn (~500 ký tự), dùng để **tìm kiếm** chính xác.

Khi user hỏi, hệ thống tìm child trước (chính xác hơn vì ngắn), rồi trả về **parent tương ứng** cho LLM (để LLM có đủ ngữ cảnh).

---

## 2. Phần Import — Mượn Công Cụ Bên Ngoài

```python
import glob
import os
from pathlib import Path
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
import config
```

| Dòng | Ý nghĩa | Khi chạy |
|------|---------|----------|
| `import glob` | Mượn thư viện `glob` — chuyên **tìm file theo mẫu** (ví dụ "tất cả file `.md`"). | Cho phép viết `glob.glob("*.md")` để liệt kê file. |
| `import os` | Mượn thư viện `os` — thao tác với **hệ điều hành** (đường dẫn, thư mục). | Dùng `os.path.join(...)` để ghép đường dẫn an toàn cho cả Windows/Linux. |
| `from pathlib import Path` | Mượn class `Path` — cách hiện đại hơn để xử lý đường dẫn (file). | Cho phép viết `Path("a/b.md").stem` để lấy "b" (tên file không có đuôi). |
| `from langchain_text_splitters import ...` | Mượn **hai loại splitter** từ thư viện LangChain. | `MarkdownHeaderTextSplitter` cắt theo tiêu đề `#`, `##`. `RecursiveCharacterTextSplitter` cắt theo độ dài ký tự. |
| `import config` | Mượn **file config.py** trong cùng thư mục — nơi chứa hằng số (chunk size, đường dẫn). | Dùng `config.CHILD_CHUNK_SIZE` để lấy giá trị `500`. |

**Vì sao tách config ra file riêng?** → Để dễ chỉnh thông số mà không phải sửa code logic.

---

## 3. Định Nghĩa Class `DocumentChuncker`

```python
class DocumentChuncker:
```

**Class** giống như "bản thiết kế" để tạo ra **đối tượng** (object). Tưởng tượng class là **bản vẽ ô tô**, còn object là **chiếc xe thực sự** chạy được.

Ta cần đóng gói các hàm chunking thành một class vì:
- Giữ trạng thái (các splitter đã cấu hình sẵn) để dùng nhiều lần.
- Code gọn, dễ tái sử dụng ở nhiều nơi.

> ⚠️ Lưu ý: Tên class viết sai chính tả là `DocumentChuncker` (thừa chữ `c`), đúng phải là `DocumentChunker`. Đây là lỗi nhỏ không ảnh hưởng chức năng nhưng nên sửa khi có dịp.

---

## 4. Hàm Khởi Tạo `__init__` — "Khi Object Ra Đời"

```python
def __init__(self):
    self.__parent_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=config.HEADERS_TO_SPLIT_ON,
        strip_headers=False
    )
    self.__child_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHILD_CHUNK_SIZE,
        chunk_overlap=config.CHILD_CHUNK_OVERLAP
    )
    self.__min_parent_size = config.MIN_PARENT_SIZE
    self.__max_parent_size = config.MAX_PARENT_SIZE
```

### Giải thích từng dòng

**`def __init__(self):`**
- `def` = định nghĩa hàm.
- `__init__` là tên đặc biệt — Python tự gọi nó **khi bạn tạo object mới**.
- `self` = bản thân object đang được tạo. Bắt buộc có ở mọi hàm trong class.

**Ví dụ chạy:** Khi bạn viết `chunker = DocumentChuncker()`, Python tự động chạy `__init__` để gán các thuộc tính cho `chunker`.

**`self.__parent_splitter = MarkdownHeaderTextSplitter(...)`**
- Tạo một "máy cắt theo tiêu đề" và gắn nó vào object.
- Hai dấu `__` ở đầu tên (`__parent_splitter`) là quy ước Python để nói **"đây là biến nội bộ, đừng động vào từ bên ngoài"**.
- `headers_to_split_on=config.HEADERS_TO_SPLIT_ON` → tham số `[("#", "H1"), ("##", "H2"), ("###", "H3")]`. Nghĩa là: hễ gặp `#`, `##`, `###` thì cắt ra một chunk mới.
- `strip_headers=False` → **giữ lại** dòng tiêu đề trong chunk (nếu `True` thì xóa luôn header). Giữ lại để chunk vẫn có ngữ cảnh "đoạn này nói về gì".

**`self.__child_splitter = RecursiveCharacterTextSplitter(...)`**
- Máy cắt theo độ dài. Khác với cái trên (cắt theo header), cái này cắt **theo số ký tự**.
- `chunk_size=500` → mỗi chunk con tối đa 500 ký tự.
- `chunk_overlap=100` → mỗi chunk con **trùng 100 ký tự** với chunk kế bên. Mục đích: tránh **mất ngữ cảnh giữa hai chunk** (ví dụ một câu bị cắt đôi).

**`self.__min_parent_size = config.MIN_PARENT_SIZE`** (= 2000)
- Parent chunk **phải dài tối thiểu** 2000 ký tự. Ngắn hơn → cần gộp lại.

**`self.__max_parent_size = config.MAX_PARENT_SIZE`** (= 4000)
- Parent chunk **tối đa** 4000 ký tự. Dài hơn → cần cắt nhỏ.

### Tổng kết bước này

Sau khi `__init__` chạy xong, object `chunker` đã có 4 "đồ nghề" sẵn sàng:
- `__parent_splitter` (cắt theo header)
- `__child_splitter` (cắt theo độ dài)
- `__min_parent_size = 2000`
- `__max_parent_size = 4000`

---

## 5. Hàm `create_chunks` — "Cánh Cửa Chính"

```python
def create_chunks(self, path_dir=config.MARKDOWN_DIR):
    all_parent_chunks, all_child_chunks = [], []

    for doc_path_str in sorted(glob.glob(os.path.join(path_dir, "*.md"))):
        doc_path = Path(doc_path_str)
        parent_chunks, child_chunks = self.create_chunks_single(doc_path)
        all_parent_chunks.extend(parent_chunks)
        all_child_chunks.extend(child_chunks)
        
    return all_parent_chunks, all_child_chunks
```

### Mục đích
Đọc **toàn bộ file `.md`** trong một thư mục, chunk từng file, rồi gom tất cả parent/child lại trả về.

### Giải thích từng dòng

**`def create_chunks(self, path_dir=config.MARKDOWN_DIR):`**
- Hàm có 1 tham số `path_dir` với **giá trị mặc định** là `config.MARKDOWN_DIR` (tức `/home/ducduy/agentic-rag/markdown_docs`).
- Có nghĩa: gọi `chunker.create_chunks()` → tự lấy thư mục mặc định. Gọi `chunker.create_chunks("/abc")` → dùng thư mục `/abc`.

**`all_parent_chunks, all_child_chunks = [], []`**
- Tạo **hai list rỗng** cùng lúc. Tương đương:
  ```python
  all_parent_chunks = []
  all_child_chunks = []
  ```
- List = mảng có thể chứa nhiều phần tử (giống cái rổ).

**`for doc_path_str in sorted(glob.glob(os.path.join(path_dir, "*.md"))):`**

Bóc tách từng phần (đọc từ **trong ra ngoài**):

1. `os.path.join(path_dir, "*.md")` → ghép thành `"/home/ducduy/agentic-rag/markdown_docs/*.md"`.
2. `glob.glob(...)` → tìm **tất cả file khớp**. Ví dụ trả về:
   ```python
   ["/home/.../markdown_docs/book.md", "/home/.../markdown_docs/article.md"]
   ```
3. `sorted(...)` → **sắp xếp theo bảng chữ cái** để kết quả ổn định (chạy lần nào cũng cùng thứ tự).
4. `for doc_path_str in ...:` → **lặp** qua từng đường dẫn.

**`doc_path = Path(doc_path_str)`**
- Chuyển chuỗi đường dẫn thành object `Path` (có nhiều hàm tiện lợi như `.stem`, `.name`).

**`parent_chunks, child_chunks = self.create_chunks_single(doc_path)`**
- Gọi hàm chunk **một file** (giải thích phía dưới). Hàm này trả về **2 list** → ta nhận vào 2 biến.

**`all_parent_chunks.extend(parent_chunks)`**
- `extend` = **thêm tất cả phần tử** của list `parent_chunks` vào list `all_parent_chunks`.
- Khác với `append` (chỉ thêm 1 phần tử):
  - `[1,2].append([3,4])` → `[1, 2, [3, 4]]` (list lồng list ❌).
  - `[1,2].extend([3,4])` → `[1, 2, 3, 4]` ✅.

**`return all_parent_chunks, all_child_chunks`**
- Trả về **2 list** cho người gọi.

### Ví dụ chạy thực tế

Giả sử thư mục có 2 file:
- `book.md` → cho ra 5 parent, 20 child.
- `article.md` → cho ra 3 parent, 12 child.

Kết quả: `(8 parent, 32 child)`.

---

## 6. Hàm `create_chunks_single` — "Xử Lý 1 File"

```python
def create_chunks_single(self, md_path):
    doc_path = Path(md_path)

    with open(doc_path, 'r', encoding='utf-8') as f:
        parent_chunks = self.__parent_splitter.split_text(f.read())

    merged_parents = self.__merge_small_parents(parent_chunks)
    split_parents = self.__split_large_parents(merged_parents)
    cleaned_parents = self.__clean_small_chunks(split_parents)

    all_parent_chunks, all_child_chunks = [], []
    self.__create_child_chunks(all_parent_chunks, all_child_chunks, cleaned_parents, doc_path)
    return all_parent_chunks, all_child_chunks
```

### Đây là **bộ não** của class. Pipeline gồm 5 bước:

```
File .md
   ↓ (1) Cắt theo header  → parent_chunks (có thể quá ngắn hoặc quá dài)
   ↓ (2) Gộp các chunk quá ngắn  → merged_parents
   ↓ (3) Cắt các chunk quá dài  → split_parents
   ↓ (4) Dọn dẹp những chunk vẫn còn ngắn lẻ  → cleaned_parents
   ↓ (5) Sinh child chunks từ mỗi parent  → all_child_chunks
```

### Giải thích từng dòng

**`with open(doc_path, 'r', encoding='utf-8') as f:`**
- Mở file ở chế độ đọc (`'r'` = read), encoding UTF-8 (để đọc được tiếng Việt, ký tự đặc biệt).
- `with ... as f:` = "context manager" — tự đóng file khi xong (tránh rò rỉ tài nguyên).

**`parent_chunks = self.__parent_splitter.split_text(f.read())`**
- `f.read()` → đọc **toàn bộ nội dung** file thành 1 chuỗi.
- `__parent_splitter.split_text(...)` → cắt theo header. Trả về list các **Document object**, mỗi cái có:
  - `.page_content` (chuỗi nội dung)
  - `.metadata` (dict chứa tiêu đề, ví dụ `{"H1": "Chương 1", "H2": "Phần 1.1"}`)

**Ví dụ minh họa cắt header:**

Input markdown:
```markdown
# Chương 1
Nội dung mở đầu.
## Phần 1.1
Chi tiết phần này.
## Phần 1.2
Chi tiết khác.
```

Sau `split_text`:
```python
[
  Document(page_content="# Chương 1\nNội dung mở đầu.", metadata={"H1": "Chương 1"}),
  Document(page_content="## Phần 1.1\nChi tiết phần này.", metadata={"H1": "Chương 1", "H2": "Phần 1.1"}),
  Document(page_content="## Phần 1.2\nChi tiết khác.", metadata={"H1": "Chương 1", "H2": "Phần 1.2"}),
]
```

**3 dòng pipeline tiếp theo** — gọi 3 hàm nội bộ (giải thích bên dưới).

**`all_parent_chunks, all_child_chunks = [], []`**
- Tạo 2 list rỗng.

**`self.__create_child_chunks(all_parent_chunks, all_child_chunks, cleaned_parents, doc_path)`**
- Hàm này **không return** mà **sửa trực tiếp** 2 list trên (gọi là "in-place modification"). Đây là quy ước Python: list truyền vào hàm có thể bị sửa đổi.

**`return all_parent_chunks, all_child_chunks`** — trả về kết quả cuối.

---

## 7. Hàm `__merge_small_parents` — "Gộp Chunk Quá Ngắn"

```python
def __merge_small_parents(self, chunks):
    if not chunks:
        return []

    merged, current = [], None
    for chunk in chunks:
        if current is None:
            current = chunk
        else:
            current.page_content += "\n\n" + chunk.page_content
            for k, v in chunk.metadata.items():
                if k in current.metadata:
                    current.metadata[k] = f"{current.metadata[k]} -> {v}"
                else:
                    current.metadata[k] = v
        if len(current.page_content) >= self.__min_parent_size:
            merged.append(current)
            current = None
    
    if current:
        if merged:
            merged[-1].page_content += "\n\n" + current.page_content
            for k, v in current.metadata.items():
                if k in merged[-1].metadata:
                    merged[-1].metadata[k] = f"{merged[-1].metadata[k]} -> {v}"
                else:
                    merged[-1].metadata[k] = v
        else:
            merged.append(current)
    
    return merged
```

### Vấn đề cần giải quyết
Sau khi cắt theo header, có những đoạn rất ngắn (vài câu thôi). Đưa vào RAG sẽ kém hiệu quả. → **Gộp các chunk ngắn lại** cho đủ `MIN_PARENT_SIZE` (2000 ký tự).

### Giải thích từng dòng

**`if not chunks: return []`**
- Nếu input rỗng → trả về list rỗng. **Early return** để tránh crash ở các bước sau.

**`merged, current = [], None`**
- `merged` = list kết quả cuối.
- `current` = "bộ đệm" đang gom các chunk nhỏ. Ban đầu chưa có gì → `None`.

**Vòng lặp `for chunk in chunks:`** — duyệt từng chunk:

**`if current is None: current = chunk`**
- Bộ đệm trống → lấy chunk này làm "hạt giống".

**`else:` (đã có bộ đệm) → cộng chunk này vào bộ đệm:**

```python
current.page_content += "\n\n" + chunk.page_content
```
- `+=` = thêm vào cuối. `\n\n` = 2 dòng trống ngăn cách (đẹp khi hiển thị).

```python
for k, v in chunk.metadata.items():
    if k in current.metadata:
        current.metadata[k] = f"{current.metadata[k]} -> {v}"
    else:
        current.metadata[k] = v
```
- Gộp **metadata** (dict các tiêu đề). Nếu key trùng → nối bằng `" -> "`. Ví dụ:
  - `current.metadata = {"H2": "Phần 1.1"}`
  - `chunk.metadata = {"H2": "Phần 1.2"}`
  - Sau gộp: `{"H2": "Phần 1.1 -> Phần 1.2"}` (cho biết chunk này gồm cả 2 phần).

**`if len(current.page_content) >= self.__min_parent_size:`**
- Khi bộ đệm đã đủ dài (≥ 2000 ký tự) → "chốt" nó vào kết quả, reset bộ đệm.

```python
merged.append(current)
current = None
```

**Xử lý phần dư sau vòng lặp:**

```python
if current:
    if merged:
        merged[-1].page_content += "\n\n" + current.page_content
        ...
    else:
        merged.append(current)
```
- Nếu hết vòng lặp mà bộ đệm `current` vẫn còn (chưa đủ dài):
  - **Nếu đã có chunk trong `merged`** → **gắn vào chunk cuối cùng** (`merged[-1]`, dấu `-1` = phần tử cuối).
  - **Nếu `merged` rỗng** (cả file ngắn hơn 2000) → cứ thêm vào.

### Ví dụ chạy

Input: 5 chunk với độ dài lần lượt `[800, 700, 600, 1500, 300]`, `MIN_PARENT_SIZE = 2000`.

| Bước | `current` | `len(current)` | Hành động |
|------|-----------|----------------|-----------|
| 1 | chunk[0] (800) | 800 | Chưa đủ, giữ lại |
| 2 | chunk[0]+chunk[1] | 1500 | Chưa đủ, gộp tiếp |
| 3 | +chunk[2] | 2100 | Đủ rồi! → `merged.append`, reset |
| 4 | chunk[3] (1500) | 1500 | Chưa đủ, giữ lại |
| 5 | +chunk[4] | 1800 | Vẫn chưa đủ |

Sau vòng lặp: `current` còn 1800 ký tự → gắn vào `merged[-1]`.

Kết quả: 1 chunk duy nhất chứa toàn bộ.

---

## 8. Hàm `__split_large_parents` — "Cắt Chunk Quá Dài"

```python
def __split_large_parents(self, chunks):
    split_chunks = []

    for chunk in chunks:
        if len(chunk.page_content) <= self.__max_parent_size:
            split_chunks.append(chunk)
        else:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size = self.__max_parent_size,
                chunk_overlap = config.CHILD_CHUNK_OVERLAP
            )
            sub_chunks = splitter.split_documents([chunk])
            split_chunks.extend(sub_chunks)
    
    return split_chunks
```

### Mục đích
Sau bước gộp, có thể có chunk **quá dài** (vd: 8000 ký tự). Phải cắt nhỏ về `MAX_PARENT_SIZE` (4000).

### Giải thích từng dòng

**`for chunk in chunks:`** — duyệt từng parent.

**`if len(chunk.page_content) <= self.__max_parent_size:`**
- Nếu ngắn hơn 4000 → giữ nguyên (`append`).

**`else:` (quá dài) → cắt nhỏ:**

```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size = self.__max_parent_size,
    chunk_overlap = config.CHILD_CHUNK_OVERLAP
)
```
- Tạo một splitter mới cắt theo độ dài 4000 ký tự, overlap 100.

> 💡 **Lưu ý hiệu năng:** Splitter được tạo lại bên trong vòng lặp — đây là điểm có thể tối ưu (đưa ra ngoài vòng lặp). Nhưng vì chỉ chạy 1 lần khi index, không quan trọng lắm.

```python
sub_chunks = splitter.split_documents([chunk])
```
- `[chunk]` = bọc chunk vào list (vì `split_documents` nhận list).
- Cắt chunk thành nhiều sub-chunk (giữ nguyên metadata).

```python
split_chunks.extend(sub_chunks)
```
- Thêm tất cả sub-chunk vào kết quả.

### Ví dụ chạy

Input: 3 chunk độ dài `[3000, 8500, 2500]`, `MAX = 4000`.

- chunk[0] (3000) → giữ nguyên.
- chunk[1] (8500) → cắt thành ~3 sub-chunk (8500/4000 ≈ 2.1, cộng overlap nên thường 3).
- chunk[2] (2500) → giữ nguyên.

Kết quả: 5 chunk.

---

## 9. Hàm `__clean_small_chunks` — "Dọn Dẹp Chunk Lẻ"

```python
def __clean_small_chunks(self, chunks):
    cleaned = []

    for i, chunk in enumerate(chunks):
        if len(chunk.page_content) < self.__min_parent_size:
            if cleaned:
                cleaned[-1].page_content += "\n\n" + chunk.page_content
                for k, v in chunk.metadata.items():
                    if k in cleaned[-1].metadata:
                        cleaned[-1].metadata[k] = f"{cleaned[-1].metadata[k]} -> {v}"
                    else:
                        cleaned[-1].metadata[k] = v
            elif i < len(chunks) - 1:
                chunks[i+1].page_content = chunk.page_content + "\n\n" + chunks[i+1].page_content
                for k,v in chunk.metadata.items():
                    if k in chunks[i + 1].metadata:
                        chunks[i+1].metadata[k] = f"{v} -> {chunks[i+1].metadata[k]}"
                    else:
                        chunks[i+1].metadata[k] = v
            else:
                cleaned.append(chunk)
        else:
            cleaned.append(chunk)
    
    return cleaned
```

### Vấn đề
Sau khi cắt chunk dài bằng `__split_large_parents`, **sub-chunk cuối** có thể bị ngắn (vd: 8500 ký tự → 4000 + 4000 + 500, cái 500 quá ngắn). Cần dọn dẹp.

### Giải thích từng dòng

**`for i, chunk in enumerate(chunks):`**
- `enumerate` cho cả **index `i`** và **giá trị `chunk`** cùng lúc. Tương đương:
  ```python
  for i in range(len(chunks)):
      chunk = chunks[i]
  ```

**`if len(chunk.page_content) < self.__min_parent_size:` (chunk này quá ngắn)**

**Trường hợp 1: `if cleaned:` (đã có chunk được clean)**
- Gắn chunk ngắn này **vào cuối chunk đã clean trước đó**. Tương tự logic gộp metadata.

**Trường hợp 2: `elif i < len(chunks) - 1:` (chưa có chunk clean, và còn chunk sau)**
- Đây là **chunk đầu tiên** mà lại ngắn → không có chỗ "lùi về sau" → **đẩy về phía trước**, gắn vào chunk kế tiếp.
- Lưu ý cách metadata được nối: `f"{v} -> {chunks[i+1].metadata[k]}"` — chunk hiện tại đứng **trước** (vì nó bị nối vào đầu chunk sau).

**Trường hợp 3: `else:` (chỉ có 1 chunk duy nhất trong cả file, và nó ngắn)**
- Đành chấp nhận, `append` vào kết quả.

**`else:` (chunk đủ dài) → `cleaned.append(chunk)`**

### Ví dụ chạy

Input độ dài `[500, 3000, 2500, 300]`, `MIN = 2000`.

| `i` | chunk | dài? | Hành động | `cleaned` sau bước |
|-----|-------|------|-----------|---------------------|
| 0 | 500 | ngắn | `cleaned` rỗng + còn chunk sau → đẩy về chunks[1] | `[]` (chunks[1] thành 500+3000=3500) |
| 1 | 3500 | đủ | `append` | `[3500]` |
| 2 | 2500 | đủ | `append` | `[3500, 2500]` |
| 3 | 300 | ngắn | `cleaned` có → gắn vào cuối `cleaned[-1]` | `[3500, 2800]` |

---

## 10. Hàm `__create_child_chunks` — "Sinh Chunk Con"

```python
def __create_child_chunks(self, all_parent_pairs, all_child_chunks, parent_chunks, doc_path):
    for i, p_chunk in enumerate(parent_chunks):
        parent_id = f"{doc_path.stem}_parent_{i}"
        p_chunk.metadata.update({"source": str(doc_path.stem)+".pdf", "parent_id": parent_id})

        all_parent_pairs.append((parent_id, p_chunk))
        all_child_chunks.extend(self.__child_splitter.split_documents([p_chunk]))
```

### Mục đích
Với mỗi parent, tạo **ID duy nhất** rồi cắt nó thành nhiều child. Mỗi child sẽ **nhớ parent ID** (qua metadata) — để sau này khi tìm thấy child trong vector DB, hệ thống biết lấy parent nào.

### Giải thích từng dòng

**`for i, p_chunk in enumerate(parent_chunks):`** — duyệt từng parent kèm index.

**`parent_id = f"{doc_path.stem}_parent_{i}"`**
- `doc_path.stem` = tên file không có đuôi. Ví dụ `Path("book.md").stem` = `"book"`.
- `f"..."` = **f-string** — chèn biến vào chuỗi.
- Ví dụ: `parent_id = "book_parent_0"`.

**`p_chunk.metadata.update({"source": ..., "parent_id": parent_id})`**
- `update` = thêm/cập nhật key-value vào dict.
- Sau dòng này metadata trở thành ví dụ:
  ```python
  {"H1": "Chương 1", "H2": "Phần 1.1", "source": "book.pdf", "parent_id": "book_parent_0"}
  ```
- Lưu ý: tác giả gắn đuôi `.pdf` vì file gốc là PDF (file `.md` được convert từ PDF — xem commit message `convert pdf to md file`).

**`all_parent_pairs.append((parent_id, p_chunk))`**
- Thêm **tuple** `(id, document)` vào list. Tuple = giống list nhưng không sửa được.
- Cấu trúc này tiện cho **bộ nhớ key-value** sau này (vd: dùng `dict(all_parent_pairs)` để tra parent theo ID).

**`all_child_chunks.extend(self.__child_splitter.split_documents([p_chunk]))`**
- Dùng `__child_splitter` (cắt 500 ký tự, overlap 100) để cắt parent thành nhiều child.
- `split_documents` **tự copy metadata của parent sang mọi child** → child cũng có `parent_id` → tra ngược được.

### Ví dụ chạy

Parent: 1 chunk dài 3500 ký tự, `parent_id = "book_parent_0"`.

Sau `split_documents`:
```python
[
  Document(page_content="...500 ký tự đầu...", metadata={..., "parent_id": "book_parent_0"}),
  Document(page_content="...400-900...", metadata={..., "parent_id": "book_parent_0"}),
  ...
  # ~8 child
]
```

Mỗi child mang `parent_id` = `"book_parent_0"` → biết nó thuộc parent nào.

---

## 11. Toàn Bộ Pipeline Khi Chạy Thực Tế

Giả sử ta chạy:

```python
chunker = DocumentChuncker()
parents, children = chunker.create_chunks()
```

### Bước 1: `__init__`
- Tạo 2 splitter, lưu 2 hằng số kích thước.

### Bước 2: `create_chunks` quét thư mục
- Tìm thấy `book.md`.

### Bước 3: `create_chunks_single("book.md")`

3.1. **Đọc file** → chuỗi 20000 ký tự.

3.2. **`__parent_splitter.split_text`** → cắt theo header:
```
[chunk0 (1200), chunk1 (800), chunk2 (3500), chunk3 (5000), chunk4 (400)]
```

3.3. **`__merge_small_parents`** (gộp các chunk < 2000):
- chunk0+chunk1 = 2000 ✅ → chốt
- chunk2 (3500) ✅ → chốt
- chunk3 (5000) ✅ → chốt
- chunk4 (400) dư → gắn vào cuối chunk3 → chunk3 thành 5400
```
[2000, 3500, 5400]
```

3.4. **`__split_large_parents`** (cắt > 4000):
- 2000 → giữ
- 3500 → giữ
- 5400 → cắt thành 2 sub (~3000 + 2400)
```
[2000, 3500, 3000, 2400]
```

3.5. **`__clean_small_chunks`** (dọn < 2000):
- Tất cả ≥ 2000 → không đổi.

3.6. **`__create_child_chunks`**:
- Parent 0 (2000 ký tự) → ~5 child, `parent_id = "book_parent_0"`.
- Parent 1 (3500) → ~8 child, `parent_id = "book_parent_1"`.
- Parent 2 (3000) → ~7 child.
- Parent 3 (2400) → ~5 child.

**Kết quả cuối:**
- `parents` = 4 cặp `(id, Document)`.
- `children` = ~25 Document, mỗi cái biết `parent_id` của nó.

---

## 12. Vì Sao Thiết Kế Như Vậy?

| Quyết định thiết kế | Lý do |
|---|---|
| Cắt theo header trước | Giữ ngữ nghĩa "trọn một mục" thay vì cắt giữa câu. |
| Gộp chunk ngắn | Tránh chunk vô nghĩa (vd: chỉ có cái tiêu đề). |
| Cắt chunk quá dài | Tránh vượt giới hạn context của LLM. |
| Dọn dẹp lần cuối | Vì sau khi cắt vẫn có thể còn chunk lẻ. |
| Parent–Child tách bạch | Tìm bằng child (chính xác), trả về parent (đủ context). |
| Dùng `__` ở đầu tên | Đánh dấu "nội bộ, đừng đụng vào". |
| Lưu `parent_id` trong metadata của child | Để truy ngược parent khi LLM cần đọc context đầy đủ. |

---

## 13. Sơ Đồ Tóm Tắt

```
                    ┌──────────────────┐
                    │   File .md       │
                    └────────┬─────────┘
                             ↓
                  MarkdownHeaderTextSplitter
                  (cắt theo #, ##, ###)
                             ↓
              ┌──────────────────────────┐
              │  parent_chunks (lộn xộn) │
              └──────────────┬───────────┘
                             ↓
                  __merge_small_parents
                  (gộp chunk < 2000)
                             ↓
                  __split_large_parents
                  (cắt chunk > 4000)
                             ↓
                  __clean_small_chunks
                  (dọn chunk lẻ còn sót)
                             ↓
              ┌──────────────────────────┐
              │  cleaned parents (2000-  │
              │  4000 ký tự, ổn định)    │
              └──────────────┬───────────┘
                             ↓
                  __create_child_chunks
                  (gắn parent_id + cắt 500)
                             ↓
              ┌──────────────────────────┐
              │  parents + children      │
              │  (sẵn sàng cho vector DB)│
              └──────────────────────────┘
```

---

## 14. Một Số Thuật Ngữ Python Đã Gặp

| Thuật ngữ | Giải thích đơn giản |
|---|---|
| `class` | Bản thiết kế để tạo object. |
| `__init__` | Hàm chạy tự động khi tạo object. |
| `self` | "Bản thân object đang xét" — phải có trong mọi method. |
| `__name` (2 gạch dưới) | Quy ước "biến/hàm nội bộ". |
| `list` (`[]`) | Mảng có thứ tự, sửa được. |
| `dict` (`{}`) | Cặp key-value (giống danh bạ). |
| `tuple` (`()`) | Như list nhưng **không sửa được**. |
| `append` vs `extend` | `append` thêm 1 phần tử, `extend` thêm nhiều (từ list khác). |
| `enumerate` | Lặp kèm index. |
| f-string (`f"..."`) | Chèn biến vào chuỗi. |
| `with open(...) as f:` | Mở file an toàn (tự đóng khi xong). |
| `for ... in ...:` | Vòng lặp duyệt từng phần tử. |
| `if/elif/else` | Rẽ nhánh điều kiện. |
| `return` | Trả kết quả cho người gọi. |

---

## 15. Kết Luận

File `document_chunker.py` là **bộ tiền xử lý tài liệu** cho hệ thống RAG. Nó biến file Markdown thô thành 2 tập chunk có cấu trúc:
- **Parent**: dài, giàu ngữ cảnh, lưu riêng để khi cần đọc.
- **Child**: ngắn, dễ tìm chính xác, có "link" về parent qua `parent_id`.

Toàn bộ logic xoay quanh việc **giữ chunk trong khoảng 2000–4000 ký tự** (cho parent) và **500 ký tự** (cho child), thông qua 3 thao tác chính: **gộp ngắn**, **cắt dài**, **dọn lẻ**.
