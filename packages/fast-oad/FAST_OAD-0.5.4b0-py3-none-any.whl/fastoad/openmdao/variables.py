"""
Module for managing OpenMDAO variables
"""
#  This file is part of FAST : A framework for rapid Overall Aircraft Design
#  Copyright (C) 2020  ONERA & ISAE-SUPAERO
#  FAST is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
from copy import deepcopy
from typing import Dict, Hashable, List, Union

import numpy as np
import openmdao.api as om
import pandas as pd
from importlib_resources import open_text
from openmdao.core.system import System

from . import resources
from .utils import get_unconnected_input_names

# Logger for this module
_LOGGER = logging.getLogger(__name__)

DESCRIPTION_FILENAME = "variable_descriptions.txt"
# Metadata that will be ignore when checking variable equality and when adding variable
# to an OpenMDAO component
METADATA_TO_IGNORE = [
    "is_input",
    "tags",
    "size",
    "src_indices",
    "src_slice",
    "flat_src_indices",
    "distributed",
    "res_units",  # deprecated in IndepVarComp.add_output() since OpenMDAO 3.2
    "lower",  # deprecated in IndepVarComp.add_output() since OpenMDAO 3.2
    "upper",  # deprecated in IndepVarComp.add_output() since OpenMDAO 3.2
    "ref",  # deprecated in IndepVarComp.add_output() since OpenMDAO 3.2
    "ref0",  # deprecated in IndepVarComp.add_output() since OpenMDAO 3.2
    "res_ref",  # deprecated in IndepVarComp.add_output() since OpenMDAO 3.2
    "ref",  # deprecated in IndepVarComp.add_output() since OpenMDAO 3.2
    "global_shape",
    "global_size",
    "discrete",  # currently inconsistent in openMDAO 3.4
    "prom_name",
    "desc",
]


