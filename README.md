# cereals

This project shows how AWS secrets can be loaded from AWS secret manager during dagster repository initialization, and then used by resources such as IO Managers.

To get started:

```
pip install -e ".[dev]"
```

The key function is in `repository.py`:

```
#  This function will load environment variables from 
#  AWS secrets if they are not already set
from .utils.load_aws_secrets import load_aws_secret
# load a secret stored as a key-value string by name
# if the secret is KEY=VALUE 
# the result is an environment variable KEY set to VALUE
load_aws_secret("aws-snowflake-password")

# load a secret that is a simple string
# if the secret is VALUE 
# the result is an environment variable SNOWFLAKE_USER set to VALUE
load_aws_secret("SNOWFLAKE_USER")
```