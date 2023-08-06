from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseForbidden
from psu_base.classes.Log import Log
from psu_base.services import auth_service, utility_service
from psu_base.decorators import require_authority, require_authentication, require_non_production
from psu_upload.services import upload_service, retrieval_service
from psu_base.classes.Log import Log
from django.core.paginator import Paginator
from psu_base.services import utility_service
from django.conf import settings
from psu_base import _DEFAULTS as base_defaults
log = Log()


def landing_page(request):
    """
    A landing page
    """
    log.trace()

    return render(
        request, 'landing.html', {}
    )


@require_authentication()
def upload_form(request):
    log.trace()

    sort_by, page = utility_service.pagination_sort_info(request, 'date_created', 'desc')
    uploaded_files = retrieval_service.get_all_files().order_by(*sort_by)

    # Paginate the results
    paginator = Paginator(uploaded_files, 10)
    uploaded_files = paginator.get_page(page)

    return render(
        request, 'upload_sample.html',
        {'uploaded_files': uploaded_files}
    )


@require_authentication()
def upload_action(request):
    """
    Upload a file and store it in S3
    """
    log.trace()

    if request.method == 'POST':

        # IF NOT SAVING FILE
        if request.POST.get('display_only'):
            files = upload_service.read_uploaded_files(request, 'sample_file', convert_to_string="base64")
            return render(request, 'unsaved_upload.html', {'files': files})

        # IF SAVING FILE
        else:
            upload_service.upload_files(request, 'sample_file', 'test-', 'Tests')

    return redirect('upload_form')
