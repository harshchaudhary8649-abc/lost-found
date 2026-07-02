"""
WSGI config for myproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Run migrations on startup
def run_migrations():
    """Run Django migrations if DATABASE_URL is set (production)."""
    try:
        if os.environ.get('DATABASE_URL'):
            print("Running migrations on WSGI startup...", flush=True)
            from django.core.management import call_command
            call_command('migrate', '--noinput', verbosity=2)
            print("Migrations completed successfully", flush=True)
    except Exception as e:
        print(f"Migration warning (non-fatal): {e}", flush=True)

# Run migrations before creating application
run_migrations()

# Create WSGI application
application = get_wsgi_application()
