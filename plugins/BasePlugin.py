class BasePlugin:
    # Override.
    def register(self):
        pass

    # Override
    def run_plugin(self, arguments: dict[str, any]):
        pass
