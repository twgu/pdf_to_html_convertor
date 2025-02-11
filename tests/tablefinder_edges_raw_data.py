import test_settings
import pdfplumber

# 추출 하고싶은 page
target_page = 2

result = ['edges = [']

# pdfplumber 라이브러리로 PDF File Open
with pdfplumber.open(test_settings.FILE_FULL_NAME) as pdf:
    page = pdf.pages[target_page - 1]  # 1 page = 0

    for idx, edge in enumerate(page.edges):
        # 수직선(v), 수평선(h) 구분
        orientation = ('"' + edge.get('orientation') + '"' if edge.get('orientation') is not None else None)

        result.append(
            ('{' if idx == 0 else ', {')
            + f'"no": {idx + 1}'
            + f', "x0": {edge.get("x0")}'
            + f', "y0": {edge.get("top")}'
            + f', "x1": {edge.get("x1")}'
            + f', "y1": {edge.get("bottom")}'
            + f', "width": {edge.get("width")}'
            + f', "height": {edge.get("height")}'
            + f', "orientation": {orientation}'
            + '}'
        )

result.append(']')

# 결과 출력
print('\n'.join(result))
