# llm-vertex

[![PyPI](https://img.shields.io/pypi/v/llm-vertex.svg)](https://pypi.org/project/llm-vertex/)
[![Changelog](https://img.shields.io/github/v/release/ar-jan/llm-vertex?include_prereleases&label=changelog)](https://github.com/ar-jan/llm-vertex/releases)
[![Tests](https://github.com/ar-jan/llm-vertex/actions/workflows/test.yml/badge.svg)](https://github.com/ar-jan/llm-vertex/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/ar-jan/llm-vertex/blob/main/LICENSE)

LLM plugin to access Google Vertex AI.

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-vertex
```
## Usage

### Set up Vertex AI

You will need a project id and an access token. The easiest way to get these seems to be to setup the gcloud CLI.

To display the access token, run: `gcloud auth print-access-token`.


### Run

Use the access token as llm key:

`llm keys set vertex`

Provide LLM_VERTEX_LOCATION and LLM_VERTEX_PROJECT_ID in your environment, e.g.:

`LLM_VERTEX_LOCATION=europe-west4 LLM_VERTEX_PROJECT_ID=yourprojectid-1234`


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
