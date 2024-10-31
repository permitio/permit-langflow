from langflow.custom import Component
from langflow.inputs import StrInput
from langflow.schema import Data
from langflow.template import Output


class CreateListComponent(Component):
    display_name = "Create List with diagnosis ID and Diagnosis"
    description = "Creates a list of diagnoses with diagnosis_id as metadata."
    icon = "list"
    name = "CreateListOfDiagnosis"

    inputs = [
        StrInput(
            name="diagnoses",
            display_name="Diagnoses with Diagnosis ID",
            info="Enter diagnoses in format 'diagnosis_id:diagnosis', one per line.",
            is_list=True,
        ),
    ]

    outputs = [
        Output(display_name="Data List", name="list", method="create_list"),
    ]

    def create_list(self) -> list[Data]:
        data = []
        for i, item in enumerate(self.diagnoses, start=1):
            parts = item.split(':', 1)
            if len(parts) != 2:
                raise ValueError(f"Invalid format in line {i}: '{item}'. Expected format: 'diagnosis_id:diagnosis'")
            
            diagnosis_id, diagnosis = parts
            diagnosis_id = diagnosis_id.strip()
            diagnosis = diagnosis.strip()
            
            if not diagnosis_id or not diagnosis:
                raise ValueError(f"Empty diagnosis_id or diagnosis in line {i}: '{item}'")
            
            data.append(Data(data={
                "text": diagnosis,
                "diagnosis_id": diagnosis_id
            }))
        
        self.status = data
        return data