import sys
import traceback
import json
from tempfile import NamedTemporaryFile
from datetime import datetime

import requests
import pandas

from uzemszunet.utils import send_email, format_email
from uzemszunet.config import cfg


def lekerdez(email=False):
    try:
        eon_file = dl_eon_file()
        uzemszunetek = {}

        parse_eon_file(eon_file, uzemszunetek)

        if len(uzemszunetek) > 0 and email:
            html = format_email(uzemszunetek)
            send_email(
                html,
                cfg.get('Email', 'smtp_host'),
                cfg.get('Email', 'user'),
                cfg.get('Email', 'password'),
                cfg.get('Email', 'to_mail'),
                'Tervezett üzemszünetek'
            )
        return uzemszunetek
    except Exception as e:
        exc_type, exc_value, exc_tb = sys.exc_info()
        exc_text = traceback.format_exception(exc_type, exc_value, exc_tb)

        if email:
            send_email(
                'Hiba történt:' + str(exc_text),
                cfg.get('Email', 'smtp_host'),
                cfg.get('Email', 'user'),
                cfg.get('Email', 'password'),
                cfg.get('Email', 'to_mail'),
                'Tervezett üzemszünetek HIBA'
            )
        print(exc_text)
