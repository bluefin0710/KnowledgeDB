#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
#import pymysql
#pymysql.install_as_MySQLdb()

#def main():
#    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KnowledgeDB.settings')
#    try:
#        from django.core.management import execute_from_command_line
#    except ImportError as exc:
#        raise ImportError(
#            "Couldn't import Django. Are you sure it's installed and "
#            "available on your PYTHONPATH environment variable? Did you "
#            "forget to activate a virtual environment?"
#        ) from exc
#    execute_from_command_line(sys.argv)
#
#if __name__ == '__main__':
#    main()
#

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KnowledgeDB.settings")
#    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nmcmh01.pythonanywhere.com.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
