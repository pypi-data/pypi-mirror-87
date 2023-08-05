from cnvrg.modules.base_module import CnvrgBase
import cnvrg.helpers.apis_helper as apis_helper
from cnvrg.modules.errors import CnvrgError
import cnvrg.helpers.export_library_helper as export_library_helper
from cnvrg.modules.project import Project
from cnvrg.helpers.param_build_helper import LIBRARY, PROJECT, parse_params
from cnvrg.helpers.url_builder_helper import url_join
from cnvrg.helpers.args_helper import args_to_string, validate_args
from cnvrg.modules.experiment import Experiment
from cnvrg.helpers.param_helper import wrap_string_to_list
from typing import List
import os
DEFAULT_WORKING_DIR = os.path.expanduser("~/cnvrg_libraries")
import importlib.util

class DataSource(CnvrgBase):
    def __init__(self, module_name, path):
        spec = importlib.util.spec_from_file_location(module_name,
                                                      path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod