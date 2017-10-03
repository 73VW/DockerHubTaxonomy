import requests
import json

repo = "library/nginx"
login_template = "https://auth.docker.io/token?service=registry.docker.io&scope=repository:{repository}:pull"
token = requests.get(login_template.format(repository=repo), json=True).json()["token"]

tag = "latest"
registry_end_point = "https://registry.hub.docker.com"
get_manifest_template = "{registry_end_point}/v2/{repository}/manifests/{tag}"
resp = requests.get(
    get_manifest_template.format(registry_end_point=registry_end_point, repository=repo, tag=tag),
    headers={"Authorization": "Bearer {}".format(token)}
)

manifest = resp.text
if resp.status_code is 200:
    print(manifest)
else:
    print(resp.status_code)
