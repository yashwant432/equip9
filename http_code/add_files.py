import boto3

def list_s3_buckets():
    # Create an S3 client
    s3_client = boto3.client('s3')

    # List all buckets
    response = s3_client.list_buckets()
    buckets = response['Buckets']

    print("Available S3 Buckets:")
    for bucket in buckets:
        print(f"- {bucket['Name']}")

    return buckets

def list_folders_in_bucket(bucket_name, prefix=''):
    s3_client = boto3.client('s3')

    # List objects in the bucket with the given prefix (to simulate folder structure)
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix, Delimiter='/')

    # List of folders (common prefixes in S3 are similar to folders)
    folders = [prefix['Prefix'] for prefix in response.get('CommonPrefixes', [])]
    
    return folders

def create_folder_in_bucket(bucket_name, folder_name):
    s3_client = boto3.client('s3')
    
    # Ensure no leading or trailing slashes and add one slash at the end
    folder_name = folder_name.strip('/')  # Remove any accidental leading/trailing slashes
    folder_key = f'{folder_name}/'  # Proper folder key format
    
    # Create the folder by uploading an empty object with the folder name
    s3_client.put_object(Bucket=bucket_name, Key=folder_key)
    print(f"Folder '{folder_name}' created in bucket '{bucket_name}'.")

def upload_file_to_folder(bucket_name, folder_name, file_path):
    s3_client = boto3.client('s3')
    
    # Ensure folder name has no leading/trailing slashes
    folder_name = folder_name.strip('/')
    
    # Get the file name from the file path
    file_name = file_path.split("/")[-1]
    
    # Upload the file to the folder (path will include the folder name)
    s3_client.upload_file(file_path, bucket_name, f'{folder_name}/{file_name}')
    print(f"File '{file_name}' uploaded to '{folder_name}' in bucket '{bucket_name}'.")

def navigate_folders(bucket_name, prefix=''):
    # List the folders under the given prefix
    folders = list_folders_in_bucket(bucket_name, prefix)

    if not folders:
        print(f"No folders found under '{prefix}'")
        return prefix

    print(f"Folders under '{prefix}':")
    for i, folder in enumerate(folders):
        print(f"{i + 1}. {folder}")

    folder_choice = input("\nDo you want to go into a folder? (Enter the folder number, 'back' to go up a level, or 'no' to stop): ")

    if folder_choice.lower() == 'no':
        return prefix  # Stay at the current level
    elif folder_choice.lower() == 'back':
        # Go up to the parent folder (strip the last part of the prefix)
        return '/'.join(prefix.strip('/').split('/')[:-1]) or ''
    try:
        folder_index = int(folder_choice) - 1
        selected_folder = folders[folder_index]
        print(f"Entering folder: {selected_folder}")
        return navigate_folders(bucket_name, selected_folder)  # Recursively navigate
    except (ValueError, IndexError):
        print("Invalid choice. Staying at the current level.")
        return prefix

def create_folders_in_current_location(bucket_name, current_folder):
    # Function to create multiple folders in the current folder without asking repeatedly
    while True:
        folder_name = input(f"Enter the name of the new folder to create in '{current_folder}': ")
        
        # Ensure no extra slashes are added
        folder_name = folder_name.strip('/')
        
        # Ensure the current folder doesn't end with a slash before appending
        full_folder_name = f"{current_folder.strip('/')}/{folder_name}"
        
        create_folder_in_bucket(bucket_name, full_folder_name)
        
        # After creating, ask if the user wants to create another folder in the current folder
        continue_choice = input(f"Do you want to create another folder in '{current_folder}'? (Enter 'yes' or 'no'): ").lower()
        if continue_choice != 'yes':
            break

# List buckets
buckets = list_s3_buckets()

# Ensure there are buckets available
if len(buckets) > 0:
    # Let the user enter the bucket name directly
    bucket_name = input("Enter the name of the bucket you want to use: ")

    # Check if the entered bucket name is valid
    valid_buckets = [bucket['Name'] for bucket in buckets]
    if bucket_name in valid_buckets:
        # Start navigation from the root of the bucket
        selected_folder = navigate_folders(bucket_name)
        
        # Ask to create folders in the selected location
        create_folders_in_current_location(bucket_name, selected_folder)

    else:
        print(f"Invalid bucket name '{bucket_name}'. Please choose from the listed buckets.")
else:
    print("No buckets available.")
