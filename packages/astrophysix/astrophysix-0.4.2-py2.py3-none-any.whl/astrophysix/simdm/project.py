# -*- coding: utf-8 -*-
# This file is part of the 'astrophysix' Python package.
#
# Copyright © Commissariat a l'Energie Atomique et aux Energies Alternatives (CEA)
#
#  FREE SOFTWARE LICENCING
#  -----------------------
# This software is governed by the CeCILL license under French law and abiding by the rules of distribution of free
# software. You can use, modify and/or redistribute the software under the terms of the CeCILL license as circulated by
# CEA, CNRS and INRIA at the following URL: "http://www.cecill.info". As a counterpart to the access to the source code
# and rights to copy, modify and redistribute granted by the license, users are provided only with a limited warranty
# and the software's author, the holder of the economic rights, and the successive licensors have only limited
# liability. In this respect, the user's attention is drawn to the risks associated with loading, using, modifying
# and/or developing or reproducing the software by the user in light of its specific status of free software, that may
# mean that it is complicated to manipulate, and that also therefore means that it is reserved for developers and
# experienced professionals having in-depth computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling the security of their systems and/or data
# to be ensured and, more generally, to use and operate it in the same conditions as regards security. The fact that
# you are presently reading this means that you have had knowledge of the CeCILL license and that you accept its terms.
#
#
# COMMERCIAL SOFTWARE LICENCING
# -----------------------------
# You can obtain this software from CEA under other licencing terms for commercial purposes. For this you will need to
# negotiate a specific contract with a legal representative of CEA.
#
"""
@startwbs

+ Simulation study
 + Project
  + Simulations
   + Simulation codes
    +_ RAMSES
    +_ AREPO
   +_ [RAMSES] Simulation #1
    + Generic results
     +_ Generic Result #1
      + Datafiles
       +_ Star formation history plot
     +_ Result #2
    + Snapshots
     +_ Snapshot #234
      + Datafiles
       +_ Gas density 2D map
        +_ 'rho_dens.png' PNG file
        +_ 'rho_slice.fits' FITS file
       +_ Star formation radial 1D profile
     +_ Snapshot #587
    + Post-processing runs
     + Post-processing codes
      +_ RadMC
     +_ [RadMC] Post-pro. run #1 (Simulation #2)
      + Generic results
       +_ Synthetic observed map
        + Datafiles
   +_ [AREPO] Simulation #2

@endwbs
"""
from __future__ import print_function, unicode_literals, division, absolute_import  # Python 2 and 3 compatibility

from enum import Enum

from future.builtins import str, list
import logging

from astrophysix.utils.persistency import Hdf5StudyPersistent
from .utils import ObjectList, GalacticaValidityCheckMixin
from astrophysix.utils.strings import Stringifiable
from .experiment import Simulation
from .protocol import SimulationCode, PostProcessingCode


__doc__ = """

.. autoclass:: astrophysix.simdm.ProjectCategory
   :members:
   :undoc-members:

.. autoclass:: astrophysix.simdm.Project
   :members:
   :undoc-members:

"""


log = logging.getLogger("astrophysix.simdm")


class ProjectCategory(Enum):
    """
    Project category enum

    Example
    -------
        >>> cat = ProjectCategory.PlanetaryAtmospheres
        >>> cat.verbose_name
        "Planetary atmospheres"
    """
    SolarMHD = ("SOLAR_MHD", "Solar Magnetohydrodynamics")
    PlanetaryAtmospheres = ("PLANET_ATMO", "Planetary atmospheres")
    StarPlanetInteractions = ("STAR_PLANET_INT", "Star-planet interactions")
    StarFormation = ("STAR_FORM", "Star formation")
    Supernovae = ("SUPERNOVAE", "Supernovae")
    GalaxyFormation = ("GAL_FORMATION", "Galaxy formation")
    GalaxyMergers = ("GAL_MERGERS", "Galaxy mergers")
    Cosmology = ("COSMOLOGY", "Cosmology")

    def __init__(self, alias, verbose):
        self._alias = alias
        self._verbose = verbose

    @property
    def alias(self):
        """Project category alias"""
        return self._alias

    @property
    def verbose_name(self):
        """Project category verbose name"""
        return self._verbose

    @classmethod
    def from_alias(cls, alias):
        """

        Parameters
        ----------
        alias: :obj:`string`
            project category alias

        Returns
        -------
        c: :class:`~astrophysix.simdm.ProjectCategory`
            Project category matching the requested alias.

        Raises
        ------
        ValueError
            if requested alias does not match any project category.

        Example
        -------
            >>> c = ProjectCategory.from_alias("STAR_FORM")
            >>> c.verbose_name
            "Star formation"
            >>> c2 = ProjectCategory.from_alias("MY_UNKNOWN_CATEGORY")
            ValuerError: No ProjectCategory defined with the alias 'MY_UNKNOWN_CATEGORY'.
        """
        for cat in cls:
            if cat.alias == alias:
                return cat
        raise ValueError("No ProjectCategory defined with the alias '{a:s}'.".format(a=alias))