class Variable(Hashable):
    """
    A class for storing data of OpenMDAO variables.

    Instantiation is expected to be done through keyword arguments only.

    Beside the mandatory parameter 'name, kwargs is expected to have keys
    'value', 'units' and 'desc', that are accessible respectively through
    properties :meth:`name`, :meth:`value`, :meth:`units` and :meth:`description`.

    Other keys are possible. They match the definition of OpenMDAO's method
    :meth:`Component.add_output` described
    `here <http://openmdao.org/twodocs/versions/latest/_srcdocs/packages/core/
    component.html#openmdao.core.component.Component.add_output>`_.

    These keys can be listed with class method :meth:`get_authorized_keys`.
    **Any other key in kwargs will be silently ignored.**

    Special behaviour: :meth:`description` will return the content of kwargs['desc']
    unless these 2 conditions are met:
     - kwargs['desc'] is None or 'desc' key is missing
     - a description exists in FAST-OAD internal data for the variable name
    Then, the internal description will be returned by :meth:`description`

    :param kwargs: the attributes of the variable, as keyword arguments
    """

    # Will store content of DESCRIPTION_FILE_PATH once and for all
    _variable_descriptions = {}

    # Default metadata
    _base_metadata = {}

    def __init__(self, name, **kwargs):
        super().__init__()

        self.name = name
        """ Name of the variable """

        self.metadata: Dict = {}
        """ Dictionary for metadata of the variable """

        # Initialize class attributes once at first instantiation -------------
        if not self._variable_descriptions:
            # Class attribute, but it's safer to initialize it at first instantiation
            with open_text(resources, DESCRIPTION_FILENAME) as desc_io:
                vars_descs = np.genfromtxt(desc_io, delimiter="\t", dtype=str)
            self.__class__._variable_descriptions.update(vars_descs)

        if not self._base_metadata:
            # Get variable base metadata from an ExplicitComponent
            comp = om.ExplicitComponent()
            # get attributes
            metadata = comp.add_output(name="a")

            self.__class__._base_metadata = metadata
            self.__class__._base_metadata["value"] = 1.0
            self.__class__._base_metadata["tags"] = set()
            self.__class__._base_metadata["shape"] = None
        # Done with class attributes ------------------------------------------

        # Feed self.metadata with kwargs, but remove first attributes with "Unavailable" as
        # value, which is a value that can be provided by OpenMDAO.
        self.metadata = self.__class__._base_metadata.copy()
        self.metadata.update(
            {
                key: value
                for key, value in kwargs.items()
                # The isinstance check is needed if value is a numpy array. In this case, a
                # FutureWarning is issued because it is compared to a scalar.
                if not isinstance(value, str) or value != "Unavailable"
            }
        )
        self._set_default_shape()

        # If no description, add one from DESCRIPTION_FILE_PATH, if available
        if not self.description and self.name in self._variable_descriptions:
            self.description = self._variable_descriptions[self.name]

    @classmethod
    def get_openmdao_keys(cls):
        """

        :return: the keys that are used in OpenMDAO variables
        """
        # As _base_metadata is initialized at first instantiation, we create an instance to
        # ensure it has been done
        cls("dummy")

        return cls._base_metadata.keys()

    @property
    def value(self):
        """ value of the variable"""
        return self.metadata.get("value")

    @value.setter
    def value(self, value):
        self.metadata["value"] = value
        self._set_default_shape()

    @property
    def units(self):
        """ units associated to value (or None if not found) """
        return self.metadata.get("units")

    @units.setter
    def units(self, value):
        self.metadata["units"] = value

    @property
    def description(self):
        """ description of the variable (or None if not found) """
        return self.metadata.get("desc")

    @description.setter
    def description(self, value):
        self.metadata["desc"] = value

    @property
    def is_input(self):
        """ I/O status of the variable.

        - True if variable is a problem input
        - False if it is an output
        - None if information not found
        """
        return self.metadata.get("is_input")

    @is_input.setter
    def is_input(self, value):
        self.metadata["is_input"] = value

    def _set_default_shape(self):
        """ Automatically sets shape if not set"""
        if self.metadata["shape"] is None:
            shape = np.shape(self.value)
            if not shape:
                shape = (1,)
            self.metadata["shape"] = shape

    def __eq__(self, other):
        # same arrays with nan are declared non equals, so we need a workaround
        my_metadata = dict(self.metadata)
        other_metadata = dict(other.metadata)
        my_value = np.asarray(my_metadata.pop("value"))
        other_value = np.asarray(other_metadata.pop("value"))

        # Let's also ignore unimportant keys
        for key in METADATA_TO_IGNORE:
            if key in my_metadata:
                del my_metadata[key]
            if key in other_metadata:
                del other_metadata[key]

        return (
            isinstance(other, Variable)
            and self.name == other.name
            and ((my_value == other_value) | (np.isnan(my_value) & np.isnan(other_value))).all()
            and my_metadata == other_metadata
        )

    def __repr__(self):
        return "Variable(name=%s, metadata=%s)" % (self.name, self.metadata)

    def __hash__(self) -> int:
        return hash("var=" + self.name)  # Name is normally unique


