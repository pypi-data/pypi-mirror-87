# This file is part of Flatplan.
#
# Flatplan is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Flatplan is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Flatplan.  If not, see <https://www.gnu.org/licenses/>.

from copy import deepcopy
from json import loads, dumps
from logging import Logger
from typing import Any, List, Optional
from .logging import setup_logger


class Flattener:
    """
    A class that can be used to flatten Terraform plans in JSON format.

    ...

    Methods
    -------
    flatten() -> str :
        flattens the plan and returns the processed result
    """

    _plan: Any
    _logger: Logger

    def __init__(self, json_plan: str, logger: Optional[Logger] = None) -> None:
        """
        Constructs all the necessary attributes for the Flattener object.

        Parameters
        ----------
        json_plan : str
            the terraform plan in JSON format

        logger : logging.Logger, optional
            the logger object to be used
        """
        self._plan = loads(json_plan)
        self._logger = (
            logger if logger is not None else setup_logger("plan-flattener", debug=True)
        )

    def _flatten_child_modules(self, modules: List) -> List:
        """
        Recursively traverses the plan and creates a list with all resources found in child modules.

        Parameters
        ----------
        modules : List
            List of modules from JSON field 'planned_values.root_module.child_modules'

        Returns
        -------
        resources : List
        """
        resources = []

        for module in modules:
            module_address = (
                module["address"] if "address" in module.keys() else "unknown"
            )

            if "resources" in module.keys():
                for resource in module["resources"]:
                    resource_address = (
                        resource["address"]
                        if "address" in resource.keys()
                        else "unknown"
                    )
                    self._logger.debug(f"Adding resource: {resource_address}")
                    resources.append(deepcopy(resource))
            else:
                self._logger.debug(f"No resources found in module: {module_address}")

            if "child_modules" in module.keys():
                resources.extend(self._flatten_child_modules(module["child_modules"]))
            else:
                self._logger.debug(
                    f"No child modules found in module: {module_address}"
                )

        return resources

    def _flatten_providers(self) -> List:
        """
        Traverses the plan and creates a list with all providers found.

        Parameters
        ----------
        None.

        Returns
        -------
        providers : List
        """
        providers = []

        if "configuration" in self._plan.keys():
            configuration = self._plan["configuration"]

            if "provider_config" in configuration.keys():
                provider_config = configuration["provider_config"]

                for provider in provider_config.values():
                    provider_name = (
                        provider["name"] if "name" in provider.keys() else "unknown"
                    )
                    self._logger.debug(f"Adding provider: {provider_name}")
                    providers.append(deepcopy(provider))
            else:
                self._logger.warning(
                    "Plan does not have 'provider_config' section under 'configuration'"
                )
        else:
            self._logger.warning("Plan does not have 'configuration' section")

        return providers

    def _flatten_resources(self) -> List:
        """
        Traverses the plan and creates a list with all resources found.

        Parameters
        ----------
        None.

        Returns
        -------
        resources : List
        """
        resources = []

        if "planned_values" in self._plan.keys():
            planned_values = self._plan["planned_values"]

            if "root_module" in planned_values.keys():
                root_module = planned_values["root_module"]

                if "resources" in root_module.keys():
                    for resource in root_module["resources"]:
                        resource_address = (
                            resource["address"]
                            if "address" in resource.keys()
                            else "unknown"
                        )
                        self._logger.debug(f"Adding resource: {resource_address}")
                        resources.append(deepcopy(resource))
                else:
                    self._logger.warning(
                        "Plan does not have 'resources' section under 'root_module'"
                    )

                if "child_modules" in root_module.keys():
                    child_modules_resources = self._flatten_child_modules(
                        root_module["child_modules"]
                    )
                    resources.extend(child_modules_resources)
                else:
                    self._logger.debug(
                        "Plan does not have 'child_modules' section under 'root_module'"
                    )
            else:
                self._logger.warning(
                    "Plan does not have 'root_module' section under 'planned_values'"
                )
        else:
            self._logger.warning("Plan does not have 'planned_values' section")

        return resources

    def flatten(self) -> str:
        """
        Traverses the plan and creates a new flattened plan with all resources and providers found.

        Parameters
        ----------
        None.

        Returns
        -------
        flattened_plan : str
        """
        self._logger.debug("Flattening providers")
        providers = self._flatten_providers()

        self._logger.debug("Flattening resources")
        resources = self._flatten_resources()

        flattened_plan = dumps({"providers": providers, "resources": resources})

        return flattened_plan
