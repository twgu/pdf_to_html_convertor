import test_settings
import pdfplumber
import fitz
import os
import shutil

# 작업 폴더 초기화
shutil.rmtree(test_settings.WORKING_FOLDER, ignore_errors=True)
os.makedirs(test_settings.CONVERSION_SAVE_FOLDER, exist_ok=True)

# pdfplumber 라이브러리로 PDF File Open
with pdfplumber.open(test_settings.FILE_FULL_NAME) as pdf:
    # fitz 라이브러리로 PDF File Open
    with fitz.open(test_settings.FILE_FULL_NAME) as fitz_pdf:
        for page in pdf.pages:
            fitz_page = fitz_pdf[page.page_number - 1]  # 1 page = 0
            for idx, image in enumerate(page.images):
                if image.get('width', 0) < test_settings.IMAGE_MIN_WIDTH \
                        or image.get('height', 0) < test_settings.IMAGE_MIN_HEIGHT:
                    continue

                # 영역 캡쳐
                pix = fitz_page.get_pixmap(
                    matrix=fitz.Matrix(2.5, 2.5),  # 이미지 해상도를 2.5배 증가시켜 선명하게 캡쳐 (180 DPI)
                    alpha=False,  # 이미지를 불투명한 RGB 포멧으로 저장
                    clip=fitz.Rect(
                        image.get('x0'), image.get('top'), image.get('x1'), image.get('bottom')
                    )
                )

                # 캡쳐본 저장
                save_name = str(page.page_number) + ' page image ' + str(idx + 1) + '.png'
                pix.save(f'{os.path.normpath(os.path.join(test_settings.CONVERSION_SAVE_FOLDER, save_name))}')
