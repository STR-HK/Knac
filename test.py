import Hangul

text = '쀏'

jamo = Hangul.jamo(text)
print(jamo)

gyeopjamo = Hangul.gyeopjamo(jamo)
print(gyeopjamo)

num = Hangul.convertonumber(''.join(gyeopjamo))
print(num)