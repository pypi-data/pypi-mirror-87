class MissingApiKeyError(Exception):
    """Raised when an API key has not been loaded.

    Attributes:
        message -- explanation of why the specific transition is not allowed
        environment_variable -- enviroment variable that should contain the key
    """

    def __init__(self, message, environment_variable, create_at_url):
        print(
            "You are missing an API loaded in the environment variable "
            + environment_variable
            + ".\nIf you do not have one, create one on: "
            + create_at_url
            + "\n\n"
        )
        self.message = message
        self.environment_variable = environment_variable
        self.create_at_url = create_at_url
