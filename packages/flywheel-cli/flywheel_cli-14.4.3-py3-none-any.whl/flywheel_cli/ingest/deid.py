"""Provides load_deid_profile function"""

import itertools
import typing

from flywheel_migration import deidentify

from . import errors, schemas


def load_deid_profile(profile_name, profiles):
    """Get deid profile"""
    profile_name = profile_name or "minimal"

    if profiles:
        loaded_profiles = []
        for config in profiles:
            profile = deidentify.DeIdProfile()
            profile.load_config(config)
            loaded_profiles.append(profile)
        profiles = loaded_profiles

    default_profiles = deidentify.load_default_profiles()
    for profile in itertools.chain(profiles, default_profiles):
        if profile.name == profile_name:
            profile_errors = profile.validate()
            if profile_errors:
                raise errors.InvalidDeidProfile("Invalid deid profile", profile_errors)
            return profile
    raise errors.InvalidDeidProfile("Unknown deid profile")


class DeidLogger:  # pylint: disable=too-few-public-methods
    """Replecment of migrations-toolkit default csv logger that can write
    logs into the database.

    See:
    https://gitlab.com/flywheel-io/public/migration-toolkit/-/blob/master/flywheel_migration/deidentify/deid_log.py#L35
    """

    def __init__(self, write_func: typing.Callable):
        self.write_func = write_func
        self.temp_logs = {}

    def write_entry(self, log_entry):
        """Write log entry.

        Args:
            log_entry (dict): Log entry

        """
        path = log_entry.pop("path")
        log_type = log_entry.pop("type")

        if log_type == "before":
            self.temp_logs[path] = log_entry
        elif log_type == "after":
            before = self.temp_logs.pop(path)
            after = log_entry
            deid_log = schemas.DeidLogIn(
                src_path=path,
                tags_before=before,
                tags_after=after,
            )
            self.write_func(deid_log)
