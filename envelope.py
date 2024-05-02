#!/usr/bin/python

from pypdf import PdfWriter, PdfReader
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_NAME=None
FONT_PATH=None
if FONT_NAME is not None and FONT_PATH is not None:
    pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))
TO_FONT_SIZE=12
FROM_FONT_SIZE=8

ENVELOPE = (7.25*inch, 5.25*inch)
INCHES_TO_POINTS = 72

def write_envelopes(out, from_addr, to_addrs):
    output = PdfWriter()
    
    MARGIN = 0.25
    for to_addr in to_addrs:
        packet = io.BytesIO()

        can = canvas.Canvas(packet, pagesize=ENVELOPE)
        if FONT_NAME is not None:
            can.setFont(FONT_NAME)
        can.setFontSize(FROM_FONT_SIZE)
        for i, line in enumerate(from_addr):
            
            can.drawString(MARGIN * INCHES_TO_POINTS, ENVELOPE[1]-((MARGIN * INCHES_TO_POINTS) + 12 + (12 * i)), line)
      
        can.setFontSize(TO_FONT_SIZE)
        for i, line in enumerate(to_addr):
            can.drawString(2.5 * INCHES_TO_POINTS, ENVELOPE[1]-((2.5 * INCHES_TO_POINTS) + 12 + (12 * i)), line)
            
            
        can.save()
        #move to the beginning of the StringIO buffer
        packet.seek(0)
        address_pdf = PdfReader(packet)
            
        address_page = address_pdf.pages[0]
        output.add_page(address_page)

    # finally, write "output" to a real file
    print(f"writing to {out}")
    output.write(out)
    
     
        


def load_csv(filename):
    # This logic is necessarily use case specific specific, but for
    # our list we just have three columns of addresses and an optional
    # fourth column that says "yes" for addresses we wanted printed.
    with open(filename) as f:
        for i, row in enumerate(csv.reader(f)):
            if i == 0:
                continue

            type = ''
            if len(row) > 3:
                type = row[3].strip()
            if type != 'yes':
                continue
            yield row[0:3]


if __name__ == '__main__':
    FROM_ADDR = ('Evan + Meena',
                 '[elided]',
                 'San Francisco, CA 94110')
    INFILE = None#'address.csv'
    OUTFILE = 'out.pdf'

    if INFILE is None:
        addresses=[FROM_ADDR]
    else:
        addresses=load_csv(INFILE)
    
    write_envelopes(OUTFILE, FROM_ADDR, addresses)
    print(f'wrote {OUTFILE}')
