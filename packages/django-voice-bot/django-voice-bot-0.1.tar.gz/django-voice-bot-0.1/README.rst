================
Django-voice-bot
================

Package for django support bot with speech recognition and voice commands.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "voice-bot" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'voice-bot',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('/', include('voice-bot.urls')),

3. Run ``python manage.py migrate`` to create the voice-bot models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a voice-bot (you'll need the Admin app enabled).

5. Setup your bot