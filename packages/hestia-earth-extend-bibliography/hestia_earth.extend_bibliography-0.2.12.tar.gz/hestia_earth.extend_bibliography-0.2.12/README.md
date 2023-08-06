# Hestia Extend Bibliography

## Install

```bash
pip install hestia_earth.extend_bibliography
```

### Usage

```python
from hestia_earth.extend_bibliography import extend

# nodes is a Dict {nodes: []}
result = extend(
  nodes,
  # pass in the desired crendentials for each API
  mendeley_username=MENDELEY_USERNAME, mendeley_password=MENDELEY_PASSWORD, # enable Mendeley
  wos_api_key=WOS_API_KEY, # enable WoS REST API
  wos_api_user=WOS_API_USER, wos_api_pwd=WOS_API_PASSWORD, # enable WoS SOAP API
  enable_crossref=False, # enable CrossRef as last fallback (slower)
  max_workers=2, # enable multi-threading, 1 thread by default
)
```
