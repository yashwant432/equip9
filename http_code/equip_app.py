from flask import Flask, jsonify
import boto3

app = Flask(__name__)

# S3 client with region specified
bucket_name = 'e9-http-service-bucket'
region_name = 'ap-south-1'  # Replace with the correct region

s3_client = boto3.client('s3', region_name=region_name)

@app.route('/list-bucket-content/<path:prefix>', methods=['GET'])
@app.route('/list-bucket-content', methods=['GET'])
def list_bucket_content(prefix=''):
    try:
        # If prefix is empty, list top-level objects (files and directories)
        if prefix == '':
            response = s3_client.list_objects_v2(Bucket=bucket_name, Delimiter='/')
        else:
            # List objects under the specified directory (prefix)
            response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix, Delimiter='/')
        
        # Log the entire response from S3 for debugging purposes
        print("S3 Response:", response)

        # Get directories (common prefixes)
        directories = [item['Prefix'].strip('/') for item in response.get('CommonPrefixes', [])]
        
        # Get files (excluding directories, objects without a trailing slash)
        files = [item['Key'].strip('/') for item in response.get('Contents', []) if not item['Key'].endswith('/')]

        # If the prefix is provided and no files or directories are found, return an empty list
        if prefix and not directories and not files:
            content = []
        else:
            content = directories + files

        return jsonify({"content": content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run Flask app on all available interfaces (0.0.0.0)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
