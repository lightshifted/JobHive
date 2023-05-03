from pprint import pprint
from typing import Any, Dict, List
import json
import os
from datetime import datetime
from typing import Optional

from langchain.callbacks import CallbackManager, StdOutCallbackHandler

class ConsolePrettyPrintManager(CallbackManager):
    def __init__(self, handlers: List[StdOutCallbackHandler] = None):
        super().__init__(handlers=handlers)
        self.handlers.append(ConsolePrettyPrinter())


class ConsolePrettyPrinter(StdOutCallbackHandler):
    def __init__(
        self, file_path: Optional[str] = "./client_data/agent_interactions",
    ):
        super().__init__()
        self.file_path = file_path

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        super().on_chain_end(outputs, **kwargs)
        pprint(outputs)
        if isinstance(outputs, dict):
            file_name = f"output_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        else:
            return

        if self.file_path:
            file_name = os.path.join(self.file_path, file_name)

        with open(file_name, 'w') as f:
            json.dump(outputs, f, indent=4)

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        super().on_chain_start(serialized, inputs, **kwargs)
        if isinstance(inputs, dict):
            file_name = f"input_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        else:
            return

        if self.file_path:
            file_name = os.path.join(self.file_path, file_name)

        with open(file_name, 'w') as f:
            json.dump(inputs, f, indent=4)

        pprint(inputs)
