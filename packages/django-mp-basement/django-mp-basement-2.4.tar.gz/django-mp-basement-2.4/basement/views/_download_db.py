
import os
import subprocess

from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.http import FileResponse
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def download_db(request):

    project_name = os.path.basename(settings.BASE_DIR)

    path = os.path.join(
        str(Path.home()),
        'sites-tmp',
        project_name)

    try:
        os.makedirs(path)
    except FileExistsError:
        pass

    filename = '{}-{}.sql'.format(
        project_name,
        datetime.now().strftime('%Y-%m-%d_%H-%M'))

    full_path = os.path.join(path, filename)

    db_name = settings.DATABASES['default']['NAME']

    command = 'pg_dump {} > {}'.format(db_name, full_path)

    subprocess.call(command, shell=True)

    response = FileResponse(open(full_path, 'rb'))

    os.remove(full_path)

    return response
