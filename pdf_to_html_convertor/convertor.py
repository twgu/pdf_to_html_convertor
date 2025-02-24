import os
import shutil

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List

import pdfplumber
import fitz
from PyPDF2 import PdfWriter, PdfReader

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

import html_format


def print_end_message(stime: datetime):
    etime = datetime.now()
    duration = (etime - stime).total_seconds()
    print(f'>>>> [{etime}] 변환종료')
    print(f'>>>> [{etime}] 소요시간: {duration}초')


@dataclass
class ConversionSettings:
    # File
    file_full_name: str
    file_path: str = field(init=False)
    file_name: str = field(init=False)
    file_extension: str = field(init=False)

    # Working Folder
    working_folder: str = field(init=False)
    conversion_save_folder: str = field(init=False)

    # Azure Document Intelligence
    azure_di_endpoint_url: str = field(default='')
    azure_di_api_key: str = field(default='')

    # Image min size
    image_min_width: int = field(default=15)
    image_min_height: int = field(default=15)

    def __post_init__(self):
        self.file_full_name = os.path.normpath(self.file_full_name)
        self.file_path = os.path.dirname(self.file_full_name)
        self.file_name, self.file_extension = os.path.splitext(os.path.basename(self.file_full_name))
        self.file_extension = self.file_extension.lower()
        self.working_folder: str = os.path.normpath(os.path.join(self.file_path, self.file_name))
        self.conversion_save_folder: str = os.path.normpath(os.path.join(self.working_folder, 'conversion'))


