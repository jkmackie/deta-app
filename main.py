#terminal uvicorn command: uvicorn main:app --reload
#Test API - http://localhost/docs
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import shutil, os, uvicorn

im_folder = './images'
if not os.path.exists(im_folder):
    os.mkdir(im_folder)

app = FastAPI()

@app.get('/', response_class=HTMLResponse)  #Homepage at root
async def home():
    return '''
    <h1>Home</h1>
    <a href='http://127.0.0.1:8000/docs'>http://127.0.0.1:8000/docs</a>'''

@app.post("/upload/") #Upload image to image_path
async def upload_file(fileb: UploadFile = File(...)):
    fsize = round(len(fileb.file.read())/1_000_000,2) #read sets pointer to END of file
    if fsize >= 5:
        return {"error_message:": "File size must be under 5 MB.", "file_MB": fsize}

    image_path = os.path.join(im_folder, fileb.filename)
    with open(image_path, 'wb') as f:
        fileb.file.seek(0)
        shutil.copyfileobj(fileb.file, f)
    return {"fileb_name": fileb.filename,"fileb_content_type": fileb.content_type, "file_MB": fsize}

if __name__ == '__main__':
    uvicorn.run(app)
