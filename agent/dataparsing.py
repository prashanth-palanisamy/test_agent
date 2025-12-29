import re, os, shutil

def contentparsing(response: str):

    # Base directory for generated Terraform code
    TERRAFORM_DIR = os.path.join(os.getcwd(), "terraform")

    # Optional: Clean existing terraform dir before writing new files
    if os.path.exists(TERRAFORM_DIR):
        shutil.rmtree(TERRAFORM_DIR)
    os.makedirs(TERRAFORM_DIR, exist_ok=True)

    # Regex to detect cloud sections (### AWS: modules/aws/, ### Azure: modules/azure/, etc.)
    cloud_section_pattern = r"###\s*(\w+):\s*(modules/[^\n/]+/)"
    cloud_sections = re.split(cloud_section_pattern, response)
    # print(cloud_sections)

    if len(cloud_sections) <= 1:
        print("⚠️ No cloud sections found. Falling back to single parser.")
        return _single_cloud_parser(response, TERRAFORM_DIR)

    # cloud_sections will split into [text_before, CloudName, ModulePath, content, CloudName, ModulePath, content, ...]
    for i in range(1, len(cloud_sections), 3):
        cloud_name = cloud_sections[i].strip()
        module_path = cloud_sections[i + 1].strip()
        content = cloud_sections[i + 2]

        print(f"🌩️ Processing {cloud_name} → {module_path}")

        # Match Terraform file blocks inside this cloud section
        file_pattern = r"####\s*([^\n]+\.(?:tf|tfvars|tf.json))\n```[\w]*\n(.*?)```"
        matches = re.findall(file_pattern, content, re.DOTALL)
        # print(f"matches: {matches}")

        if not matches:
            print(f"⚠️ No Terraform files found under {cloud_name} / {module_path}")
            continue

        for filename, filecontent in matches:
            #filename = filename.strip()
            filename = filename.strip().split('/')[-1]
            filecontent = filecontent.strip() + "\n"

            # Full path (terraform/modules/aws/main.tf, etc.)
            # print(f"module path :- {module_path}")
            # print(f"filename :- {filename}")
            filepath = os.path.join(TERRAFORM_DIR, module_path, filename)
            # print(f"filepath :- {filepath}")
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            # print(f"response :- {response}")


            with open(filepath, "w") as f:
                f.write(filecontent)

            print(f"✅ Saved {filepath}")

    return f"🎉 Multi-cloud Terraform files generated inside {TERRAFORM_DIR}/"


def _single_cloud_parser(response, TERRAFORM_DIR):
    import re, os

    # This regex looks for:
    # 1. A path/filename (can include slashes)
    # 2. A terraform code block wrapped in ```
    pattern = r"([^\s\n]+\.(?:tf|tfvars|tf\.json))\n(.*?)(?=\n[^\s\n]+\.(?:tf|tfvars|tf\.json)|\Z)"
    matches = re.findall(pattern, response, re.DOTALL)
    print(f"matches {matches}")

    if not matches:
        return "❌ Parsing failed — no files detected."

    for filepath_raw, filecontent in matches:
        # Clean up the path and content
        clean_relative_path = filepath_raw.strip()
        filecontent = filecontent.strip() + "\n"

        # Combine the base terraform dir with the relative path from the LLM
        # This automatically handles 'modules/vpc/main.tf' or 'main.tf'
        final_filepath = os.path.normpath(os.path.join(TERRAFORM_DIR, clean_relative_path))

        # Create any necessary subfolders (like modules/vpc/)
        os.makedirs(os.path.dirname(final_filepath), exist_ok=True)
        # print(f"filepath_raw: {filepath_raw}")
        # print(f"filecontent: {filecontent}")
        # print(f"final_filepath: {final_filepath}")
        with open(final_filepath, "w") as f:
            f.write(filecontent)

        print(f"✅ Saved {final_filepath}")

    return f"🎉 All Terraform files generated in {TERRAFORM_DIR}"

#################################
# shann - code starting
#====================================#

# def _single_cloud_parser(response, TERRAFORM_DIR):
#     """Fallback parser if no cloud sections exist"""
#     #pattern = r"([^\n:]+\.(?:tf|tfvars|tf.json))\n(.*?)(?=(?:\n\S+\.(?:tf|tfvars|tf.json))|$)" # shan code re-gex working for multi cloud
#     pattern = r"\s*([^\n]+\.(?:tf|tfvars|tf.json))\n```[\w]*\n(.*?)```"
#     matches = re.findall(pattern, response, re.DOTALL)
#     print(f"\n==============\nresponse :- \n {response}")
#     print(f"\n==============\nmatches :- \n {matches}")
#
#     if not matches:
#         print("❌ Parsing failed — no files detected.")
#         return "❌ Parsing failed — no files detected."
#
#     for filename, content in matches:
#         filename = filename.strip()
#         content = content.strip() + "\n"
#
#         #filepath = os.path.join(TERRAFORM_DIR, filename)
#         filepath = os.path.join(TERRAFORM_DIR, "modules", filename)
#         #os.makedirs(os.path.dirname(filepath), exist_ok=True)
#
#         with open(filepath, "w") as f:
#             f.write(content)
#
#         print(f"✅ Saved {filepath}")
#
#     return f"🎉 All Terraform files generated in {os.path.join(TERRAFORM_DIR, 'modules')}"
###############################
# shaan code ending
#=======================================

