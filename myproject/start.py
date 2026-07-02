#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

try:
    print("Initializing Django...", flush=True)
    django.setup()
    print("Django initialized", flush=True)
except Exception as e:
    print(f"ERROR initializing Django: {e}", flush=True)
    sys.exit(1)

# Run migrations
try:
    print("Running migrations...", flush=True)
    from django.core.management import call_command
    call_command('migrate', verbosity=2)
    print("Migrations completed", flush=True)
except Exception as e:
    print(f"ERROR running migrations: {e}", flush=True)
    sys.exit(1)

# Run collectstatic
try:
    print("Collecting static files...", flush=True)
    call_command('collectstatic', '--noinput', verbosity=2)
    print("Static files collected", flush=True)
except Exception as e:
    print(f"ERROR collecting static files: {e}", flush=True)
    sys.exit(1)

# Start gunicorn
try:
    print("Starting gunicorn...", flush=True)
    os.execvp('gunicorn', ['gunicorn', 'myproject.wsgi:application'])
except Exception as e:
    print(f"ERROR starting gunicorn: {e}", flush=True)
    sys.exit(1)

