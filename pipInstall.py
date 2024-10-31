import subprocess
from typing import Optional

from langflow.custom import Component
from langflow.inputs import StrInput
from langflow.template import Output
from langflow.schema.message import Message

class PipInstallComponent(Component):
    display_name: str = "Pip Install"
    description: str = "Installs a specified Python library using pip."
    icon = "download"

    inputs = [
        StrInput(
            name="library_name",
            display_name="Library Name",
            info="The name of the Python library to install.",
            value="permit",
        ),
    ]

    outputs = [
        Output(display_name="Installation Status", name="status", method="install_library"),
    ]

    def install_library(self) -> Message:
        try:
            # Run the pip install command
            result = subprocess.run(
                ["pip", "install", self.library_name],
                capture_output=True,
                text=True,
                check=True
            )
            # Capture the output and set it as the status
            self.status = f"Successfully installed {self.library_name}\n{result.stdout}"
        except subprocess.CalledProcessError as e:
            # Handle the error case
            self.status = f"Failed to install {self.library_name}\n{e.stderr}"
        
        return Message(text=self.status)
