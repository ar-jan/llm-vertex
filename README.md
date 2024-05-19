# llm-vertex

LLM plugin to access Google Vertex AI (experiment, not packaged).

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/), following the steps under `Development`.

## Usage

### Set up Vertex AI

You will need a project id and an access token. The easiest way to get these seems to be to setup the gcloud CLI.

To display the access token, run: `gcloud auth print-access-token`.


### Run

Use the access token as llm key:

`llm keys set vertex`

Provide `LLM_VERTEX_LOCATION` and `LLM_VERTEX_PROJECT_ID` in your environment, e.g.:

`LLM_VERTEX_LOCATION=europe-west4 LLM_VERTEX_PROJECT_ID=yourprojectid-1234 llm --model gemini-1.5-pro-preview-0514 "How to calculate the circumference of a circle?"`


## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-vertex
python3 -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
llm install -e '.[test]'
```
To run the tests:
```bash
pytest
```
