from pix2text import Pix2Text
import sys

tmp_path = sys.argv[1]

pix2text_engine = Pix2Text()

text = pix2text_engine.recognize(tmp_path)

print(text)