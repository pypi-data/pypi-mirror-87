import uuid 

'''
    Gennerate unique.
    @length size of unique.
    return unique string
'''
def gennerate_unique(length=6):
    return uuid.uuid4().hex[:length].upper()
    