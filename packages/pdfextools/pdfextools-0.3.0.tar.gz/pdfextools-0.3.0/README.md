# PdfExTools

This package contains tools can be used to handle pdf files. 

## 1. PageNumberExtractor:

to extract physical page numbers, i.e., the page numbers printed in page (as part of content in the page), rather than the logical page numbers tracked by pdf reader or tools like pdfplumber, pymupdf, etc. This can be useful because sometimes the pdf file was excerpted from a large file, as a result, the page number showing in page can start from 135 to 145, while the total number of pages is 11 (1-11).

### 1) to install:
```
pip install PdfExTools
```

### 2) to use, do the following:
```
from pdfextools import PageNumberExtractor

pdf_file = r"./sample-pdfs/2-col-pubmed.pdf"

print("pdf_file: " + pdf_file)

extractor = PageNumberExtractor()
page_numbers = extractor.process(pdf_file)

print(page_numbers)
```

The result will be a dictionary mapping logical page numbers (base-0) to the physical ones. For example:
```
pdf_file: /sample-pdfs/2-col-pubmed.pdf
{0: 11, 1: 12, 2: 13, 3: 14, 4: 15, 5: 16, 6: 17, 7: 18, 8: 19, 9: 20, 10: 21, 11: 22, 12: 23}
```
