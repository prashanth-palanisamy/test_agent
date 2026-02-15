import streamlit as st
import os
import glob
from agent import agent,dataparsing,format,modelsearch,terraform, githelper  # Import your existing functions

BASE_DIR = os.getcwd()
TERRAFORM_DIR = os.path.join(BASE_DIR, "terraform")
JENKINS_DIR = os.path.join(BASE_DIR, "jenkins")

# --- PAGE CONFIG ---
st.set_page_config(page_title="DevOps Agent Hub", page_icon="🤖", layout="wide")

# --- INITIALIZE SESSION STATE ---
if "iac_prompt" not in st.session_state:
    st.session_state["iac_prompt"] = ""

if "jenkins_prompt" not in st.session_state:
    st.session_state["jenkins_prompt"] = ""

# --- BEAUTIFICATION (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .stTextInput>div>div>input { border-radius: 5px; }
    .agent-header { color: #1E3A8A; font-size: 24px; font-weight: bold; border-bottom: 2px solid #1E3A8A; padding-bottom: 10px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)


# --- AGENT FUNCTIONS ---
def iac_agent():
    st.markdown('<div class="agent-header">🏗️ IAC-Agent (Terraform)</div>', unsafe_allow_html=True)
    # Paste your existing Terraform generation/editing logic here
    # global prompt
    prompt = st.text_area("📥 Enter Terraform Request", height=180, placeholder="e.g., VPC with 2 public subnets...", key="_temp_iac_prompt")
    # st.write(st.session_state.iac_prompt)
    st.session_state["iac_prompt"] = st.session_state["_temp_iac_prompt"]
    message = [{
        "role": "user",
        "content": prompt,
    }
    ]

    if st.button("🧠 Generate Terraform code"):
        st.subheader("Generated Terraform Code")
        # Calling LLM to fetch data
        response = agent.calling_groq(message, model_id="llama-3.3-70b-versatile")

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

    cloud_folder = st.selectbox("Select Cloud to run Terraform commands",
                                [None, "modules/aws", "modules/azure", "modules/gcp"])

    available_tfvars = [f for f in os.listdir(terraform_dir) if f.endswith(".tfvars")] if os.path.exists(
        terraform_dir) else []
    selected_tfvars = st.multiselect("Select values file(s):", available_tfvars)

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    if col1.button("📋 terraform plan"):
        with st.spinner("Running terraform plan...⏳"):
            cleanoutput = format.clean_output(
                terraform.run_terraform_command("plan", values_files=selected_tfvars, terraform_subfolder=cloud_folder))
            st.code(f"📝 Plan Output..\n {cleanoutput}", language="bash")

    if col2.button("🚀 terraform apply"):
        with st.spinner("Running terraform apply...⏳"):
            st.code("📝 Apply Output",
                    format.clean_output(terraform.run_terraform_command("apply", values_files=selected_tfvars),
                                        language="bash"))

    if col3.button("💥 terraform destroy"):
        with st.spinner("Running terraform destroy...⏳"):
            st.code("📝 Destroy Output",
                    format.clean_output(terraform.run_terraform_command("destroy", values_files=selected_tfvars),
                                        language="bash"))

    if col4.button("✅ terraform validate"):
        with st.spinner("Running terraform validate...⏳"):
            cleanoutput = format.clean_output(
                terraform.run_terraform_command("validate", terraform_subfolder=cloud_folder))
            st.code(f"📝 Validate Output...\n {cleanoutput}", language="bash")

    if col5.button("✨ terraform format"):
        with st.spinner("Running terraform format...⏳"):
            cleanoutput = format.clean_output(terraform.run_terraform_command("fmt", terraform_subfolder=cloud_folder))
            st.code(f"📝 Terraform format Output...\n {cleanoutput}", language="bash")

    if col6.button("📖 terraform explain"):
        with st.spinner("Running terraform explain...⏳"):
            cleanoutput = format.clean_output(terraform.terraform_explain("terraform", terraform_subfolder=cloud_folder,
                                                                          model_id="llama-3.3-70b-versatile"))
            st.code(f"📝 Explain Output...\n {cleanoutput}", language="bash")
    st.info("Manage your Infrastructure as Code templates and configurations.")


def jenkins_agent():
    st.markdown('<div class="agent-header">🚀 Jenkins-Agent</div>', unsafe_allow_html=True)
    if "iac_prompt" in st.session_state and st.session_state.iac_prompt:
        st.info(f"📋 **Prompt from IAC-Agent:** {st.session_state.iac_prompt}")
    else:
        st.warning("No prompt found from IAC-Agent yet.")

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
                        {"role": "system",
                         "content": "You are a CI/CD assistant that writes production-ready Jenkins pipelines."},
                        {"role": "user",
                         "content": f"Generate a {pipeline_type} Jenkinsfile with the following requirements:\n{jenkins_prompt}"}
                    ]

                    jenkins_code = agent.calling_groq(messages, model_id="llama-3.3-70b-versatile")

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

    st.info("Automate your CI/CD pipelines with generated Jenkinsfiles.")


def git_ops_agent():
    st.markdown('<div class="agent-header">📦 Git-Ops Agent</div>', unsafe_allow_html=True)

    # BEAUTIFIED GIT SECTION (Using your existing githelper logic)
    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("Git Username", placeholder="e.g. prashanth-palanisamy")
        branch = st.text_input("Target Branch", "test")
    with col2:
        token = st.text_input("Git PAT Token", type="password")
        commit_msg = st.text_input("Commit Message", "Update from Agent")

    if st.button("🚀 Execute Commit & Push"):
        try:
            # Select only terraform and jenkins folders for commit
            files_to_commit = []
            if os.path.exists(TERRAFORM_DIR):
                files_to_commit += [os.path.relpath(f, BASE_DIR) for f in
                                    glob.glob(f"{TERRAFORM_DIR}/**/*", recursive=True) if os.path.isfile(f)]

            if os.path.exists(JENKINS_DIR):
                files_to_commit += [os.path.relpath(f, BASE_DIR) for f in
                                    glob.glob(f"{JENKINS_DIR}/**/*", recursive=True) if os.path.isfile(f)]
            files_to_commit = None
            print(
                f"files to commit :- {files_to_commit}\n commit msg :- {commit_msg} \n branch :- {branch} \n username :- {username} \n token :- {token}")
            result = githelper.git_commit_push(files_to_commit, commit_msg, branch, username, token)
            st.success(result)
        except Exception as e:
            st.error(f"❌ Git commit/push failed: {e}")


# --- NAVIGATION SETUP ---
pg = st.navigation([
    st.Page(iac_agent, title="IAC-Agent", icon="🏗️"),
    # st.Page(jenkins_agent, title="Jenkins-Agent", icon="🚀"),
    st.Page(git_ops_agent, title="Git-Ops Agent", icon="📦"),
])

pg.run()