from permit import Permit

from langflow.custom import Component
from langflow.io import MessageTextInput, Output
from langflow.schema import Data

class PermitFilterComponent(Component):
    display_name: str = "Resource Permission Filter"
    description = ("This component checks user permissions for resources and filters the list based on whether the user has the permission.")
    icon = "filter"
    name = "PermitFilter"

    inputs = [
        MessageTextInput(
            name="user",
            display_name="User Email",
            info="Email of the user whose permissions are to be checked.",
        ),
        MessageTextInput(
            name="action",
            display_name="Action",
            value="view",
        ),
        MessageTextInput(
            name="pdp_url",
            display_name="Permit PDP URL",
            info="URL of the Permit PDP service.",
        ),
        MessageTextInput(
            name="token",
            display_name="Permit Token",
            info="API token for Permit.",
        ),
        
        MessageTextInput(
            name="resource_name",
            display_name="Resource name",
            value="Diagnosis",
        ),
        MessageTextInput(
            name="resource_id",
            display_name="Resource ID key",
            value="diagnosis_id",
        ),
        DataInput(
            name="resources",
            display_name="Input resources",
            info="Collection of resources to check for permissions."
        ),
    ]

    outputs = [
        Output(display_name="Permitted Resources", name="permitted_resources", method="filter_resources")
    ]

    async def filter_resources(self) -> Data:
        required_fields = ['user', 'action', 'pdp_url', 'token', 'resources', 'resource_name', 'resource_id']
        
        if any(not getattr(self, field) for field in required_fields):
            raise ValueError(f"Missing required input fields: {', '.join(field for field in required_fields if not getattr(self, field))}")
    
        permit = Permit(pdp=self.pdp_url, token=self.token)
    
        try:
            check_results = await permit.bulk_check(
                {
                    "user": self.user,
                    "action": self.action,
                    "resource": f"{self.resource_name}:{getattr(item, self.resource_id, None)}",
                }
                for item in self.resources
            )
    
            return [
                resource for resource, result in zip(self.resources, check_results) if result
            ]
        except Exception as e:
            raise RuntimeError(f"Error during bulk check: {str(e)}") from e
