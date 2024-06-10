from flask import *
import requests, os, zipfile, shutil, datetime
from flask import send_file

def folder_to_zip(folder_name):
    zip_file_name = f"{folder_name}.zip"
    with zipfile.ZipFile(zip_file_name, 'w') as zip_file:
        for root, dirs, files in os.walk(folder_name):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, folder_name))

def get_code_from_prompt_list(y):
  h=""
  for x in [i for i in y if y.index(i)%2 == 1]:
    if "python\n" in x:
      h = h + x.replace("python\n","")
    else:
      h=h+x
  return h

api_key = "" # Enter your own API KEY

def get_zip(foldername, api_key, prompt):
  try:
    open(foldername+".py","a").write(get_code_from_prompt_list(str(requests.post("https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=" + api_key, headers={"Content-Type": "application/json"}, json={"contents": [{"parts": [{"text": f'write the python code to create files in director name = "{foldername}" and write code content inside it. Just geneate python code for query - '+ prompt.upper()}]}]}).json()["candidates"][0]["content"]["parts"][0]["text"]).split("```")))
    os.system(f"python3 {foldername}.py")
    os.remove(f"{foldername}.py")
    if os.listdir(foldername) == []:
      shutil.rmtree(foldername)
      return False
    folder_to_zip(foldername)
    shutil.rmtree(foldername)
    return True
  except:
    return False

#get_zip(input("Enter folder name: "),api_key, input("Enter prompt: "))

app = Flask(__name__, template_folder=os.getcwd(), static_folder="static")

@app.route("/", methods=["POST","GET"])
def index():
  if request.method == "GET":
    return render_template("index.html")
  else:
    file=str(datetime.datetime.now()).replace("-","").replace(":","").replace(".","").replace(" ","")
    if get_zip(file, api_key, request.form["search"]):
      return send_file(file+".zip")
    else:
      return render_template("index.html", err=True,msg="Try again")

if __name__ == '__main__':
  app.run(debug=True)