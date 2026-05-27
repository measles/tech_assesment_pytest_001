"""Module for parsing and storing credentials grouped by organization and role."""

import os
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


class Role(Enum):
    """Enumeration for user roles."""

    ADMIN = "admin"
    USER = "user"


@dataclass
class Creds:
    """Dataclass to store email and password."""

    email: str
    password: str


@dataclass
class Organization:
    """Dataclass to store credentials for an organization."""

    name: str
    admin: Optional[Creds] = None
    user: Optional[Creds] = None


def load_credentials(file_path="CREDENTIALS.txt") -> Dict[str, Organization]:
    """
    Reads credentials from a file or environment variable and groups them by organization (SLD) and role.
    - Admin: email starts with 'admin'
    - User: others
    - Organization: second-level domain (e.g., 'org-alpha' from 'admin@org-alpha.com')
    """
    orgs: Dict[str, Organization] = {}
    lines = []

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    else:
        env_creds = os.getenv("CREDENTIALS")
        if env_creds:
            # Handle both newline and literal '\n' characters in env var
            lines = env_creds.replace("\\n", "\n").splitlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "," in line:
            email, password = [s.strip() for s in line.split(",", 1)]

            # Extract organization name (SLD)
            # admin@org-alpha.com -> domain: org-alpha.com -> sld: org-alpha
            try:
                domain = email.split("@")[1]
                org_name = domain.split(".")[0]
            except IndexError:
                continue  # Skip malformed emails

            if org_name not in orgs:
                orgs[org_name] = Organization(name=org_name)

            # Determine role and assign creds
            if email.lower().startswith("admin"):
                orgs[org_name].admin = Creds(email=email, password=password)
            else:
                orgs[org_name].user = Creds(email=email, password=password)

    return orgs
