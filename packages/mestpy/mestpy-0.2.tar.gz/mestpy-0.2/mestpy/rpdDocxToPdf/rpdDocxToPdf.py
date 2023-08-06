def rpdDocxToPdf(directory):
    from docx2pdf import convert
    import os

  
    files = os.listdir(directory)
    print(len(files))


    for ids,f in enumerate(files):
        f_name, f_ext=os.path.splitext(f)
        # Паказываю инфо о файлах
        name='{} {} {}'.format(ids+1,f_name, f_ext)
        print(name)
    convert(directory+'/')

