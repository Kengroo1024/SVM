import requests

a = requests.post("http://127.0.0.1:7735/upload",
                  files={"data": open(".venv\\pyvenv.cfg", "rb")})

print(a.status_code)
