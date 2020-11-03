import os
import PyPDF2
from config import *


def get_number_before_separator(page):
    return page.extractText().rsplit(SEPARATOR, 1)[0][-1]


def clean_pdf(pdf_input):
    pdf_reader = PyPDF2.PdfFileReader(f'{INPUT_PATH}/{pdf_input}')
    pdf_writer = PyPDF2.PdfFileWriter()
    last_page_n = pdf_reader.getNumPages() - 1

    for i in range(last_page_n):
        current_page = pdf_reader.getPage(i)
        next_page = pdf_reader.getPage(i + 1)
        print(f'Checked page: {i}')
        if get_number_before_separator(current_page) != get_number_before_separator(next_page):
            pdf_writer.addPage(current_page)
            print(f'Added page: {i}')

    # Add last page
    new_pdf_page_numbers = pdf_writer.getNumPages() - 1
    new_pdf_last_page = pdf_writer.getPage(new_pdf_page_numbers)
    old_pdf_last_page = pdf_reader.getPage(last_page_n)
    if old_pdf_last_page != new_pdf_last_page:
        pdf_writer.addPage(old_pdf_last_page)
        print(f'Added page: {last_page_n}')

    pdf_output = f'{OUTPUT_PATH}/{pdf_input}'

    with open(pdf_output, 'wb') as f:
        pdf_writer.write(f)


def make_directory():
    try:
        os.mkdir(OUTPUT_PATH)
        print("Directory created")
    except FileExistsError:
        print("Directory already exists")


def clean_pdf_all():
    make_directory()
    for entry in os.scandir(INPUT_PATH):
        print(f'Processing file: {entry.name}')
        clean_pdf(entry.name)


if __name__ == '__main__':
    clean_pdf_all()
