def load_protobuf_from_file(container,filename):
    with open(filename,'rb') as fin:
        file_content=fin.read()
    try:
        container.ParseFromString(file_content)
        print("Parse file [%s] with binary format successfully." % (filename))
        return container
    except Exception as e:
        print("Info: Trying to parse file [%s] with binary format but failed with error [%s]." % (filename, str(e)))
    try:
        from google.protobuf import text_format
        text_format.Parse(file_content.decode('UTF-8'), container, allow_unknown_extension=True)
        print("Parse file [%s] with text format successfully." % (filename))
    except text_format.ParseError as e:
        raise IOError("Cannot parse file %s: %s." % (filename, str(e)))
    return container