import test_settings
import os
import shutil
from PyPDF2 import PdfWriter, PdfReader

# 분할 하고싶은 page
target_page = 18

# 작업 폴더 초기화
shutil.rmtree(test_settings.WORKING_FOLDER, ignore_errors=True)
os.makedirs(test_settings.CONVERSION_SAVE_FOLDER, exist_ok=True)

# PDF File Open
with open(test_settings.FILE_FULL_NAME, 'rb') as rb_file:
    # PyPDF2 라이브러리로 PDF 읽기
    pypdf2_reader = PdfReader(rb_file)

    # PyPDF2 라이브러리로 신규 PDF 작성
    pypdf2_writer = PdfWriter()
    pypdf2_writer.add_page(pypdf2_reader.pages[target_page - 1])  # 1 page = 0

    # 신규 작성된 PDF 저장
    save_name = str(target_page) + ' page.pdf'
    with open(
            os.path.normpath(os.path.join(test_settings.CONVERSION_SAVE_FOLDER, save_name)),
            'wb'
    ) as wb_file:
        pypdf2_writer.write(wb_file)
