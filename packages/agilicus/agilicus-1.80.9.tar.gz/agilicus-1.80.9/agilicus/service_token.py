from datetime import datetime
from datetime import timedelta
from datetime import timezone
import jwt

from . import tokens
import agilicus
import agilicus_api


class Token:
    """Class for managing token lifecycle for service accounts."""

    def __init__(
        self=None,
        org_id=None,
        user_id=None,
        auth_issuer_url=None,
        auth_expiry_secs=None,
        scope=None,
        client_id=None,
        referer=None,
        auth_doc=None,
        api_config=None,
        auth_doc_static=False,
        **kwargs,
    ):
        self.org_id = org_id
        self.user_id = user_id
        self.auth_issuer_url = auth_issuer_url
        self.auth_expiry_secs = auth_expiry_secs
        self.client_id = client_id
        self.api_config = api_config
        self.tokens_api = agilicus_api.TokensApi(agilicus.ApiClient(api_config))
        self.referer = referer
        self.scope = scope
        self.token = None
        self.auth_doc = auth_doc
        self.auth_doc_static = auth_doc_static

    def is_expired(self):
        if not self.token:
            return True
        if datetime.now(timezone.utc) > self.token_expiry:
            return True

    def set_access_token(self, token):
        self.api_config.access_token = token

    def set_token(self, token):
        self.token = token
        _token_dict = jwt.decode(self.token, verify=False)
        _exp = datetime.fromtimestamp(_token_dict["exp"], tz=timezone.utc)
        _iat = datetime.fromtimestamp(_token_dict["iat"], tz=timezone.utc)
        # grab a new token when expiry is half expired
        self.token_expiry = _iat + ((_exp - _iat) / 2)

    def get_auth_document_expiry(self):
        if self.auth_doc:
            if isinstance(self.auth_doc["spec"]["expiry"], str):
                return datetime.fromisoformat(self.auth_doc["spec"]["expiry"])
            else:
                return self.auth_doc["spec"]["expiry"]

    def valid_user(self):
        if not self.auth_doc:
            return False

        # no user_id/org_id, we take the spec as is
        if not self.user_id and not self.org_id:
            return True

        spec = self.auth_doc["spec"]
        if spec["user_id"] == self.user_id and spec["org_id"] == self.org_id:
            return True
        return False

    def get_auth_document(self):
        if self.auth_doc and self.valid_user():
            if self.auth_doc["spec"]["expiry"]:
                if isinstance(self.auth_doc["spec"]["expiry"], str):
                    expiry = datetime.fromisoformat(self.auth_doc["spec"]["expiry"])
                else:
                    expiry = self.auth_doc["spec"]["expiry"]

                if datetime.now(timezone.utc) < expiry:
                    return self.auth_doc
            else:
                # no expiry in doc
                return self.auth_doc

        if self.auth_doc_static:
            if not self.valid_user():
                raise Exception(
                    "Static authentication document has mismatched requested org/user"
                )
            else:
                raise Exception("Static authentication document has expired")

        auth_expiry = None
        if self.auth_expiry_secs:
            auth_expiry = str(
                datetime.now(timezone.utc) + timedelta(seconds=self.auth_expiry_secs)
            )

        spec = agilicus_api.AuthenticationDocumentSpec(
            org_id=self.org_id,
            user_id=self.user_id,
            auth_issuer_url=self.auth_issuer_url,
            expiry=auth_expiry,
        )
        model = agilicus_api.AuthenticationDocument(spec=spec)
        self.auth_doc = self.tokens_api.create_authentication_document(model).to_dict()
        return self.auth_doc

    def get(self):
        if self.is_expired():
            _token = tokens.create_service_token(
                self.get_auth_document(),
                verify=self.api_config.ssl_ca_cert,
                scope=self.scope,
                client_id=self.client_id,
                referer=self.referer,
            )
            self.set_token(_token["access_token"])
        return self.token
