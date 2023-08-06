class Loggers:
    def __init__(self):
        self._names = set()
        self._names_excluded = set()

    def populate_with(self, name=None, logger=None, settings=None):
        """
        Once populated with name 'foobar', Loggers().foobar and Loggers().foobar_settings will exists
        """
        if name is None:
            return

        if logger is not None:
            self._populate_logger_prop(name, logger)

        if settings is not None:
            key = self._get_setting_property_name(name)
            self._populate_settings_prop(key, settings)

    def _populate_logger_prop(self, name, value):
        self._set_property(name, value)
        self._names_excluded.add(name)

    def _populate_settings_prop(self, name, value):
        self._set_property(name, value)
        self._names.add(name)

    def _get_setting_property_name(self, name):
        return f"{name}_settings"

    def _get_settings(self, name):
        key = self._get_setting_property_name(name)
        return self._get_property(key, None)

    def _get_property(self, key, value):
        return self.__dict__.get(key, value)

    def _set_property(self, key, value):
        self.__dict__[key] = value

    def settings(self):
        loggers = Loggers()
        for name in self._names:
            value = self._get_property(name, None)
            loggers._populate_settings_prop(name, value)
        for name in self._names_excluded:
            loggers._populate_logger_prop(name, None)
        return loggers
