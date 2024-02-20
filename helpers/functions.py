import os
from flask import render_template

uploadFolder = 'static/uploads/'



def deleteFiles(app):

    # List all files in the uploads folder
    files = os.listdir(app)
    # Iterate over the files and remove them

    for file in files:
        if file != 's9k8o0p6d5r2f3i1l4e7t2e8x9t0f1o4r2u5m7t6e5n3o2d4i7s9c8o0m1p5u2t3e6r9i0n4t7e2r1e5l8a4e8t5c2o1n3s7e9c0t4e6t1u7r2p5i0s4i1c9s3u8m6v3o2l4u0t1p3o7r9a5c4t8e2x1t7r9a4o2r1n5a6d0i3p8i2s7c5o1r3d6o2v4a9t0i8o7n1s3.txt':
            file_path = os.path.join(app, file)
            os.remove(file_path)

# apology function for wrong input
def apology(message, code=400):

    # render apology
    return render_template("apology.html", top=code, bottom=message), code
