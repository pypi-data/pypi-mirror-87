import dataclasses
from typing import List


@dataclasses.dataclass
class AgilicusScopes:
    applications: List[str]
    audits: List[str]
    catalogues: List[str]
    challenges: List[str]
    diagnostics: List[str]
    files: List[str]
    issuers: List[str]
    messages: List[str]
    metrics: List[str]
    orgs: List[str]
    sysgroups: List[str]
    traffic_tokens: List[str]
    users: List[str]
    permissions: List[str]

    def to_list(self):
        scopes = []
        for endpoint, scope_list in self.__dict__.items():
            # Translate _ to - since we're representing these as python vars
            endpoint_name = endpoint.replace("_", "-")
            for scope in scope_list:
                scopes.append(f"urn:agilicus:api:{endpoint_name}:{scope}")

        return scopes


# Please keep this list in sync with the one in
# portal/src/app/core/services/auth-service.service.ts
DEFAULT_SCOPES = AgilicusScopes(
    applications=["viewer?", "reader?", "owner?"],
    audits=["owner?"],
    catalogues=["viewer?", "reader?", "owner?"],
    challenges=["self?"],
    diagnostics=["owner?"],
    files=["owner?"],
    issuers=["owner?"],
    messages=["self?"],
    metrics=["viewer?", "owner?"],
    orgs=["owner?"],
    permissions=[],
    sysgroups=["owner?"],
    traffic_tokens=["user?", "owner?"],
    users=["self?", "viewer?", "owner?"],
).to_list()

# For readibility please keep this list in alphabetical order
ADMIN_SCOPES = AgilicusScopes(
    applications=["creator?"],
    audits=["creator?"],
    catalogues=["creator?"],
    challenges=["creator?"],
    diagnostics=["creator?"],
    files=["creator?"],
    issuers=["creator?"],
    messages=["creator?"],
    metrics=["creator?"],
    orgs=["creator?"],
    permissions=["creator?"],
    sysgroups=["creator?"],
    traffic_tokens=["creator?"],
    users=["creator?"],
).to_list()


def get_default_scopes():
    return DEFAULT_SCOPES


def get_admin_scopes():
    return ADMIN_SCOPES
