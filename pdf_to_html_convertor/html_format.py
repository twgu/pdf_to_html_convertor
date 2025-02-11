from typing import List


def header() -> List[str]:
    return [
        '<!DOCTYPE html>',
        '<html lang="en">',
        '<head>',
        '    <meta charset="UTF-8">',
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '    <title>PDF to HTML</title>',
        '    <style>',
        '        table {',
        '            width: 50%;',
        '            border-collapse: collapse;',
        '            margin: 10px 0;',
        '        }',
        '        th, td {',
        '            border: 1px solid #ddd;',
        '            padding: 8px;',
        '            text-align: left;',
        '        }',
        '        th {',
        '            background-color: #f4f4f4;',
        '        }',
        '        p {',
        '            text-align: left;',
        '            margin: 10px 0;',
        '            width: 60%;',
        '            line-height: 1.6;',
        '        }',
        '    </style>',
        '</head>',
        '<body>'
    ]


def footer() -> List[str]:
    return [
        '</body>',
        '</html>'
    ]


def page_start_line(page_number: int) -> List[str]:
    return [
        f'    <p page={page_number}>↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓ {page_number} page ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓</p>'
    ]


def page_end_line(page_number: int) -> List[str]:
    return [
        f'    <p page={page_number}>↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑ {page_number} page ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑</p>'
    ]
