import sys
import os
from PyPDF2 import PdfMerger

def merge_pdfs(output_filename, input_filenames):
    merger = PdfMerger()

    for filename in input_filenames:
        merger.append(filename)

    merger.write(output_filename)
    merger.close()

    #Usuń stare pliki PDF
    #for filename in input_filenames:
     #os.remove(filename)

if __name__ == "__main__":
    first_filename = sys.argv[1]
    input_filenames = sys.argv[1:]
    output_filename = first_filename.rsplit('.', 1)[0] + '_merged.pdf'
    merge_pdfs(output_filename, input_filenames)

