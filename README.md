# Secret Rotation Automation

This repository contains a project for automating the rotation of secrets. The project includes a YAML file listing all the secret names that need to be manually rotated, a GitHub Action that runs nightly to check the secrets, and a Grafana Cloud alert to notify if the issue is not addressed within the SLA.

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone https://github.com/githubnext/workspace-blank.git
   cd workspace-blank
   ```

2. **Create a `secrets.yaml` file:**
   ```yaml
   secrets:
     - name: "database_password"
       target_date: "2023-12-01"
     - name: "api_key"
       target_date: "2023-12-15"
     - name: "encryption_key"
       target_date: "2023-12-20"
   ```

3. **Set up GitHub Actions:**
   - Create a `.github/workflows/rotate-secrets.yml` file with the following content:
     ```yaml
     name: Rotate Secrets

     on:
       schedule:
         - cron: "0 0 * * *" # Runs nightly at midnight

     jobs:
       rotate-secrets:
         runs-on: ubuntu-latest

         steps:
           - name: Checkout repository
             uses: actions/checkout@v2

           - name: Set up Python
             uses: actions/setup-python@v2
             with:
               python-version: '3.x'

           - name: Install dependencies
             run: |
               python -m pip install --upgrade pip
               pip install requests

           - name: Rotate secrets
             run: |
               python .github/scripts/rotate_secrets.py
     ```

4. **Set up Grafana Cloud API:**
   - Follow the instructions on the [Grafana Cloud API documentation](https://grafana.com/docs/grafana-cloud/reference/api/) to create an API key and configure the GitHub Action to use it.

5. **Run the GitHub Action:**
   - The GitHub Action will run nightly and check the secrets. If a secret is approaching its target date, it will trigger a Grafana Cloud alert if the issue is not addressed within the SLA.

## Contributing

Please refer to the `CONTRIBUTING.md` file for guidelines on how to contribute to this project.

## License

This project is licensed under the terms of the `LICENSE` file.
