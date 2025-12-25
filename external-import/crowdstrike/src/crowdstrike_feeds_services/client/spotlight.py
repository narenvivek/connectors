# -*- coding: utf-8 -*-
"""CrowdStrike Spotlight API client."""

import requests
from typing import Any, Dict, Optional
from falconpy import OAuth2
from ..utils.config_variables import ConfigCrowdstrike


class SpotlightAPI:
    """API client for CrowdStrike Spotlight vulnerabilities."""

    def __init__(self, helper):
        """Initialize Spotlight API client."""
        self.config = ConfigCrowdstrike()
        self.helper = helper
        self.base_url = self.config.base_url
        self.oauth = OAuth2(
            client_id=self.config.client_id,
            client_secret=self.config.client_secret,
            base_url=self.base_url,
        )
        self.token = None

    def _get_token(self) -> str:
        """Get OAuth2 access token."""
        if not self.token:
            result = self.oauth.token()
            self.token = result["body"]["access_token"]
        return self.token

    def get_vulnerabilities(
        self,
        limit: int,
        offset: int,
        filter_query: Optional[str] = None,
        sort: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get vulnerabilities from Spotlight combined API."""
        params = {
            "limit": limit,
            "offset": offset,
            "filter": filter_query,
        }
        if sort:
            params["sort"] = sort

        headers = {
            "Authorization": f"Bearer {self._get_token()}",
            "Accept": "application/json",
        }

        response = requests.get(
            f"{self.base_url}/spotlight/combined/vulnerabilities/v1",
            headers=headers,
            params=params,
        )
        
        if response.status_code >= 400:
            error_msg = f"API error {response.status_code}: {response.text}"
            self.helper.connector_logger.error(
                "[API] Error fetching vulnerabilities",
                {"error": error_msg},
            )
            return {"resources": [], "meta": {}}
        
        body = response.json()
        resources = body.get("resources", [])
        self.helper.connector_logger.info(
            f"Fetched {len(resources)} vulnerabilities from Spotlight API"
        )

        return body
