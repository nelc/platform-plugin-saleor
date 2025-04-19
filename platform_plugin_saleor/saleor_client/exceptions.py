"""Exceptions for Saleor GraphQL client."""

import json
from typing import Any, Dict, Optional, Sequence


class GraphQLError(Exception):
    """
    Raised on Saleor GraphQL errors
    """

    def __init__(
        self,
        errors: Sequence[Dict[str, Any]],
        response_data: Optional[Dict[str, Any]] = None,
    ):
        self.errors = errors
        self.response_data = response_data

    def __str__(self):
        errors_str = (
            f"GraphQL errors: {json.dumps(self.errors, indent=2)}"
            if self.errors
            else ""
        )
        response_data_str = (
            f"Response data: {json.dumps(self.response_data, indent=2)}"
            if self.response_data
            else ""
        )
        return f"{errors_str}{response_data_str}"
