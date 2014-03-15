#!/usr/bin/env python
import json
import requests

github_url = "https://api.github.com/user/repos"
data = json.dumps({'name': 'test', 'description': 'some test repo'})
r = requests.post(github_url, data, auth=('user', '*****'))

print r.json
