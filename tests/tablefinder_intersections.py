import test_settings
import pdfplumber
from pdfplumber.table import TableFinder

# 추출 하고싶은 page
target_page = 2

result = ['intersections = [']

# pdfplumber 라이브러리로 PDF File Open
with pdfplumber.open(test_settings.FILE_FULL_NAME) as pdf:
    page = pdf.pages[target_page - 1]  # 1 page = 0

    for idx, intersection in enumerate(TableFinder(page).intersections):
        result.append(
            ('{' if idx == 0 else ', {')
            + f'"no": {idx + 1}'
            + f', "x": {intersection[0]}'
            + f', "y": {intersection[1]}'
            + '}'
        )

result.append(']')

# 결과 출력
print('\n'.join(result))
