import gradio as gr
from fileTransferMXF import *

def return_multiple(name, number):
    result = "Hi {}! 😎. The Mulitple of {} is {}".format(name, number, round(number**2, 2))
    return result

def ingest_disc():
    src_path = "C:\\Users\\alex.hobbs\\Desktop\\Input"
    dst_path = "C:\\Users\\alex.hobbs\\Desktop\\Output"
    finalDst_path = "C:\\Users\\alex.hobbs\\Desktop\\Output\\FILE"
    file_extension = ".mxf"

    targetPath = destinationFolderCreation(dst_path)
    copyAllFiles(src_path, targetPath, file_extension)
    ingest_folder(targetPath, finalDst_path)
    confirmation = "finished copying " + targetPath + "! :)"
    return confirmation


if __name__ == "__main__":
    #app = gr.Interface(fn = return_multiple, inputs=["text", gr.Slider(0, 50)], outputs="text")
    app = gr.Interface(fn = ingest_disc, inputs=[], outputs="text")
    #gr.Blocks(title="Disk Ingester", theme="darkdefault")
    app.launch()

