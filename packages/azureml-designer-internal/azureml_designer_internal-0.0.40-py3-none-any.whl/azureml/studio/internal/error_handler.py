import logging
import os
import json
from functools import wraps

from azureml.studio.core.error import UserError
from azureml.studio.core.logger import TimeProfile
from azureml.studio.internal.io.rwbuffer_manager import AzureMLOutput
from azureml.studio.internal.error import ErrorMapping, CUSTOMER_SUPPORT_GUIDANCE
from azureml.studio.internal.error import ModuleError, ModuleErrorInfo, UserErrorInfo, ModuleOutOfMemoryError
from azureml.studio.internal.error import LibraryExceptionError, LibraryErrorInfo


class ModuleStatistics:
    ERROR_INFO_FILE = 'error_info.json'
    _AZUREML_STATISTICS_FOLDER = 'module_statistics'
    JSON_INDENT = 2

    def __init__(self):
        self._error_info = None

    @property
    def error_info(self):
        return {'Exception': self._error_info}

    @error_info.setter
    def error_info(self, error: BaseException):

        if not isinstance(error, BaseException):
            raise TypeError('Input error must be BaseException Type')

        if isinstance(error, ModuleError):
            self._error_info = ModuleErrorInfo(error).to_dict()

        elif isinstance(error, UserError):
            self._error_info = UserErrorInfo(error).to_dict()

        else:
            self._error_info = LibraryErrorInfo(error).to_dict()

    def save_to_file(self, folder):
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, self.ERROR_INFO_FILE), 'w') as f:
            json.dump(self.error_info, f, indent=self.JSON_INDENT)

    def save_to_azureml(self):
        azureml_file_path = os.path.join(self._AZUREML_STATISTICS_FOLDER, self.ERROR_INFO_FILE)
        with AzureMLOutput.open(azureml_file_path, 'w') as f:
            json.dump(self.error_info, f, indent=self.JSON_INDENT)


class ErrorHandler:

    def __init__(self, folder=None, logger=None, module_statistics=None):
        self.logger = logging.getLogger('studio.error') if logger is None else logger
        self._module_statistics = ModuleStatistics() if module_statistics is None else module_statistics
        self._folder = folder

    @staticmethod
    def find_cause_with_type(err, error_class):
        while isinstance(err, BaseException):
            if isinstance(err, error_class):
                return err
            err = err.__cause__
        return None

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Catch all exception and store them to module_statistics
            try:
                # Converting specific errors to UserError
                try:
                    return func(*args, **kwargs)
                except BaseException as err:
                    if self.find_cause_with_type(err, MemoryError):
                        ErrorMapping.rethrow(
                            e=err,
                            err=ModuleOutOfMemoryError(),
                        )
                    else:
                        raise
            except BaseException as e:
                # If the error is caused by a UserError/ModuleError, the error is recorded.
                user_error = self.find_cause_with_type(e, (ModuleError, UserError))
                if user_error:
                    e = user_error
                self._handle_exception(e, func.__name__)
            finally:
                self._module_statistics.save_to_azureml()
                if self._folder:
                    self._module_statistics.save_to_file(self._folder)
        return wrapper

    def _handle_exception(self, exception, entry):

        self.logger.info(f"Set error info in module statistics")
        self._module_statistics.error_info = exception

        with TimeProfile("Logging exception information of module execution"):
            # Try to print the session id for better debugging Dataset issues.
            try:
                from azureml._base_sdk_common import _ClientSessionId
                self.logger.info('Session_id = ' + _ClientSessionId)
            except Exception:
                self.logger.info('Session_id cannot be imported.')

            if isinstance(exception, ModuleError):
                self.logger.exception(f"Get ModuleError when invoking {entry}")
                raise exception
            elif isinstance(exception, UserError):
                self.logger.exception(f"Get UserError when invoking {entry}")
                raise exception
            else:
                self.logger.exception(f"Get library exception when invoking {entry}")
                ErrorMapping.rethrow(
                    e=exception,
                    err=LibraryExceptionError(exception, CUSTOMER_SUPPORT_GUIDANCE)
                )


error_handler = ErrorHandler()
