import test_settings
import pdfplumber

contents = []

# pdfplumber 라이브러리로 PDF File Open
with pdfplumber.open(test_settings.FILE_FULL_NAME) as pdf:
    for page in pdf.pages:
        contents.append(test_settings.page_start_line(page.page_number))

        tables = page.find_tables()
        for idx, table in enumerate(tables):
            contents.append(f'    ┌───────── table {idx + 1} ─────────┐')
            for row in table.extract():
                contents.append(str(row))
            contents.append(f'    └───────── table {idx + 1} ─────────┘')

        contents.append(test_settings.page_end_line(page.page_number))

# 결과 출력
print('\n'.join(contents))
