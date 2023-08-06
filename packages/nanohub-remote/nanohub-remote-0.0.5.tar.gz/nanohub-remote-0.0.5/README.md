# Nanohubtools

A set of tools/apps to run on nanohub

## Installation


```bashv
pip install nanohub-remote
```

## Usage


```python

import nanohub.remote as nr
auth_data = {
  'client_id': XXXXXXXX,
  'client_secret': XXXXXXXX,
  'grant_type': 'password',
  'username': XXXXXXXX,
  'password': XXXXXXXX
}

# to get username and password, register on nanohub.org (https://nanohub.org/register/)
# to get client id and secret, create a web application (https://nanohub.org/developer/api/applications/new), use "https://127.0.0.1" as Redirect URL

session = nr.Session(auth_data)

```

## Available Nanohub Points

## Tools

```python
TOOLNAME = '' # valid Nanoohub tool name e.g. pntoy
tool = nr.Tool(auth_data)

# Get Available input parameters
params = tool.getToolParameters(TOOLNAME)

# Submit a simulation experiment
job_id = tool.submitTool(params)

# Check Status
status = tool.checkStatus(job_id['job_id'])

# Get Results
results = tool.getResults(job_id['job_id'])

# Submit an wait for results
results = tool.submitTool(params, wait_results=True)
```
