from flask import Flask, render_template, request
import requests
import base64


def RestApi(ticket):
    organization = 'oyn1szh'
    project = 'CICT_TryRun'
    pipelineId = '1'

    # Azure Pipelines API URL
    url = f"https://dev.azure.com/{organization}/{project}/_apis/pipelines/{pipelineId}/runs?&api-version=7.2-preview.1"

    # Replace 'your-pat' with your actual PAT
    pat = "cvkdqwkjadg6mjgsgzf5x7gda6qjlgphzihwm3b557sor53dt3nq"
    credentials = base64.b64encode(f":{pat}".encode()).decode()

    # Headers with PAT for authentication
    headers = {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/json"
    }

    Container_check_ticket_ID = ticket  # FVGIIICAEO-843

    # POST request payload
    payload = {
        "resources": {
            "repositories": {
                "self": {
                    "refName": "refs/heads/main"  # Set branch name
                }
            }
        },
        "templateParameters": {  # Add parameters
            "ticket": Container_check_ticket_ID
        },
        "variables": {}
    }
    # Send POST request to trigger the pipeline
    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        print("Pipeline triggered successfully!")
    else:
        print("Failed to trigger the pipeline:", response.text)
        print(response.status_code)
        

app = Flask(__name__)

@app.route("/index",methods=["GET","POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        ticket = request.form.get('ticket')
        print(ticket)
        RestApi(ticket)
        return 'Pipeline triggered successfully!' 
if __name__ == '__main__':
    app.run(port=8000)