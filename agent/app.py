import os, glob
import re
import streamlit as st
from dotenv import load_dotenv
from agent.modelsearch import get_model_list
#from agent
import terraform, format, agent, dataparsing, githelper

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# TERRAFORM_DIR = os.path.join(os.getcwd(), "terraform")

# os.makedirs(TERRAFORM_DIR, exist_ok=True)

BASE_DIR = os.getcwd()
TERRAFORM_DIR = os.path.join(BASE_DIR, "terraform")
JENKINS_DIR = os.path.join(BASE_DIR, "jenkins")

# Modified to accept the selected model as an argument
# def get_groq_response(prompt, model_id):
#     headers = {
#         "Authorization": f"Bearer {GROQ_API_KEY}",
#         "Content-Type": "application/json"
#     }
#     payload = {
#         "model": model_id,
#         "messages": [{"role": "user", "content": prompt}]
#     }
#     response = requests.post("https://api.groq.com/openai/v1/chat/completions",
#                              headers=headers, json=payload)
#
#     if response.status_code == 200:
#         return response.json()["choices"][0]["message"]["content"]
#     else:
#         raise Exception(f"Groq API Error: {response.text}")


# # ========== User Prompt ==========
# user_prompt = st.text_area("Enter your prompt:", placeholder="Type your Terraform request here...")

# ========== Generate Terraform Code ==========


# def extract_tf_blocks(content):
#     blocks = {"main.tf": "", "variables.tf": "", "outputs.tf": ""}
#     current_file = "main.tf"
#     lines = content.split("\n")
#     for line in lines:
#         if re.match(r"^\s*(main|variables|outputs)\.tf\s*[:：]?\s*$", line.strip().lower()):
#             current_file = line.strip().split(".")[0].lower() + ".tf"
#         elif "```" not in line:
#             blocks[current_file] += line + "\n"
#     return blocks


# def write_tf_files(blocks):
#     for filename, code in blocks.items():
#         file_path = os.path.join(TERRAFORM_DIR, filename)
#         with open(file_path, "w") as f:
#             f.write(code.strip())


# def run_terraform_command(command):
#     try:
#         subprocess.run(["terraform", "init", "-input=false"], cwd=TERRAFORM_DIR,
#                        check=True, capture_output=True)
#         tf_command = ["terraform", command]
#         if command in ["apply", "destroy"]:
#             tf_command.append("-auto-approve")
#         result = subprocess.run(tf_command, cwd=TERRAFORM_DIR,
#                                 capture_output=True, text=True, check=True)
#         return result.stdout
#     except subprocess.CalledProcessError as e:
#         return e.stderr


# def clean_output(output):
#     if isinstance(output, bytes):
#         output = output.decode("utf-8", errors="ignore")
#     elif not isinstance(output, str):
#         output = str(output)
#     ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
#     return ansi_escape.sub('', output)


# --- Streamlit UI ---
st.set_page_config(page_title="Terraform AI Agent", layout="wide")
st.title("🚀 AI Terraform Agent")

# 1. Fetch Model Data
models = get_model_list()

if models:
    # Create a mapping so we can retrieve the full ID later
    # Format: "gpt-oss-120b (Owned by: OpenAI)" -> "openai/gpt-oss-120b"

    model_map = {
        f"{m['id'].split('/')[-1]} (Owned by: {m['owned_by']})": m['id']
        for m in models
    }

    options = list(model_map.keys())

    if "persistent_model_selection" not in st.session_state:
        st.session_state.persistent_model_selection = options[0]

    # if "selected_model" not in st.session_state:
    #     st.session_state.selected_model = options[0]

    selected_option = st.selectbox(
        "Select a Model:",
        options,
        key="persistent_model_selection"
    )

    st.session_state.selected_model = selected_option

    # selected_option = st.selectbox("Select a Model:", list(model_map.keys()))
    selected_model_full_id = "llama-3.3-70b-versatile"
    #selected_model_full_id = model_map[st.session_state.selected_model]  # This goes to API
    #selected_model_display = selected_option.split(" (")[0]  # For UI display
    selected_model_display = selected_option.split(" (")[0]
    #selected_model_display = st.session_state.selected_model.split(" (")[0]

    st.markdown(
        f"Use this interface to generate, preview, and apply Terraform code using **{selected_model_display}**.")
    st.success(f"Active Model: {selected_model_full_id}")
