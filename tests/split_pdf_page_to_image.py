import test_settings
import os
import shutil
import fitz

# 분할 하고싶은 page
target_page = 18

# 작업 폴더 초기화
shutil.rmtree(test_settings.WORKING_FOLDER, ignore_errors=True)
os.makedirs(test_settings.CONVERSION_SAVE_FOLDER, exist_ok=True)

# fitz 라이브러리로 PDF File Open
with fitz.open(test_settings.FILE_FULL_NAME) as fitz_pdf:
    fitz_page = fitz_pdf[target_page - 1]  # 1 page = 0

    # 페이지 캡쳐
    pix = fitz_page.get_pixmap(
        matrix=fitz.Matrix(2.5, 2.5),  # 이미지 해상도를 2.5배 증가시켜 선명하게 캡쳐 (180 DPI)
        alpha=False  # 이미지를 불투명한 RGB 포멧으로 저장
    )

    # 캡쳐본 저장
    save_name = str(target_page) + ' page.png'
    pix.save(os.path.normpath(os.path.join(test_settings.CONVERSION_SAVE_FOLDER, save_name)))
