import os
from flask import Flask, jsonify
import boto3

app = Flask(__name__)

# Configure S3 client
s3_client = boto3.client('s3')
bucket_name = 'e9-http-service-bucket'

@app.route('/list-bucket-content', defaults={'path': ''})
@app.route('/list-bucket-content/<path:path>')
def list_bucket_content(path):
    try:
        # If path is empty, list top-level contents of the bucket
        if path == '':
            response = s3_client.list_objects_v2(Bucket=bucket_name, Delimiter='/')
            # Include all files and folders from the top level, excluding the directory prefixes
            contents = [content['Prefix'].strip('/') for content in response.get('CommonPrefixes', [])]
            contents.extend([content['Key'] for content in response.get('Contents', [])])
            
            # Filter out directories from the contents (remove items that end with '/')
            contents = [item for item in contents if not item.endswith('/')]
            return jsonify({'content': contents})

        # If path is specified, list contents inside that directory
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=path + '/', Delimiter='/')
        # Include all files and folders inside the specified path, excluding the directory prefixes
        contents = [content['Prefix'].strip('/') for content in response.get('CommonPrefixes', [])]
        contents.extend([content['Key'] for content in response.get('Contents', [])])
        
        # Filter out directories from the contents (remove items that end with '/')
        contents = [item for item in contents if not item.endswith('/')]
        
        # If no contents are found, return an empty array
        if not contents:
            return jsonify({'content': []})

        return jsonify({'content': contents})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