class VariableList(list):
    """
    Class for storing OpenMDAO variables

    A list of Variable instances, but items can also be accessed through variable names.

    There are 2 ways for adding a variable::

        # Assuming these Python variables are ready
        var_1 = Variable('var/1', value=0.)
        metadata_2 = {'value': 1., 'units': 'm'}

        # ... a VariableList instance can be populated like this
        vars = VariableList()
        vars.append(var_1)              # Adds directly a Variable instance
        vars['var/2'] = metadata_2      # Adds the variable with given name and given metadata

    After that, following equalities are True::

        print( var_1 in vars )
        print( 'var/1' in vars.names() )
        print( 'var/2' in vars.names() )

    Note:
        Adding a Variable instance that has a name that is already in the VariableList instance
        will replace the previous Variable instance instead of adding a new one.
    """

    def names(self) -> List[str]:
        """
        :return: names of variables
        """
        return [var.name for var in self]

    def metadata_keys(self) -> List[str]:
        """
        :return: the metadata keys that are common to all variables in the list
        """
        keys = list(self[0].metadata.keys())
        for var in self:
            keys = [key for key in var.metadata.keys() if key in keys]
        return keys

    def append(self, var: Variable) -> None:
        """
        Append var to the end of the list, unless its name is already used. In that case, var
        will replace the previous Variable instance with the same name.
        """
        if not isinstance(var, Variable):
            raise TypeError("VariableList items should be Variable instances")

        if var.name in self.names():
            self[self.names().index(var.name)] = var
        else:
            super().append(var)

    def update(self, other_var_list: "VariableList", add_variables: bool = False):
        """
        Uses variables in other_var_list to update the current VariableList instance.

        For each Variable instance in other_var_list:
            - if a Variable instance with same name exists, it is replaced by the one
              in other_var_list
            - if not, Variable instance from other_var_list will be added only if
              add_variables==True

        :param other_var_list: source for new Variable data
        :param add_variables: if True, variables can be added instead of just updated
        """

        for var in other_var_list:
            if add_variables or var.name in self.names():
                self.append(var)

    def to_ivc(self) -> om.IndepVarComp:
        """
        :return: an OpenMDAO IndepVarComp instance with all variables from current list
        """
        ivc = om.IndepVarComp()
        for variable in self:
            attributes = variable.metadata.copy()
            value = attributes.pop("value")
            # Some attributes are not compatible with add_output
            for attr in METADATA_TO_IGNORE:
                if attr in attributes:
                    del attributes[attr]
            ivc.add_output(variable.name, value, **attributes)

        return ivc

    def to_dataframe(self) -> pd.DataFrame:
        """
        Creates a DataFrame instance from a VariableList instance.

        Column names are "name" + the keys returned by :meth:`Variable.get_authorized_keys`.
        Values in Series "value" are floats or lists (numpy arrays are converted).

        :return: a pandas DataFrame instance with all variables from current list
        """
        var_dict = {"name": []}
        var_dict.update({metadata_name: [] for metadata_name in self.metadata_keys()})

        # To be able to edit floats and integer
        def _check_shape(value):
            if np.shape(value) == (1,):
                value = float(value[0])
            elif np.shape(value) == ():
                pass
            else:
                value = np.asarray(value).tolist()
            return value

        for variable in self:
            value = _check_shape(variable.value)
            var_dict["name"].append(variable.name)
            for metadata_name in self.metadata_keys():
                if metadata_name == "value":
                    var_dict["value"].append(value)
                else:
                    # TODO: make this more generic
                    if metadata_name in ["value", "initial_value", "lower", "upper"]:
                        metadata = _check_shape(variable.metadata[metadata_name])
                    else:
                        metadata = variable.metadata[metadata_name]
                    var_dict[metadata_name].append(metadata)

        df = pd.DataFrame.from_dict(var_dict)

        return df

    @classmethod
    def from_ivc(cls, ivc: om.IndepVarComp) -> "VariableList":
        """
        Creates a VariableList instance from an OpenMDAO IndepVarComp instance

        :param ivc: an IndepVarComp instance
        :return: a VariableList instance
        """
        variables = VariableList()

        ivc = deepcopy(ivc)
        om.Problem(ivc).setup()  # Need setup to have get_io_metadata working

        for name, metadata in ivc.get_io_metadata(
            metadata_keys=["value", "units", "upper", "lower"]
        ).items():
            metadata = metadata.copy()
            value = metadata.pop("value")
            if np.shape(value) == (1,):
                value = float(value[0])
            elif np.shape(value) == ():
                pass
            else:
                value = np.asarray(value)
            metadata.update({"value": value})
            variables[name] = metadata

        return variables

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> "VariableList":
        """
        Creates a VariableList instance from a pandas DataFrame instance.

        The DataFrame instance is expected to have column names "name" + some keys among the ones given by
        :meth:`Variable.get_authorized_keys`.

        :param df: a DataFrame instance
        :return: a VariableList instance
        """
        column_names = [name for name in df.columns]

        # To be able to edit floats and integer
        def _check_shape(value):
            if np.shape(value) == (1,):
                value = float(value[0])
            elif np.shape(value) == ():
                if type(value) == str:
                    value = float(value)
                else:
                    # Integer
                    pass
            else:
                value = np.asarray(value).tolist()
            return value

        def _get_variable(row):
            var_as_dict = {key: val for key, val in zip(column_names, row)}
            # TODO: make this more generic
            for key, val in var_as_dict.items():
                if key in ["value", "initial_value", "lower", "upper"]:
                    var_as_dict[key] = _check_shape(val)
                else:
                    pass
            return Variable(**var_as_dict)

        return VariableList([_get_variable(row) for row in df[column_names].values])

    @classmethod
    def from_system(cls, system: System) -> "VariableList":
        """
        Creates a VariableList instance containing inputs and outputs of a an OpenMDAO System.
        The inputs (is_input=True) correspond to the variables of IndepVarComp
        components and all the unconnected variables.

        Warning: setup() must NOT have been called.

        In the case of a group, if variables are promoted, the promoted name
        will be used. Otherwise, the absolute name will be used.

        :param system: OpenMDAO Component instance to inspect
        :return: VariableList instance
        """

        problem = om.Problem()
        if isinstance(system, om.Group):
            problem.model = deepcopy(system)
        else:
            # problem.model has to be a group
            problem.model.add_subsystem("comp", deepcopy(system), promotes=["*"])

        problem.setup()
        return VariableList.from_problem(problem, use_initial_values=True)

    @classmethod
    def from_problem(
        cls, problem: om.Problem, use_initial_values: bool = False, get_promoted_names=True,
    ) -> "VariableList":
        """
        Creates a VariableList instance containing inputs and outputs of a an OpenMDAO Problem.

        .. warning::

            problem.setup() must have been run.

        The inputs (is_input=True) correspond to the variables of IndepVarComp
        components and all the unconnected variables.

        If variables are promoted, the promoted name will be used. Otherwise (and if
        promoted_only is False), the absolute name will be used.

        .. note::

            Variables from _auto_ivc are ignored.

        :param problem: OpenMDAO Problem instance to inspect
        :param use_initial_values: if True, returned instance will contain values before computation
        :param get_promoted_names: if True, only promoted variable names will be returned
        :return: VariableList instance
        """
        variables = VariableList()

        model = problem.model

        # Determining global inputs

        # from unconnected inputs
        mandatory_unconnected, optional_unconnected = get_unconnected_input_names(
            problem, promoted_names=True
        )
        unconnected_inputs = mandatory_unconnected + optional_unconnected

        # from ivc outputs
        ivc_inputs = []
        for subsystem in model.system_iter():
            if isinstance(subsystem, om.IndepVarComp):
                if subsystem.name != "_auto_ivc":  # Exclude vars from _auto_ivc
                    input_variables = cls.from_ivc(subsystem)
                    for var in input_variables:
                        ivc_inputs.append(var.name)

        global_inputs = unconnected_inputs + ivc_inputs

        for abs_name, metadata in model.get_io_metadata(
            metadata_keys=["value", "units", "upper", "lower"], return_rel_names=False
        ).items():

            # Exclude vars from _auto_ivc
            if abs_name.startswith("_auto_ivc."):
                continue

            prom_name = metadata["prom_name"]

            if not (get_promoted_names and prom_name == abs_name):
                if get_promoted_names and prom_name in variables.names():
                    # In case we get promoted names, several variables can match the same
                    # promoted name, with possibly different declaration for default values.
                    # We retain the first non-NaN value with defined units. If no units is
                    # ever defined, the first non-NaN value is kept.
                    # A non-NaN value with no units will be retained against a NaN value with
                    # defined units.

                    if np.all(np.isnan(variables[prom_name].value)) and metadata["units"] is None:
                        # Current variable can add no data.
                        continue

                    if (
                        not np.all(np.isnan(variables[prom_name].value))
                        and variables[prom_name].units is not None
                    ):
                        # We already have a non-NaN value with defined units for current promoted
                        # name. No need for using the current variable.
                        continue

                    if not np.all(np.isnan(variables[prom_name].value)) and np.all(
                        np.isnan(metadata["value"])
                    ):
                        # We already have a non-NaN value and current variable has a NaN value and
                        # can only add information about units. We keep the non-NaN value
                        continue

                metadata = metadata.copy()  # a copy is needed because we will modify it

                # Setting type (IN or OUT)
                if prom_name in global_inputs:
                    metadata.update({"is_input": True})
                else:
                    metadata.update({"is_input": False})

                variable = Variable(name=prom_name, **metadata)
                if not use_initial_values:
                    try:
                        # Maybe useless, but we force units to ensure it is consistent
                        variable.value = problem.get_val(prom_name, units=variable.units)
                    except RuntimeError:
                        # In case problem is incompletely set, problem.get_val() will fail.
                        # In such case, falling back to the method for initial values
                        # should be enough.
                        pass
                variables.append(variable)

        return variables

    @classmethod
    def from_unconnected_inputs(
        cls, problem: om.Problem, with_optional_inputs: bool = False
    ) -> "VariableList":
        """
        Creates a VariableList instance containing unconnected inputs of an OpenMDAO Problem.

        .. warning::

            problem.setup() must have been run.

        If *optional_inputs* is False, only inputs that have numpy.nan as default value (hence
        considered as mandatory) will be in returned instance. Otherwise, all unconnected inputs
        will be in returned instance.

        :param problem: OpenMDAO Problem instance to inspect
        :param with_optional_inputs: If True, returned instance will contain all unconnected inputs.
                                Otherwise, it will contain only mandatory ones.
        :return: VariableList instance
        """
        variables = VariableList()

        mandatory_unconnected, optional_unconnected = get_unconnected_input_names(problem)
        model = problem.model

        # processed_prom_names will store promoted names that have been already processed, so that
        # it won't be stored twice.
        # By processing mandatory variable first, a promoted variable that would be mandatory
        # somewhere and optional elsewhere will be retained as mandatory (and associated value
        # will be NaN), which is fine.
        # For promoted names that link to several optional variables and no mandatory ones,
        # associated value will be the first encountered one, and this is as good a choice as any
        # other.
        processed_prom_names = []

        io_metadata = model.get_io_metadata(
            metadata_keys=["value", "units"], return_rel_names=False
        )

        def _add_outputs(unconnected_names):
            """ Fills ivc with data associated to each provided var"""
            for abs_name in unconnected_names:
                prom_name = io_metadata[abs_name]["prom_name"]
                if prom_name not in processed_prom_names:
                    processed_prom_names.append(prom_name)
                    metadata = deepcopy(io_metadata[abs_name])
                    metadata.update({"is_input": True})
                    variables[prom_name] = metadata

        _add_outputs(mandatory_unconnected)
        if with_optional_inputs:
            _add_outputs(optional_unconnected)

        return variables

    def __getitem__(self, key) -> Variable:
        if isinstance(key, str):
            return self[self.names().index(key)]
        else:
            return super().__getitem__(key)

    def __setitem__(self, key, value):
        if isinstance(key, str):
            if isinstance(value, dict):
                if key in self.names():
                    self[key].metadata = value
                else:
                    self.append(Variable(key, **value))
            else:
                raise TypeError(
                    'VariableList can be set with a "string index" only if value is a '
                    "dict of metadata"
                )
        elif not isinstance(value, Variable):
            raise TypeError("VariableList items should be Variable instances")
        else:
            super().__setitem__(key, value)

    def __delitem__(self, key):
        if isinstance(key, str):
            del self[self.names().index(key)]
        else:
            super().__delitem__(key)

    def __add__(self, other) -> Union[List, "VariableList"]:
        if isinstance(other, VariableList):
            return VariableList(super().__add__(other))
        else:
            return super().__add__(other)
