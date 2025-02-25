# 🌍 Terraburst

**Terraform "Smarter", and Parallelized** 🚀

Terraburst is a CLI tool that supercharges your Terraform workflows by running **Terraform plans in parallel** across multiple projects. It automates workspace selection, runs pre- and post-execution commands, and ensures **Terraform plan files** are saved both in your project folder and in the current working directory.

---

## ✨ Features
✅ **Parallel Execution** – Run Terraform plans across multiple directories simultaneously.
 
✅ **Workspace-Aware** – Automatically selects the right workspace for each project.

✅ **Custom Hooks** – Define `before_plan` and `after_plan` commands to automate additional tasks.

✅ **Plan File Management** – Saves Terraform plan files in both your project directory and the current working directory.

✅ **Seamless Configuration** – Each Terraform project can have its own `terraburst.yml` configuration file.

✅ **Global Configuration** – Use a global `terraform-main.yaml` file to manage multiple projects.

✅ **Plan Validation** – Classifies and validates Terraform plan changes based on impact.

---

## 📦 Installation

Make sure you have Python installed, then install Terraburst (there's no pip package yet):

```sh
git clone git@github.com:AnthraxisBR/terraburst.git
cd terraburst
pip install -e .
```

---

## 🚀 Getting Started

### 1️⃣ Create a Configuration File
Each Terraform project should have a `terraburst.yml` file with the following structure:

```yaml
workspace: production
var_file: vars.json  # Optional
output_file: output  # Optional
variables:  # Optional
  - name: action
    value: plan
before_plan:
  - terraform init
  - echo "Preparing Terraform"
after_plan:
  - echo "Plan completed!"
```

### 2️⃣ Create a Global Configuration File
You can also create a global `terraburst-main.yaml` file to manage multiple projects:

```yaml
projects:
  - name: infrastructure-core
    projects:
     - name: terraform-project-1
       project_path: projects/terraform-project-1
       workspace: production
       var_file: vars.json
       output_file: output
       variables:
         - name: action
           value: plan
       before_plan:
         - terraform init
         - echo "Preparing Terraform"
       after_plan:
         - echo "Plan completed!"
     - name: terraform-project-2
       project_path: projects/terraform-project-2
       workspace: production
       var_file: vars.json
       output_file: output
       variables:
         - name: action
           value: plan
       before_plan:
         - terraform init
         - echo "Preparing Terraform"
       after_plan:
         - echo "Plan completed!"
```

### 3️⃣ Run Terraburst
From the root directory containing multiple Terraform projects, execute:

```sh
terraburst -d ./environments -c 3
```

This will:
1. **Find all Terraform projects** inside `./environments`.
2. **Execute Terraform plans in parallel** (3 at a time, based on `-c 3`).
3. **Run any before/after commands** specified in `terraburst.yml`.
4. **Save the Terraform plan files** in both locations:
   - `./environments/my-project/terraburst_plan`
   - `./terraburst_plan_my-project`

### 4️⃣ Validate Terraform Plan
To validate a Terraform plan, execute:

```sh
terraburst validate -p planfile
```

This will:
1. **Load the Terraform plan** from the specified file.
2. **Classify and validate changes** based on their impact.
3. **Output a summary** of the validation results.

---

## 🔧 Advanced Usage

### 💨 Increase Parallel Execution
If you want to speed things up even more, increase the concurrency:

```sh
terraburst -d ./environments -c 5
```

### 🔄 Apply Instead of Plan
Terraburst currently runs `terraform plan`, but you can modify the configuration to execute `terraform apply` after reviewing the plan manually.

Or, you can add the `apply` command to the `after_plan` section (be careful with this!):

```yaml
after_plan:
  - terraform apply -auto-approve
```

---

## 📌 Running a Specific Project from a Global Configuration

If you want to execute Terraform plans for a **specific project** defined in your `terraburst-main.yaml` file, use the following command:

```sh
terraburst plan -tc terraburst-main.yaml -c 2 --project infrastructure-core
```

### What This Command Does:
✅ **Uses `terraburst-main.yaml` as the configuration file** (`-tc terraburst-main.yaml`).

✅ **Limits parallel execution to 2 projects at a time** (`-c 2`).

✅ **Runs only the `infrastructure-core` project** (`--project infrastructure-core`).

This approach is useful when you have multiple Terraform projects and only need to run plans for a specific set of them while maintaining efficiency and avoiding unnecessary execution.

---

## 🎯 Why Use Terraburst?
- **No More Waiting** – Parallel execution speeds up your Terraform workflow.
- **Less Manual Work** – Automatically selects workspaces and executes pre/post commands.
- **Consistent Plan Storage** – Keeps Terraform plans in both project and root directories.
- **Easy to Integrate** – Works with any existing Terraform project structure.
- **Change Validation** – Ensures changes are classified and validated based on their impact.

---

## 🛠️ Contributing

Want to add features or fix bugs? Fork the repo, create a branch, and open a PR! Contributions are always welcome.