class Conversion:
    def __init__(self, file_full_name: str):
        self.settings = ConversionSettings(file_full_name)

    def initialize(self) -> bool:
        if self.settings.file_extension != '.pdf':
            print(f'>>>> [{datetime.now()}] 파일 확장자 오류')
            return False

        try:
            shutil.rmtree(self.settings.working_folder, ignore_errors=True)
            os.makedirs(self.settings.conversion_save_folder, exist_ok=True)
        except Exception as e:
            print(f'>>>> [{datetime.now()}] 작업 폴더 초기화 중 오류 발생:')
            print(f'{e}')
            return False

        return True

    def extract_text_contents(self) -> List[Dict[str, Any]]:
        print(f'>>>> [{datetime.now()}] <텍스트 추출 시작>')

        contents = []

        with pdfplumber.open(self.settings.file_full_name) as pdf:
            for page in pdf.pages:
                item = {
                    'page_number': page.page_number,
                    'item_bbox': None,
                    'item_type': 'text',
                    'item_data': '',
                    'table_row_count': None,
                    'di_page_wratio': None,
                    'di_page_hratio': None
                }

                words = page.extract_words()
                for word in words:
                    word_text = word.get('text')
                    word_x0, word_y0 = word.get('x0'), word.get('top')
                    word_x1, word_y1 = word.get('x1'), word.get('bottom')

                    if item.get('item_bbox'):
                        if abs(word_y0 - item.get('item_bbox')[1]) <= 5:
                            item['item_data'] += ' ' + word_text
                            item['item_bbox'][2] = max(item.get('item_bbox')[2], word_x1)
                            item['item_bbox'][3] = max(item.get('item_bbox')[3], word_y1)
                        else:
                            contents.append(item)
                            item = {
                                'page_number': page.page_number,
                                'item_bbox': [word_x0, word_y0, word_x1, word_y1],
                                'item_type': 'text',
                                'item_data': word_text,
                                'table_row_count': None,
                                'di_page_wratio': None,
                                'di_page_hratio': None
                            }
                    else:
                        item = {
                            'page_number': page.page_number,
                            'item_bbox': [word_x0, word_y0, word_x1, word_y1],
                            'item_type': 'text',
                            'item_data': word_text,
                            'table_row_count': None,
                            'di_page_wratio': None,
                            'di_page_hratio': None
                        }

                if item.get('item_data'):
                    contents.append(item)

        print(f'>>>> [{datetime.now()}] <텍스트 추출 종료>')

        return contents

    def extract_table_contents(self) -> List[Dict[str, Any]]:
        print(f'>>>> [{datetime.now()}] <테이블 추출 시작>')

        contents = []

        with pdfplumber.open(self.settings.file_full_name) as pdf:
            in_pdf = False
            for page in pdf.pages:
                if page.find_tables():
                    in_pdf = True
                    break

            if not in_pdf:
                print(f'>>>> [{datetime.now()}] 발견된 테이블 없음')
                print(f'>>>> [{datetime.now()}] <테이블 추출 종료>')
                return contents

            page_matching = []
            pypdf2_page = 0

            with open(self.settings.file_full_name, 'rb') as rb_file:
                pypdf2_reader = PdfReader(rb_file)
                pypdf2_writer = PdfWriter()

                for page in pdf.pages:
                    if page.find_tables():
                        print(f'>>>> [{datetime.now()}] {page.page_number} 페이지 테이블 발견')
                        pypdf2_page += 1
                        page_matching.append({
                            'pypdf2_page': pypdf2_page,
                            'page': page.page_number,
                            'width': page.width,
                            'height': page.height
                        })
                        pypdf2_writer.add_page(pypdf2_reader.pages[page.page_number - 1])

                save_name = 'table.pdf'
                with open(
                        os.path.normpath(os.path.join(self.settings.conversion_save_folder, save_name)),
                        'wb'
                ) as wb_file:
                    pypdf2_writer.write(wb_file)

        print(f'>>>> [{datetime.now()}] <테이블 추출 종료>')

        print(f'>>>> [{datetime.now()}] <Azure Document Intelligence 분석 시작>')

        azure_di_client = DocumentAnalysisClient(
            self.settings.azure_di_endpoint_url,
            AzureKeyCredential(self.settings.azure_di_api_key)
        )

        with open(
                os.path.normpath(os.path.join(self.settings.conversion_save_folder, save_name)),
                'rb'
        ) as rb_file:
            azure_di_poller = azure_di_client.begin_analyze_document('prebuilt-layout', rb_file)
            azure_di_result = azure_di_poller.result()

            for di_table in azure_di_result.tables:
                di_table_page_number = di_table.bounding_regions[0].page_number
                di_table_polygon = di_table.bounding_regions[0].polygon

                page_number = next(
                    (item for item in page_matching if item['pypdf2_page'] == di_table_page_number),
                    None
                ).get('page')
                page_width = next(
                    (item for item in page_matching if item['pypdf2_page'] == di_table_page_number),
                    None
                ).get('width')
                page_height = next(
                    (item for item in page_matching if item['pypdf2_page'] == di_table_page_number),
                    None
                ).get('height')
                di_page_width = azure_di_result.pages[di_table_page_number - 1].width
                di_page_height = azure_di_result.pages[di_table_page_number - 1].height
                di_page_wratio = round(page_width / di_page_width, 4)
                di_page_hratio = round(page_height / di_page_height, 4)

                item = {
                    'page_number': page_number,
                    'item_bbox': [
                        min(point.x for point in di_table_polygon) * di_page_wratio,
                        min(point.y for point in di_table_polygon) * di_page_hratio,
                        max(point.x for point in di_table_polygon) * di_page_wratio,
                        max(point.y for point in di_table_polygon) * di_page_hratio
                    ],
                    'item_type': 'table',
                    'item_data': di_table.cells,
                    'table_row_count': di_table.row_count,
                    'di_page_wratio': di_page_wratio,
                    'di_page_hratio': di_page_hratio
                }

                contents.append(item)

        print(f'>>>> [{datetime.now()}] <Azure Document Intelligence 분석 종료>')

        return contents

    def extract_image_contents(self) -> List[Dict[str, Any]]:
        print(f'>>>> [{datetime.now()}] <이미지 추출 시작>')

        contents = []

        with pdfplumber.open(self.settings.file_full_name) as pdf:
            with fitz.open(self.settings.file_full_name) as fitz_pdf:
                for page in pdf.pages:
                    fitz_page = fitz_pdf[page.page_number - 1]
                    for idx, image in enumerate(page.images):
                        if image.get('width', 0) < self.settings.image_min_width \
                                or image.get('height', 0) < self.settings.image_min_height:
                            continue

                        print(f'>>>> [{datetime.now()}] {page.page_number} 페이지 이미지 발견 {idx + 1}')

                        image_x0, image_y0 = image.get('x0'), image.get('top')
                        image_x1, image_y1 = image.get('x1'), image.get('bottom')

                        pix = fitz_page.get_pixmap(
                            matrix=fitz.Matrix(2.5, 2.5),
                            alpha=False,
                            clip=fitz.Rect(image_x0, image_y0, image_x1, image_y1)
                        )

                        save_name = str(page.page_number) + ' page image ' + str(idx + 1) + '.png'
                        pix.save(f'{os.path.normpath(os.path.join(self.settings.conversion_save_folder, save_name))}')

                        item = {
                            'page_number': page.page_number,
                            'item_bbox': [image_x0, image_y0, image_x1, image_y1],
                            'item_type': 'image',
                            'item_data': os.path.normpath(
                                os.path.join(self.settings.conversion_save_folder, save_name)
                            ),
                            'table_row_count': None,
                            'di_page_wratio': None,
                            'di_page_hratio': None
                        }

                        contents.append(item)

        if not contents:
            print(f'>>>> [{datetime.now()}] 발견된 이미지 없음')
        else:
            print(f'>>>> [{datetime.now()}] 총 {len(contents)}개 이미지 발견')

        print(f'>>>> [{datetime.now()}] <이미지 추출 종료>')

        return contents

    def to_html(self, contents: List[Dict[str, Any]]):
        print(f'>>>> [{datetime.now()}] <HTML 변환 시작>')

        sorted_contents = sorted(
            contents,
            key=lambda sitem: (sitem.get('page_number'), sitem.get('item_bbox')[1])
        )

        html_text = html_format.header()

        now_page = 0
        for item in sorted_contents:
            page_number = item.get('page_number')
            item_bbox = item.get('item_bbox')
            item_type = item.get('item_type')
            item_data = item.get('item_data')
            di_page_wratio = item.get('di_page_wratio')
            di_page_hratio = item.get('di_page_hratio')

            table_contents = [
                titem for titem in sorted_contents if titem.get('page_number') == page_number \
                                                      and titem.get('item_type') == 'table'
            ]
            image_contents = [
                iitem for iitem in sorted_contents if iitem.get('page_number') == page_number \
                                                      and iitem.get('item_type') == 'image'
            ]

            if page_number != now_page:
                if now_page != 0:
                    html_text.extend(html_format.page_end_line(now_page))
                html_text.extend(html_format.page_start_line(page_number))
                now_page = page_number

            in_table = False
            if item_type == 'text' or item_type == 'image':
                for titem in table_contents:
                    if titem.get('item_bbox')[0] <= item_bbox[0] \
                            and titem.get('item_bbox')[1] <= item_bbox[1] \
                            and titem.get('item_bbox')[2] >= item_bbox[2] \
                            and titem.get('item_bbox')[3] >= item_bbox[3]:
                        in_table = True
                        break

            if in_table:
                continue

            if item_type == 'text':
                html_text.append(f'    <p>{item_data}</p>')
            elif item_type == 'table':
                html_text.append(f'    <table>')
                for idx in range(item.get("table_row_count")):
                    html_text.append(f'        <tr>')

                    table_row_data = [citem for citem in item_data if citem.row_index == idx]

                    for cell_data in table_row_data:
                        cell_polygon = cell_data.bounding_regions[0].polygon

                        cell_x0 = min(point.x for point in cell_polygon) * di_page_wratio
                        cell_y0 = min(point.y for point in cell_polygon) * di_page_hratio
                        cell_x1 = max(point.x for point in cell_polygon) * di_page_wratio
                        cell_y1 = max(point.y for point in cell_polygon) * di_page_hratio

                        html_text.append(
                            f'            <td rowspan={cell_data.row_span} colspan={cell_data.column_span}>'
                        )

                        html_text.append(f'{cell_data.content}')

                        for iitem in image_contents:
                            if cell_x0 <= iitem.get('item_bbox')[0] \
                                    and cell_y0 <= iitem.get('item_bbox')[1] \
                                    and cell_x1 >= iitem.get('item_bbox')[2] \
                                    and cell_y1 >= iitem.get('item_bbox')[3]:
                                html_text.append(f'                <image src="{iitem.get("item_data")}" />')

                        html_text.append(f'            </td>')
                    html_text.append(f'        </tr>')
                html_text.append(f'    </table>')
            elif item_type == 'image':
                html_text.append(f'    <image src="{item_data}" />')

        html_text.extend(html_format.page_end_line(now_page))

        html_text.extend(html_format.footer())

        with open(
                os.path.normpath(
                    os.path.join(self.settings.conversion_save_folder, self.settings.file_name + '.html')
                ),
                'w',
                encoding='utf-8'
        ) as w_file:
            w_file.write('\n'.join(html_text))

        print(f'>>>> [{datetime.now()}] <HTML 변환 종료>')

    def start(self) -> str:
        stime = datetime.now()
        print(f'>>>> [{stime}] 변환시작')
        print(f'>>>> [{stime}] 대상파일: {self.settings.file_full_name}')

        if not self.initialize():
            print_end_message(stime)
            return ''

        contents = []
        contents.extend(self.extract_text_contents())
        contents.extend(self.extract_table_contents())
        contents.extend(self.extract_image_contents())

        self.to_html(contents)

        print_end_message(stime)

        return os.path.join(self.settings.conversion_save_folder, self.settings.file_name + '.html')


# 실행
if __name__ == '__main__':
    conversion = Conversion(
        'C:/Users/gutaewan/Downloads/품질영향평가.pdf'
    )
    conversion.start()
