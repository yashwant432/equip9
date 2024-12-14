# equip9
equip9
 Structure of the Repository equp9
/equip9
  ├── README.md
  ├── /http_code
  │   ├── add_files.py
  │   ├── equip_app.py
  ├── /terraform_e9
  │   ├── main.tf
  │   ├── terraform.tfstate
  │   └── terraform.tfstate.backup
  
  
this assesment involve 2 steps 
1.Developing an HTTP service using a programming language of your choice.
2.Using Terraform to deploy this service on AWS.

Prerequisites
Before proceeding i have installed the following set up:

AWS account: will need access to an AWS account with appropriate IAM permissions.
AWS CLI: Ensure we have the AWS Command Line Interface (CLI) installed and configured with the proper credentials.
Terraform: Make sure Terraform is installed on ec2 machine.
Python 3: The HTTP service is written in Python, so we need Python 3 and pip installed

Structure of the equip9 assesment i used 
├── equip9/
│   ├── http_code/                # Contains the Flask app for the HTTP service
│   │   ├── equip_app.py          # Python Flask app for the HTTP service
│   │   └── add_files.py          # Script to add files to S3 bucket
│   └── terraform_e9/             # Contains the Terraform files for AWS deployment
│       ├── main.tf               # Terraform configuration for provisioning AWS resources
│       ├── terraform.tfstate     # Terraform state file
│       └── terraform.tfstate.backup  # Backup state file

Part 1: HTTP Service
Objective:
The goal of the HTTP service is to expose an endpoint that lists the contents of a specified path within an S3 bucket. If no path is specified, it lists the top-level files and directories.

Implementation:
The service is built using Flask and Boto3 (AWS SDK for Python). The service exposes the following API endpoint:

GET http://50.19.0.206:5000/list-bucket-content is list-bucket-content: Returns the top-level contents of the S3 bucket.
GET http://50.19.0.206:5000/list-bucket-content/dir1 : Lists the contents of the S3 directory specified in the <path> parameter.
Example Usage:
GET http://50.19.0.206:5000/list-bucket-content/dir2/list-bucket-content:
Response:
{
  "content": ["dir1", "dir2", "file1", "file2"]
}
GET http://50.19.0.206:5000/list-bucket-content/dir1:
{
  "content": []
}
GET http://50.19.0.206:5000/list-bucket-content/dir2:

{
  "content": ["file1", "file2"]
}

How it works:
Flask is used to create a simple API.
Boto3 is used to interact with AWS S3 to list the contents of the bucket and directories.
The S3 client uses list_objects_v2 to get the objects inside the bucket.
If no path is provided, it lists the top-level files and folders.
If a specific path (directory) is provided, it lists the contents of that path.

attaching screenshots of the final output
1. For http://50.19.0.206:5000/list-bucket-content
![alt text](image.png)
2. for http://50.19.0.206:5000/list-bucket-content/dir1
![alt text](image-1.png)
3. for http://50.19.0.206:5000/list-bucket-content/dir2
![alt text](image-2.png)

i have tested on localy befor deploying on ec2 instance 
How to run locally:
Install the required dependencies:
go the the code path
├── equip9/
   ├── http_code/                # Contains the Flask app for the HTTP service
     ── equip_app.py   # code 
Run the app:
python3 equip_app.py
The Flask app will start, and you can test it using curl or Postman by visiting:
http://127.0.0.1:5000/list-bucket-content
http://127.0.0.1:5000/list-bucket-content/dir1
http://127.0.0.1:5000/list-bucket-content/dir2

attaching screenshots for local run
![alt text](image-4.png)    ![alt text](image-17.png)
![alt text](image-18.png)
output screenshot
![alt text](image-3.png)

Part 2: Terraform Deployment
Objective:
The goal of this part is to automate the deployment of the HTTP service using Terraform. Terraform is used to provision AWS infrastructure, including an EC2 instance to run the Flask application and an S3 bucket to store the files.

Steps to Deploy:
Configure AWS Credentials: Ensure your AWS CLI is configured with your credentials. You can configure it by running:

aws configure

Set up Terraform:

Install Terraform as was not installed yet.

Created main.tf file, which will:

Provision an EC2 instance that will host the Flask app.
Create an S3 bucket to store the files.
main.tf configuration:
main.tf 
after creating the main.tf Deploy with Terraform:

Initialize Terraform:
terraform init
plan the configuration to check :
terraform plan
Apply the configuration:
terraform apply
 will create the necessary resources in AWS, including the EC2 instance and the S3 bucket.

 attaching screenshots but initialization, plan and apply step in recorded video
 terraform destroy
 ![alt text](image-5.png)

 terraform plan 
![alt text](image-6.png)
![alt text](image-7.png)

after terraform apply
![alt text](image-9.png)   - resource added by aaply
![alt text](image-8.png)    - s3 bucket creation
![alt text](image-10.png)  ![alt text](image-11.png)  - creation of instance 

Folder creation in bucket using python 
![alt text](image-12.png)  - dir1 and dir2
![alt text](image-13.png)   ![alt text](image-14.png)  -file1 and file2
output foe dir1 and dir 2 ![alt text](image-15.png) ![alt text](image-16.png)
s3 bucket url s3://e9-http-service-bucket/dir2/file1/

Clean Up:
After the testing is complete, you can delete the AWS resources to avoid extra charges by running:
terraform destroy  

 
1: Create a GitHub Repository
Log into GitHub:
![alt text]({A33AFECB-1D7F-49A4-963D-E847E5E5095F}.png)
Visit GitHub and log in with your GitHub account credentials.
Create a New Repository:
Repository Name: equip9
2: Initialize a Local Git Repository
Navigate to  project directory: Open a terminal/command prompt and navigate to the root folder of your project (where your README.md and project files are located). 
cd /home/ubuntu/equip9

Initialize a Git repository: Run the following command to initialize the local Git repository:
git init    

3: Add Files to the Repository
Add all files to the staging area: Run the following command to add all files in your project to the Git staging area:

git add .       
screenshot ![alt text](image-19.png)
Commit the changes: Commit changes with a descriptive message:


git commit -m "Initial commit with HTTP service and Terraform deployment"
screenshot ![alt text](image-20.png)

5: Push Code to GitHub
Push the code to the repository: Push code to the main branch on GitHub using:

git push -u origin main
screenshot 



Step 6: Verify on GitHub
Go to your GitHub repository: After pushing, visit your repository page on GitHub 
https://github.com/yashwant432/equip9.git
screenshot ![alt text]({FA2DF79E-570D-45F0-9D7D-DDE8DEE0CC84}.png)



