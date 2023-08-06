'''
    Set page start end for query offset
    @num_page number of page
    @max_rows max_rows for query in one page.
'''
def setstartend(num_page,max_rows):
    start    = (int(num_page)-1)*max_rows
    end      = int(num_page)*max_rows
    return {'start':start,'end':end}
