import zipfile
import os
import shutil

#in this case, we want to make all the files to this dir
target_dir = "DIR" # change the target dir here
if not os.path.exists(target_dir):
    os.makedirs(target_dir) ## find the target folder, if not created, it will create a new dir

# Process every zip file in the current directory
for file in os.listdir("."):
    if file.endswith(".zip"):
        print(f"Processing {file}...") # check status 
        with zipfile.ZipFile(file, 'r') as zip_ref:
            for member in zip_ref.namelist():
                # skip the doclist PDFs 
                if member.endswith("_doclist.PDF"): ## remove the line if you do not want to remove the files
                    continue
                if member.endswith('/'): #skip directory entries 
                    continue
                # extract and flatten (ignore internal folders)
                filename = os.path.basename(member)
                if filename: # not empty
                    source = zip_ref.open(member)
                    target_path = os.path.join(target_dir, filename)
                    with open(target_path, "wb") as target_file:
                        shutil.copyfileobj(source, target_file)

print(f"\nSuccess! Files are ready in the '{target_dir}' folder.")
