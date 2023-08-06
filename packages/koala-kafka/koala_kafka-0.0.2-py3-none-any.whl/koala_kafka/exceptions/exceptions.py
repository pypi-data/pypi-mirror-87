class SchemaRegistryError(Exception):

    def __init__(self, mesg):
        self._mesg = mesg

    def __str__(self):
        return f"""
                Schema registry error:
                {self._mesg}
                """


class EnvironmentVariableNotSet(Exception):

    def __init__(self, env):
        self._env = env

    def __str__(self):
        return f"""
                Required environment variable {self._env} is not set
                """
