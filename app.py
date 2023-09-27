import boto3
import requests
import os

from flask import Flask, redirect, url_for, request, render_template

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

    @app.route("/s3", methods=["GET", "POST"])
    def index():
        url = os.environ['GET_NUM_OF_RECS_URL']

        users_count = requests.get(url).text

        print(users_count)

        text_file = open("file_to_upload.txt", "w")
        text_file.write(users_count)
        text_file.close()

        if request.method == "POST":
            uploaded_file = request.files["file-to-save"]
            if not allowed_file(uploaded_file.filename):
                return "FILE NOT ALLOWED!"

            bucket_name = 'ttomczyk-bucket-ups006'
            s3_client = boto3.client('s3')

            response = s3_client.generate_presigned_post(
                Bucket=bucket_name,
                Key=uploaded_file.filename,
                ExpiresIn=10
            )

            files = {'file': open(uploaded_file.filename, 'rb')}
            r = requests.post(response['url'], data=response['fields'], files=files)
            print(r.status_code)

            return redirect(url_for("index"))

        return render_template("index.html", users_count=users_count)

    return app
