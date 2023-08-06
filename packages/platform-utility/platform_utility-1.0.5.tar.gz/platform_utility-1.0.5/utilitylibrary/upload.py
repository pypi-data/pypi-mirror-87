
from utilitylibrary.unique import gennerate_unique

'''
    Get file type from filename.
    @filename name of file.
    return mimeType
'''

def split_mime_type(filename):
    mimeType = filename.split(".")
    return mimeType[1]


'''
    Upload list of file.
    @f temp of file.
    @destination_path pathupload with out filename.
'''
def handle_uploaded_file(f,destination_path):
    with open(destination_path+gennerate_unique()+'.'+split_mime_type(f.name), 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)
            