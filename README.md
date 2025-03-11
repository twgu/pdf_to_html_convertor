# 개요

PDF to HTML convertor

비정형·비구조화된 데이터인 PDF 파일을 AI가 학습할 수 있도록 HTML 파일로 변환하는 기능 수행

# 개발 환경

SDK

- Python (Version: 3.11.5)

    ```bash
    python --version
    ```

Install Libraries

- python-dotenv (Version: 1.0.1)

    ```bash
    pip install python-dotenv
    ```

    ```bash
    pip show python-dotenv
    ```

- pdfplumber (Version: 0.11.5)

    ```bash
    pip install pdfplumber
    ```

    ```bash
    pip show pdfplumber
    ```

- pymupdf

    ```bash
    pip install pymupdf
    ```

    ```bash
    pip show pymupdf
    ```

- PyPDF2

    ```bash
    pip install PyPDF2
    ```

    ```bash
    pip show PyPDF2
    ```

- azure-ai-formrecognizer

    ```bash
    pip install azure-ai-formrecognizer
    ```

    ```bash
    pip show azure-ai-formrecognizer
    ```

- matplotlib

    ```bash
    pip install matplotlib
    ```

    ```bash
    pip show matplotlib
    ```

# Test Playground Guide

Azure Document Intelligence

- `azure_di.py`: Azure Document Intelligence 사용

pdfplumber

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

기타

- `test_settings.py`: 테스트 셋팅

- `split_pdf_page_to_pdf.py`: PDF 파일 페이지 분할 저장 (PDF)

- `split_pdf_page_to_image.py`: PDF 파일 페이지 분할 저장 (IMAGE)

- `os_path_test.py`: os별 파일경로 테스트
