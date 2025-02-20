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
workspace: production (required)
var_file: vars.json (optional)
output_file: output (optional)
variables: (optional)
  - name: action
    value: plan
before_plan:
  - terraform init (optional)
  - echo "Preparing Terraform" (optional)
after_plan:
  - echo "Plan completed!" (optional)
```

### 2️⃣ Run Terraburst
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

## 🎯 Why Use Terraburst?
- **No More Waiting** – Parallel execution speeds up your Terraform workflow.
- **Less Manual Work** – Automatically selects workspaces and executes pre/post commands.
- **Consistent Plan Storage** – Keeps Terraform plans in both project and root directories.
- **Easy to Integrate** – Works with any existing Terraform project structure.

---

## 🛠️ Contributing
Want to add features or fix bugs? Fork the repo, create a branch, and open a PR! Contributions are always welcome.

---