else:
    st.error("No models found or API error.")
    selected_model_full_id = os.getenv("GROQ_MODEL", "llama3-8b-8192")

prompt = st.text_area("📥 Enter Terraform Request", height=180, placeholder="e.g., VPC with 2 public subnets...")

message = [{
        "role": "user",
        "content": prompt,
}
]

if st.button("🧠 Generate Terraform code"):
    st.subheader("Generated Terraform Code")
    # Calling LLM to fetch data
    response = agent.calling_groq(message, selected_model_full_id)

    # # After receiving AI response and extracting blocks:
    # blocks = extract_tf_blocks_universal(response)
    # clear_terraform_folder()
    # write_tf_blocks(blocks)
    # # Show generated files
    # for filename, code in blocks.items():
    #     with st.expander(filename): st.code(code, language="hcl")

    # Printing collected data on screen
    st.code(response, language="hcl")
    # Parsing data to multiple files
    dataparsing.contentparsing(response)
    st.success("✅ Terraform files generated successfully!")


# if st.button("🧠 Generate Terraform Code"):
#     with st.spinner("Generating Terraform code..."):
#         try:
#             # Pass the selected model ID to the function
#             response = (prompt, selected_model_full_id)
#             tf_blocks = extract_tf_blocks(response)
#             write_tf_files(tf_blocks)
#
#             st.success("✅ Terraform files generated successfully!")
#
#             for filename, code in tf_blocks.items():
#                 with st.expander(f"📄 {filename}", expanded=False):
#                     st.code(code.strip(), language="hcl")
#         except Exception as e:
#             st.error(f"❌ Error: {str(e)}")

# --- Terraform Commands ---
st.markdown("---")
st.subheader("⚙ Terraform Actions")


# --- Values file selection ---
terraform_dir = os.path.join(os.getcwd(), "terraform")

cloud_folder = st.selectbox("Select Cloud to run Terraform commands", [None, "modules/aws", "modules/azure", "modules/gcp"])

available_tfvars = [f for f in os.listdir(terraform_dir) if f.endswith(".tfvars")] if os.path.exists(terraform_dir) else []
selected_tfvars = st.multiselect("Select values file(s):", available_tfvars)

col1, col2, col3, col4, col5, col6 = st.columns(6)

if col1.button("📋 terraform plan"):
    with st.spinner("Running terraform plan...⏳"):
        cleanoutput = format.clean_output(terraform.run_terraform_command("plan", values_files=selected_tfvars, terraform_subfolder=cloud_folder))
        st.code(f"📝 Plan Output..\n {cleanoutput}", language="bash")

if col2.button("🚀 terraform apply"):
    with st.spinner("Running terraform apply...⏳"):
        st.code("📝 Apply Output", format.clean_output(terraform.run_terraform_command("apply", values_files=selected_tfvars), language="bash"))

if col3.button("💥 terraform destroy"):
    with st.spinner("Running terraform destroy...⏳"):
        st.code("📝 Destroy Output", format.clean_output(terraform.run_terraform_command("destroy", values_files=selected_tfvars), language="bash"))

if col4.button("✅ terraform validate"):
    with st.spinner("Running terraform validate...⏳"):
        cleanoutput = format.clean_output(terraform.run_terraform_command("validate", terraform_subfolder=cloud_folder))
        st.code(f"📝 Validate Output...\n {cleanoutput}", language="bash")

if col5.button("✨ terraform format"):
    with st.spinner("Running terraform format...⏳"):
        cleanoutput = format.clean_output(terraform.run_terraform_command("fmt", terraform_subfolder=cloud_folder))
        st.code(f"📝 Terraform format Output...\n {cleanoutput}",  language="bash")

