from flask import Flask, request
from fileTransferMXF import *

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # src_path = request.form.get("src_path", "C:\\Users\\alex.hobbs\\Desktop\\Input")
        # dst_path = request.form.get("dst_path", "C:\\Users\\alex.hobbs\\Desktop\\Output")
        # finalDst_path = request.form.get("finalDst_path", "C:\\Users\\alex.hobbs\\Desktop\\Output\\FILE")
        # file_extension = request.form.get("file_extension", ".mxf")
        #test_var = request.form.get("test_var", ".mxf")
        src_path = "C:\\Users\\alex.hobbs\\Desktop\\Input"
        dst_path = "C:\\Users\\alex.hobbs\\Desktop\\Output"
        finalDst_path = "C:\\Users\\alex.hobbs\\Desktop\\Output\\FILE"
        file_extension = ".mxf"

        if request.form.get("ingest_button"):
            targetPath = destinationFolderCreation(dst_path)
            copyAllFiles(src_path, targetPath, file_extension)
            ingest_folder(targetPath, finalDst_path)
            return "Files have been copied and ingested."

    return '''
        <form method="post">
            Source Path: <input type="text" name="src_path" value="C:\\Users\\alex.hobbs\\Desktop\\Input"><br>
            Destination Path: <input type="text" name="dst_path" value="C:\\Users\\alex.hobbs\\Desktop\\Output"><br>
            Final Destination Path: <input type="text" name="finalDst_path" value="C:\\Users\\alex.hobbs\\Desktop\\Output\\FILE"><br>
            File Extension: <input type="text" name="file_extension" value=".mxf"><br>
            <input type="submit" name="ingest_button" value="Ingest"><br>   
        </form>
    '''

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)

