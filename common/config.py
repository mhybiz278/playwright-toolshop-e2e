"""Environment configuration.

Base URLs come from the environment so the same suite runs against a local
stack, a review app or production without a code change — the Jenkins jobs set
them per environment. Defaults point at a locally running Toolshop.
"""
import os

BASE_URL = os.getenv("BASE_URL", "http://localhost:4200").rstrip("/")
API_URL = os.getenv("API_URL", "http://localhost:8091").rstrip("/")

# Deliberately low. Retries hide flake, they do not fix it; anything that needs
# a second attempt gets investigated instead of a higher number here.
DEFAULT_TIMEOUT_MS = 10_000
