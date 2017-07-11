from django.conf import settings

class GlobalRouter(object):
    """
A router to control all database operations on models in the
auth application.
"""

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth.
        """
        app_list = ('Identity',)

        if model._meta.app_label in app_list:
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth.
        """
        app_list = ('Identity',)
        if model._meta.app_label in app_list:
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        app_list = ('Identity',)
        if obj1._meta.app_label in app_list and obj2._meta.app_label in app_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        Make sure the auth app only appears in the 'auth'
        database.
        """
        app_list = ('Identity',)

        if app_label in app_list:
            return db == 'default', 'DS_Douane', 'DS_Impots', 'DS_Finance'
        return None