if col6.button("📖 terraform explain"):
    with st.spinner("Running terraform explain...⏳"):
        cleanoutput = format.clean_output(terraform.terraform_explain("terraform", terraform_subfolder=cloud_folder, model_id=selected_model_full_id))
        st.code(f"📝 Explain Output...\n {cleanoutput}", language="bash")


# ========== Show User Inputs ==========
if prompt:
    st.subheader("📌 Captured Inputs")
    st.write("**User Prompt:**", prompt)


# --- Enhanced code with cicd
# === Jenkins Pipeline UI ===
st.subheader("🛠️ Jenkins Pipeline Generator")

pipeline_type = st.selectbox(
    "Choose pipeline type",
    ["jenkins-pr-pipeline", "jenkins-build-pipeline"]
)

jenkins_prompt = st.text_area(
    "Enter pipeline requirements:",
    placeholder="Example: checkout repo, run terraform fmt, terraform plan, build docker image, run unit tests..."
)

if st.button("Generate Jenkinsfile with Groq"):
    if not jenkins_prompt.strip():
        st.warning("⚠️ Please enter pipeline requirements before generating.")
    else:
        with st.spinner("Calling Groq to generate Jenkinsfile..."):
            try:
                messages = [
                    {"role": "system", "content": "You are a CI/CD assistant that writes production-ready Jenkins pipelines."},
                    {"role": "user", "content": f"Generate a {pipeline_type} Jenkinsfile with the following requirements:\n{jenkins_prompt}"}
                ]

                jenkins_code = agent.calling_groq(messages, selected_model_full_id)

                # store in session so it persists after rerun
                st.session_state["jenkins_code"] = jenkins_code

            except Exception as e:
                st.error(f"❌ Groq API call failed: {e}")

# Show editable Jenkinsfile if code exists
if "jenkins_code" in st.session_state:
    st.subheader("📜 Generated Jenkinsfile (editable)")

    # Editable text area so user can tweak before saving
    updated_code = st.text_area(
        "Review & Edit Jenkinsfile:",
        st.session_state["jenkins_code"],
        height=400
    )

    if st.button("✅ Save Jenkinsfile"):
        save_dir = "jenkins"
        os.makedirs(save_dir, exist_ok=True)

        # Save directly as "jenkins-pr-pipeline" or "jenkins-build-pipeline"
        filepath = os.path.join(save_dir, pipeline_type)

        with open(filepath, "w") as f:
            f.write(updated_code)

        # update session state with latest edits
        st.session_state["jenkins_code"] = updated_code

        st.success(f"🎉 Jenkinsfile saved to {filepath}")

# ========== GitOps Section ==========
st.subheader("📌 Git Commit & Push Changes")

branch = st.text_input("Branch to push changes to", "main")
commit_msg = st.text_input("Commit Message", "Update terraform & Jenkins pipelines")

username = st.text_input("Git Username")
token = st.text_input("Git Token", type="password")

if st.button("Commit & Push Terraform + Jenkins Changes"):
    try:
        # Select only terraform and jenkins folders for commit
        files_to_commit = []
        if os.path.exists(TERRAFORM_DIR):
              files_to_commit += [os.path.relpath(f, BASE_DIR) for f in glob.glob(f"{TERRAFORM_DIR}/**/*", recursive=True) if os.path.isfile(f)]

        if os.path.exists(JENKINS_DIR):
              files_to_commit += [os.path.relpath(f, BASE_DIR) for f in glob.glob(f"{JENKINS_DIR}/**/*", recursive=True) if os.path.isfile(f)]
        files_to_commit=None
        print(f"files to commit :- {files_to_commit}\n commit msg :- {commit_msg} \n branch :- {branch} \n username :- {username} \n token :- {token}")
        result = githelper.git_commit_push(files_to_commit, commit_msg, branch, username, token)
        st.success(result)
    except Exception as e:
        st.error(f"❌ Git commit/push failed: {e}")