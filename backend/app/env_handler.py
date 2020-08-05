from typing import Final
"""
A file for storing the keys that correspond to environment variables.
This helps with future names changes and prevents bad typing somewhere
deep in the code
"""
# Environment variable key for the hashing algorithm used for passwords
Hash_Alg_Env_Key: Final = "HASH_ALG"
# Environment variable key that represents the key used for hashing JWT tokens
Hash_Key_Env_Key: Final = "HASH_KEY"
# Environment variable key for TTL of JWT tokens, units are minutes
JWT_Token_TTL: Final = "JWT_Token_TTL"


