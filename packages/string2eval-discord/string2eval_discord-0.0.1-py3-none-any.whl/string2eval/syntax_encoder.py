import base64
import codecs


def syntax_encode(_in):
    bas = codecs.decode(_in, "rot13")
    asc = bas.encode('ascii')
    n_coded = base64.b64decode(asc)
    return int(n_coded.decode('ascii'))
