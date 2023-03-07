import os
import cv2
#from app.image_quality_single import image_index_cal
from app.Class_imageQI_tool import image_index_cal
from flask import render_template, request
from flask import send_file


upload_folder = 'static/upload'

def index():
    return render_template('index.html')

def app():
    return render_template('app.html')

def download_csv(file_name):
    csv_path = os.path.join('static/predict', file_name)
    return send_file(csv_path, as_attachment=True)

def tool():
    if request.method == "POST":
        # Get all uploaded images
        files = request.files.getlist("image_name")
        report = []

        # Iterate through each uploaded image
        for f in files:
            filename = f.filename
            # Save the image in the upload folder
            path = os.path.join(upload_folder, filename)
            f.save(path)

            # Get predictions for the image
            csv_file, predictions = image_index_cal(upload_folder)
            #print(predictions)

            # Generate report for the image
            '''
            for i, obj in enumerate(predictions):
                image_name = obj['Image_name'] # image name
                quality_index = obj['Quality_index']
                image_quality = obj['Image_Quality']

                # Save report
                report.append([image_name, quality_index, image_quality])
                '''

                #csv_file = f"{image_name}_quality.csv" # Construct the file name of the CSV file
                #csv_path = os.path.join('static/predict', csv_file) # Construct the path to the CSV file
        
        print(predictions)
        
        # Delete uploaded image
        for f in files:
            filename = f.filename
            path = os.path.join(upload_folder, filename)
            os.remove(path)

        return render_template('tool.html', fileupload = True, report=predictions, csv_file=csv_file) # post request
    
    

    return render_template('tool.html', fileupload = False) # get request