import pyPdf
import time
import urllib2
from django.conf import settings

#save file locally 
def archive_file(original_url, gov_id, doc_type, file_type):
    type_dir = doc_type.lower().replace(' ', '_')
    file_name = "%s%s/%s.%s" % (settings.DATA_ROOT, type_dir, gov_id, file_type)
    try:
        remote_file = urllib2.urlopen(original_url)
        local_file = open(file_name, "w")
        local_file.write(remote_file.read())
        local_file.close
    except:
        pass
    return file_name
    
def pdf_extract_text(path, original_url):
    #adapted from http://code.activestate.com/recipes/511465/
    content = ""
    try:
        try:
            pdf = pyPdf.PdfFileReader(file(path, "rb"))
        except:
            remote_file = urllib2.urlopen(original_url)
            local_file = open(path, "w")
            local_file.write(remote_file.read())
            local_file.close
            pdf = pyPdf.PdfFileReader(file(path, "rb"))

        for i in range(0, pdf.getNumPages()):
            content += pdf.getPage(i).extractText() + "\n"
        content = " ".join(content.replace("\n", " ").strip().split())
    except:
        pass
    return content
    
def debug_print(output):
    if DEBUG:
        print output