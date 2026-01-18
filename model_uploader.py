from huggingface_hub import login, upload_folder

# (optional) Login with your Hugging Face credentials
login()

# Push your model files
upload_folder(folder_path="C:/Users/HP/Desktop/PROJECTS/FNOL/models/", repo_id="SUPERMOSCO/fnol_model", repo_type="model")