class Project(Hdf5StudyPersistent, GalacticaValidityCheckMixin, Stringifiable):
    """
    Project (Simulation data model)

    Parameters
    ----------
    category: :class:`~astrophysix.simdm.ProjectCategory` or :obj:`string`
        project category or project category alias (mandatory)
    project_title: :obj:`string`
        project title (mandatory)
    alias: :obj:`string`
        Project alias (if defined, 16 max characters is recommended)
    short_description: :obj:`string`
        project short description
    general_description: :obj:`string`
        (long) project description
    data_description: :obj:`string`
        available data description in the project
    directory_path: :obj:`string`
        project directory path
    """
    def __init__(self, *args, **kwargs):
        uid = kwargs.pop("uid", None)
        super(Project, self).__init__(uid=uid)

        self._category = ProjectCategory.StarFormation
        self._title = ""
        self._short_description = ""
        self._general_description = ""
        self._data_description = ""
        self._alias = ""
        self._directory_path = ""

        self._simulations = ObjectList(Simulation, "name")

        if "category" not in kwargs:
            raise AttributeError("Project 'category' attribute is not defined (mandatory).")
        self.category = kwargs["category"]

        if "project_title" not in kwargs:
            raise AttributeError("Project 'project_title' attribute is not defined (mandatory).")
        self.project_title = kwargs["project_title"]

        if "alias" in kwargs:
            self.alias = kwargs["alias"]

        if "short_description" in kwargs:
            self.short_description = kwargs["short_description"]

        if "general_description" in kwargs:
            self.general_description = kwargs["general_description"]

        if "data_description" in kwargs:
            self.data_description = kwargs["data_description"]

        if "directory_path" in kwargs:
            self.directory_path = kwargs["directory_path"]

    def __eq__(self, other):
        """
        Project comparison method

        other: :class:`~astrophysix.simdm.Project`
            project to compare to.
        """
        if not super(Project, self).__eq__(other):
            return False

        if self._category != other.category:
            return False

        if self._title != other.project_title:
            return False

        if self._alias != other.alias:
            return False

        if self._short_description != other.short_description:
            return False

        if self._general_description != other.general_description:
            return False

        if self._data_description != other.data_description:
            return False

        if self._directory_path != other.directory_path:
            return False

        if self._simulations != other.simulations:
            return False

        return True

    def __ne__(self, other):  # Not an implied relationship between "rich comparison" equality methods in Python 2.X
        return not self.__eq__(other)

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_cat):
        try:
            scat = Stringifiable.cast_string(new_cat)
            self._category = ProjectCategory.from_alias(scat)
        except ValueError as  ve:
            log.error(str(ve))
            raise AttributeError(str(ve))
        except TypeError:
            if not isinstance(new_cat, ProjectCategory):
                err_msg = "Project 'category' attribute is not a valid ProjectCategory enum value."
                log.error(err_msg)
                raise AttributeError(err_msg)
            self._category = new_cat

    @property
    def project_title(self):
        return self._title

    @project_title.setter
    def project_title(self, new_title):
        try:
            self._title = Stringifiable.cast_string(new_title, valid_empty=False)
        except TypeError:
            err_msg = "Project 'project_title' property is not a valid (non empty) string."
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def alias(self):
        return self._alias

    @alias.setter
    def alias(self, new_alias):
        try:
            self._alias = Stringifiable.cast_string(new_alias)
        except TypeError:
            err_msg = "Project 'alias' property is not a valid string"
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def short_description(self):
        """Short description of the project"""
        return self._short_description

    @short_description.setter
    def short_description(self, new_descr):
        try:
            self._short_description = Stringifiable.cast_string(new_descr)
        except TypeError:
            err_msg = "Project 'short_description' property is not a valid string"
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def general_description(self):
        """General description of the project"""
        return self._general_description

    @general_description.setter
    def general_description(self, new_descr):
        try:
            self._general_description = Stringifiable.cast_string(new_descr)
        except TypeError:
            err_msg = "Project 'general_description' property is not a valid string"
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def data_description(self):
        """Data description available in this project"""
        return self._data_description

    @data_description.setter
    def data_description(self, new_descr):
        try:
            self._data_description = Stringifiable.cast_string(new_descr)
        except TypeError:
            err_msg = "Project 'data_description' property is not a valid string"
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def directory_path(self):
        """Project data directory path"""
        return self._directory_path

    @directory_path.setter
    def directory_path(self, new_path):
        try:
            self._directory_path = Stringifiable.cast_string(new_path)
        except TypeError:
            err_msg = "Project 'directory_path' property is not a valid string"
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def simulations(self):
        """Project :class:`~astrophysix.simdm.experiment.Simulation` list
        (:class:`~astrophysix.simdm.utils.ObjectList`)"""
        return self._simulations

    def _simu_codes(self):
        """Simulation codes iterator"""
        puid_list = []
        for simu in self._simulations:
            p = simu.simulation_code
            if p.uid not in puid_list:
                puid_list.append(p.uid)
                yield p

    def _post_pro_codes(self):
        """Post-processing codes iterator"""
        ppcode_uid_list = []
        for simu in self._simulations:
            for pprun in simu.post_processing_runs:
                p = pprun.postpro_code
                if p.uid not in ppcode_uid_list:
                    ppcode_uid_list.append(p.uid)
                    yield p

    @property
    def _target_objects(self):
        """Target object iterator"""
        # TODO
        to_uid_list = []
        for simu in self._simulations:
            yield None

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize a Project object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the Project into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write() : write UUID, etc.
        super(Project, self)._hsp_write(h5group, **kwargs)

        # If necessary, call callback function with project name
        self._hsp_write_callback(str(self), **kwargs)

        # Write project title
        self._hsp_write_attribute(h5group, ('title', self._title), **kwargs)

        # Write project category alias
        self._hsp_write_attribute(h5group, ('category', self._category.alias), **kwargs)

        # Write project Galactica alias, if defined
        self._hsp_write_attribute(h5group, ('galactica_alias', self._alias), **kwargs)

        # Write project directory path, if defined
        self._hsp_write_attribute(h5group, ('project_directory', self._directory_path), **kwargs)

        # Write project short/general/data description
        self._hsp_write_attribute(h5group, ('short_description', self._short_description), **kwargs)
        self._hsp_write_attribute(h5group, ('general_description', self._general_description), **kwargs)
        self._hsp_write_attribute(h5group, ('data_description', self._data_description), **kwargs)

        # Write protocol directory
        if kwargs.get("from_project", False):  # Write protocol list in project subgroup (not in each experiment)
            proto_group = self._hsp_get_or_create_h5group(h5group, "PROTOCOLS", **kwargs)
            self._hsp_write_object_list(proto_group, "SIMU_CODES", self._simu_codes, "simu_code_", **kwargs)
            self._hsp_write_object_list(proto_group, "PPRUN_CODES", self._post_pro_codes, "pprun_code_", **kwargs)

        # Write all target objects
        # if kwargs.get("from_project", False):
        #     self._hsp_write_object_list(h5group, "TARGET_OBJECTS", self._target_objects, "targobj_", **kwargs)

        # Write all simulations
        self._hsp_write_object_list(h5group, "SIMULATIONS", self._simulations, "simu_", **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read a Project object from a HDF5 file (*.h5).

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to read the object from.
        version: ``int``
            version of the object to read.
        dependency_objdict: ``dict``
            dependency object dictionary. Default None

        Returns
        -------
        proj: ``Project``
            Read Project instance
        """
        # Handle different versions here

        # Fetch Hdf5StudyPersistent object UUID
        uid = super(Project, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Create Project instance with mandatory attributes
        t = cls._hsp_read_attribute(h5group, "title", "project title")
        cat = cls._hsp_read_attribute(h5group, "category", "project category")
        proj = cls(uid=uid, category=cat, project_title=t)

        # ------------------------------------------ Optional attributes --------------------------------------------- #
        # Read Galactica alias
        alias = cls._hsp_read_attribute(h5group, "galactica_alias", "project Galactica alias",
                                        raise_error_if_not_found=False)
        if alias is  not None:
            proj.alias = alias
        # Read project directory
        dpath = cls._hsp_read_attribute(h5group, "project_directory", "project directory",
                                        raise_error_if_not_found=False)
        if dpath is not None:
            proj.directory_path = dpath
        # Read project short/general/data description
        ddescr = cls._hsp_read_attribute(h5group, "data_description", "project data description",
                                         raise_error_if_not_found=False)
        if ddescr is not None:
            proj.data_description = ddescr
        gdescr = cls._hsp_read_attribute(h5group, "general_description", "project general description",
                                         raise_error_if_not_found=False)
        if gdescr is not None:
            proj.general_description = gdescr
        sdescr = cls._hsp_read_attribute(h5group, "short_description", "project short description",
                                         raise_error_if_not_found=False)
        if sdescr is not None:
            proj.short_description = sdescr
        # ------------------------------------------------------------------------------------------------------------ #

        # Build dependency object dictionary indexed by their class name
        dod = {}
        if "PROTOCOLS" in h5group:
            protgroup = h5group["PROTOCOLS"]
            # Build simulation code dictionary indexed by their UUID
            if "SIMU_CODES" in protgroup:
                simu_code_dict = {}
                for simu_code in SimulationCode._hsp_read_object_list(protgroup, "SIMU_CODES", "simu_code_",
                                                                      "simulation code"):
                    simu_code_dict[simu_code.uid] = simu_code

                dod[SimulationCode.__name__] = simu_code_dict

            # Build post-processing code dictionary indexed by their UUID
            if "PPRUN_CODES" in protgroup:
                pprun_code_dict = {}
                for pprun_code in PostProcessingCode._hsp_read_object_list(protgroup, "PPRUN_CODES", "pprun_code_",
                                                                           "post-processing code"):
                    pprun_code_dict[pprun_code.uid] = pprun_code

                dod[PostProcessingCode.__name__] = pprun_code_dict

        # Build simulation list and add each simulation into project
        if "SIMULATIONS" in h5group:
            for simu in Simulation._hsp_read_object_list(h5group, "SIMULATIONS", "simu_", "project simulation",
                                                         dependency_objdict=dod):
                proj.simulations.add(simu)

        return proj

    def galactica_validity_check(self, **kwargs):
        """
        Perform validity checks on this  instance and eventually log warning messages.

        Parameters
        ----------
        kwargs: `dict`
            keyword arguments (optional)
        """
        # Check project alias
        if len(self.alias) == 0:
            log.warning("{p!s} Galactica alias is missing.".format(p=self))
        elif len(self._alias) > 16:
            log.warning("{p!s} Galactica alias is too long (max. 16 characters).".format(p=self))
        else:
            err_msg = self.galactica_valid_alias(self._alias)
            if err_msg is not None:
                log.warning("{p!s} Galactica alias is not valid ({m:s})".format(p=self, m=err_msg))

        # Check project title
        if len(self._title) == 0:
            log.warning("{p!s} Galactica project title is missing.".format(p=self))
        elif len(self._title) > 128:
            log.warning("{p!s} Galactica project title is too long (max. 128 characters).".format(p=self))

        # Check project short description
        if len(self._short_description) == 0:
            log.warning("{p!s} Galactica short description is missing.".format(p=self))
        elif len(self._short_description) > 256:
            log.warning("{p!s} Galactica short description is too long (max. 256 characters).".format(p=self))

        # Check project post-processing/simulation code validity + protocol alias unicity
        code_names = {}
        for scode in self._simu_codes():
            scode.galactica_validity_check()
            if len(scode.alias) > 0:
                if scode.alias in code_names:
                    log.warning("{c1!s} and {c2!s} protocols share the same alias. They must be "
                                "unique.".format(c1=code_names[scode.alias], c2=scode))
                else:
                    code_names[scode.alias] = scode
        for pcode in self._post_pro_codes():
            pcode.galactica_validity_check()
            if len(pcode.alias) > 0:
                if pcode.alias in code_names:
                    log.warning("{c1!s} and {c2!s} protocols share the same alias. They must be "
                                "unique.".format(c1=code_names[pcode.alias], c2=pcode))
                else:
                    code_names[pcode.alias] = pcode

        # TODO Check target object validity + object name unicity

        # Check project post-processing runs/simulations validity + experiment alias unicity
        experiments = {}
        for srun in self._simulations:
            srun.galactica_validity_check()
            if len(srun.alias) > 0:
                if srun.alias in experiments:
                    log.warning("{r1!s} and {r2!s} experiments share the same alias. They must be "
                                "unique.".format(r1=experiments[srun.alias], r2=srun))
                else:
                    experiments[srun.alias] = srun

            for prun in srun.post_processing_runs:
                prun.galactica_validity_check()
                if len(prun.alias) > 0:
                    if prun.alias in experiments:
                        log.warning("{r1!s} and {r2!s} experiments share the same alias. They must be "
                                    "unique.".format(r1=experiments[prun.alias], r2=prun))
                    else:
                        experiments[prun.alias] = prun

    def __unicode__(self):
        """
        String representation of the instance
        """
        strrep = "[{category:s}]".format(category=self._category.verbose_name)

        # Title and short description
        if len(self._title) > 0:
            strrep += " '{ptitle:s}' project".format(ptitle=self._title)

        return strrep


__all__ = ["Project", "ProjectCategory"]
