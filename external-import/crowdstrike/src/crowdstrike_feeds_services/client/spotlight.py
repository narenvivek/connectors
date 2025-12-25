# -*- coding: utf-8 -*-
"""CrowdStrike Spotlight API client."""

from typing import Any, Dict, List, Optional
from .base_api import BaseCrowdstrikeClient


class SpotlightAPI(BaseCrowdstrikeClient):
    """API client for CrowdStrike Spotlight vulnerabilities."""

    def __init__(self, helper):
        """Initialize Spotlight API client."""
        super().__init__(helper)

    def get_vulnerabilities(
        self,
        limit: int,
        offset: int,
        filter_query: Optional[str] = None,
        sort: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get vulnerabilities from Spotlight API.
        
        :param limit: Maximum number of records to return
        :param offset: Starting index for pagination
        :param filter_query: FQL query to filter results
        :param sort: Sort order (e.g., 'created_timestamp|desc')
        :return: Dict object containing API response
        """
        params = {
            "limit": limit,
            "offset": offset,
        }
        
        if filter_query:
            params["filter"] = filter_query
        if sort:
            params["sort"] = sort

        # Use FalconPy's command method for Spotlight API
        response = self.cs_intel.command(
            action="queryCombinedVulnerabilities",
            parameters=params
        )

        self.handle_api_error(response)
        self.helper.connector_logger.info(
            f"Fetched {len(response.get('body', {}).get('resources', []))} vulnerabilities from Spotlight API"
        )

        return response["body"]

    def get_vulnerability_details(self, cve_ids: List[str]) -> Dict[str, Any]:
        """
        Get detailed information for specific CVE IDs.
        
        :param cve_ids: List of CVE IDs to query
        :return: Dict object containing API response
        """
        response = self.cs_intel.command(
            action="getCombinedVulnerabilities",
            ids=cve_ids
        )

        self.handle_api_error(response)
        self.helper.connector_logger.info(
            f"Fetched details for {len(cve_ids)} vulnerabilities"
        )

        return response["body"]
