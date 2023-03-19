from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

@app.route("/generate_ppt", methods=["POST"])
def generate_ppt():
    user_input = request.json.get("user_input")

    # Replace with your Azure Databricks workspace details
    domain = "https://adb-5976771229466627.7.azuredatabricks.net"
    token = "dapi1b7700dffe48b29d4d16386bf046c490-3"

    # Run a notebook in the Azure Databricks environment
    response = requests.post(
        f"{domain}/api/2.0/jobs/run-now",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "job_id": 923724153236391,  # Replace with your job ID
            "notebook_params": {"user_input": user_input},
        },
    )

    run_id = response.json()["run_id"]

    # Check the job status periodically and wait for it to finish
    status = "RUNNING"
    while status == "RUNNING":
        response = requests.get(
            f"{domain}/api/2.0/jobs/runs/get",
            headers={"Authorization": f"Bearer {token}"},
            params={"run_id": run_id},
        )
        status = response.json()["state"]["life_cycle_state"]

    if status == "TERMINATED":
    # Return the downloaded PowerPoint file path
    pptx_path = response.json()["state"]["result_state"]
    pptx_filename = os.path.basename(pptx_path)
    return jsonify({"success": True, "pptx_filename": pptx_filename})
else:
    return jsonify({"success": False})


@app.route("/download_ppt")
def download_ppt():
    pptx_filename = request.args.get("pptx_filename")
    pptx_path = os.path.join("/dbfs", pptx_filename)
    return send_from_directory("/dbfs", pptx_path, as_attachment=True, attachment_filename="generated_presentation.pptx")


if __name__ == "__main__":
    app.run()
