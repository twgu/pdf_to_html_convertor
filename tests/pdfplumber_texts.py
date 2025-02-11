import test_settings
import pdfplumber

contents = []

# pdfplumber 라이브러리로 PDF File Open
with pdfplumber.open(test_settings.FILE_FULL_NAME) as pdf:
    # contents.append('>>>> 방법 1:')
    # for page in pdf.pages:
    #     contents.append(test_settings.page_start_line(page.page_number))
    #     contents.append(page.extract_text())
    #     contents.append(test_settings.page_end_line(page.page_number))

    contents.append('>>>> 방법 2:')
    for page in pdf.pages:
        contents.append(test_settings.page_start_line(page.page_number))

        text_block = {'text': '', 'bbox': None}

        words = page.extract_words()
        for word in words:
            word_text = word.get('text')
            word_x0, word_y0 = word.get('x0'), word.get('top')
            word_x1, word_y1 = word.get('x1'), word.get('bottom')

            if text_block.get('bbox'):
                if abs(word_y0 - text_block.get('bbox')[1]) <= 5:
                    text_block['text'] += ' ' + word_text
                    text_block['bbox'][2] = max(text_block.get('bbox')[2], word_x1)
                    text_block['bbox'][3] = max(text_block.get('bbox')[3], word_y1)
                else:
                    contents.append(text_block.get('text'))
                    text_block = {'text': word_text, 'bbox': [word_x0, word_y0, word_x1, word_y1]}
            else:
                text_block = {'text': word_text, 'bbox': [word_x0, word_y0, word_x1, word_y1]}

        if text_block.get('text'):
            contents.append(text_block.get('text'))

        contents.append(test_settings.page_end_line(page.page_number))

# 결과 출력
print('\n'.join(contents))
