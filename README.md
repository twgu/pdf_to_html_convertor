# 개요

PDF File HTML 변환기

# 개발환경

### Python 3.11.5

```
python --version
```

### Install Libraries

- PDF 파일 데이터 추출

  ```
  pip install pdfplumber
  ```

- PDF 파일 영역 캡쳐

  ```
  pip install pymupdf
  ```

- PDF 파일 분할

  ```
  pip install PyPDF2
  ```

- Azure Document Intelligence

  ```
  pip install azure-ai-formrecognizer
  ```

- 좌표 데이터 시각화

  ```
  pip install matplotlib
  ```

# 실행

1. `/pdf_to_html_convertor` 패키지의 `convertor.py` Open
2. `@dataclass`인 `ConversionSettings`의 `Azure Document Intelligence` 관련 값 세팅
3. 파일 최하단 PDF 파일 세팅
4. 실행

### 결과

PDF 파일과 같은 경로에 PDF 파일명과 같은 폴더가 생성되며 `/conversion` 경로에 결과물이 저장됨

# /tests

### Azure Document Intelligence

- `azure_di.py`: Azure Document Intelligence 사용

### pdfplumber

- `pdfplumber_texts.py`: PDF 파일에서 텍스트 추출 후 출력
- `pdfplumber_tables.py`: PDF 파일에서 테이블 추출 후 출력
- `pdfplumber_images.py`: PDF 파일에서 이미지 추출 후 저장
- 테이블 생성 흐름 디버깅
    + `tablefinder_edges_raw_data.py`: TableFinder edges raw data 추출 후 출력
    + `tablefinder_edges.py`: TableFinder edges 추출 후 출력
    + `tablefinder_intersections.py`: TableFinder intersections 추출 후 출력
    + `tablefinder_cells.py`: TableFinder cells 추출 후 출력
    + (출력된 데이터를 `visualizing_to_...py`에서 시각화)
- visualizing
    + `visualizing_to_edges.py`: edges 시각화
    + `visualizing_to_intersections.py`: intersections 시각화
    + `visualizing_to_cells.py`: cells 시각화

### 기타

- `test_settings.py`: 테스트 셋팅
- `split_pdf_page_to_pdf.py`: PDF 파일 페이지 분할 저장 (PDF)
- `split_pdf_page_to_image.py`: PDF 파일 페이지 분할 저장 (IMAGE)
- `os_path_test.py`: os별 파일경로 테스트
