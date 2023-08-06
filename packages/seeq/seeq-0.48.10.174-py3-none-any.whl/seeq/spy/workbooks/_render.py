import datetime
import os
import re
import textwrap
import types


import pandas as pd
from seeq.base import system
from seeq.sdk import *

from .. import _common
from .. import _login
from .. import _config

from .._common import Status


# noinspection PyPep8Naming
def pull(report, *, errors='raise', quiet=False, status: Status = None):
    status = Status.validate(status, quiet)
    _common.validate_errors_arg(errors)
    report.rendered_content_images = None
    images = dict()

    jobs_api = JobsApi(_login.client)

    def _get_screenshot(_embedded_content_id, _kwargs):
        _timer = _common.timer_start()

        # noinspection PyBroadException
        try:
            status.send_update(_embedded_content_id, {
                'Result': 'Rendering',
                'Time': _common.timer_elapsed(_timer)
            })

            _screenshot_output = jobs_api.get_screenshot(
                **_kwargs
            )  # type: ScreenshotOutputV1

            if _screenshot_output.screenshot is None:
                raise RuntimeError(
                    f'Could not render screenshot. Status message: {_screenshot_output.status_message}')

            _seeq_url = _config.get_seeq_url()
            _request_url = _seeq_url + _screenshot_output.screenshot

            status.send_update(_embedded_content_id, {
                'Result': 'Success',
                'Time': _common.timer_elapsed(_timer)
            })

            return _embedded_content_id, _login.pull_image(_request_url)

        except BaseException:
            status.send_update(_embedded_content_id, {
                'Result': _common.format_exception(),
                'Time': _common.timer_elapsed(_timer)
            })

            if errors == 'raise':
                raise

    def _on_success(_row_index, _job_result):
        _embedded_content_id, _image = _job_result
        images[(_embedded_content_id, 'Content.png')] = _image

    img_matches = re.finditer(r'<img[^>]* id="([^"]+)".*?>', report.html, re.IGNORECASE)
    for img_match in img_matches:
        img_html = img_match.group(0)
        embedded_content_id = img_match.group(1)
        workbookId = _common.get_html_attr(img_html, 'data-seeq-workbookid')
        worksheetId = _common.get_html_attr(img_html, 'data-seeq-worksheetid')
        if not worksheetId:
            continue

        workstepId = _common.get_html_attr(img_html, 'data-seeq-workstepid')

        status.df.at[embedded_content_id, 'Workbook ID'] = workbookId
        status.df.at[embedded_content_id, 'Worksheet ID'] = worksheetId
        status.df.at[embedded_content_id, 'Workstep ID'] = workstepId
        status.df.at[embedded_content_id, 'Result'] = 'Queued'

        # Must match webserver/app/scripts/reportEditor/reportContentSize.component.ts
        REPORT_CONTENT = types.SimpleNamespace(
            SIZE={
                'small': types.SimpleNamespace(name='REPORT.SIZE.SMALL', width=350),
                'medium': types.SimpleNamespace(name='REPORT.SIZE.MEDIUM', width=700),
                'large': types.SimpleNamespace(name='REPORT.SIZE.LARGE', width=1050),
                'custom': types.SimpleNamespace(name='REPORT.SIZE.CUSTOM')
            },
            SHAPE={
                'strip': types.SimpleNamespace(name='REPORT.SHAPE.STRIP', width=16, height=4),
                'rectangle': types.SimpleNamespace(name='REPORT.SHAPE.RECTANGLE', width=16, height=9),
                'square': types.SimpleNamespace(name='REPORT.SHAPE.SQUARE', width=15, height=15)
            },
            MIN_NON_CUSTOM_HEIGHT=130
        )

        SCREENSHOT_SIZE_TO_CONTENT = types.SimpleNamespace(
            DEFAULT_WIDTH=100,
            DEFAULT_HEIGHT=100,
            SELECTOR='.screenshotSizeToContent'
        )

        # Must match webserver/app/scripts/reportEditor/reportContent.store.ts
        # noinspection PyPep8Naming
        def computeHeight(sizeKey, shapeKey, customHeight, contentHeight, screenshotSizeToContent):
            if screenshotSizeToContent:
                return contentHeight or SCREENSHOT_SIZE_TO_CONTENT.DEFAULT_HEIGHT
            elif sizeKey == 'custom':
                return customHeight
            else:
                # Fallback to size: MEDIUM and shape: RECTANGLE in case size and shape are undefined CRAB-11278
                size = REPORT_CONTENT.SIZE.get(sizeKey) or REPORT_CONTENT.SIZE['medium']
                shape = REPORT_CONTENT.SHAPE.get(shapeKey) or REPORT_CONTENT.SHAPE['rectangle']
                return max(size.width * (shape.height / shape.width), REPORT_CONTENT.MIN_NON_CUSTOM_HEIGHT)

        # noinspection PyPep8Naming
        def computeWidth(sizeKey, customWidth, contentWidth, screenshotSizeToContent):
            if screenshotSizeToContent:
                return contentWidth or SCREENSHOT_SIZE_TO_CONTENT.DEFAULT_WIDTH
            elif sizeKey == 'custom':
                return customWidth
            else:
                # Fallback to size: MEDIUM in case size is undefined CRAB-11278
                size = REPORT_CONTENT.SIZE.get(sizeKey) or REPORT_CONTENT.SIZE['medium']
                return size.width

        _size = _common.get_html_attr(img_html, 'data-seeq-size')
        _shape = _common.get_html_attr(img_html, 'data-seeq-shape')
        _customWidth = _common.get_html_attr(img_html, 'data-seeq-customwidth')
        _customHeight = _common.get_html_attr(img_html, 'data-seeq-customheight')
        _contentWidth = _common.get_html_attr(img_html, 'data-seeq-contentwidth')
        _contentHeight = _common.get_html_attr(img_html, 'data-seeq-contentheight')
        _dateVariableId = _common.get_html_attr(img_html, 'data-seeq-datevariableid')
        _screenshotSizeToContent = _common.get_html_attr(img_html, 'data-seeq-screenshotsizetocontent')

        width = computeWidth(_size, _customWidth, _contentWidth, _screenshotSizeToContent)
        height = computeHeight(_size, _shape, _customHeight, _contentHeight, _screenshotSizeToContent)

        if _size:
            status.df.at[embedded_content_id, 'Size'] = _size
        if _shape:
            status.df.at[embedded_content_id, 'Shape'] = _shape
        status.df.at[embedded_content_id, 'Width'] = width
        status.df.at[embedded_content_id, 'Height'] = height

        get_screenshot_kwargs = dict(
            document_id=report.worksheet.id,
            worksheet_id=worksheetId,
            workstep_id=workstepId,
            width=int(width),
            height=int(height)
        )

        if _dateVariableId:
            workstep = report.worksheet.current_workstep()
            date_ranges = workstep.date_ranges  # type: pd.DataFrame()
            date_range = date_ranges[date_ranges['ID'] == _dateVariableId]
            if len(date_range) == 0:
                msg = f'DateVariableID {_dateVariableId} not found in Topic Document workstep'
                if errors == 'raise':
                    raise RuntimeError(msg)
                else:
                    status.df.at[embedded_content_id, 'Result'] = f'Error: {msg}'
                    continue

            date_range = date_range.squeeze()
            if _common.get(date_range, 'Auto Enabled'):
                duration = _common.parse_str_time_to_timedelta(_common.get(date_range, 'Auto Duration'))
                capsule_start = datetime.datetime.now(datetime.timezone.utc) - duration
                capsule_end = datetime.datetime.now(datetime.timezone.utc)
                if _common.get(date_range, 'Auto Offset'):
                    offset = _common.parse_str_time_to_timedelta(_common.get(date_range, 'Auto Offset'))
                    if _common.get(date_range, 'Auto Offset Direction') == 'Past':
                        capsule_start -= offset
                        capsule_end -= offset
                    else:
                        capsule_start += offset
                        capsule_end += offset
            else:
                capsule_start = _common.get(date_range, 'Start')
                capsule_end = _common.get(date_range, 'End')

            if _common.present(date_range, 'Condition ID'):
                conditions_api = ConditionsApi(_login.client)
                capsules_output = conditions_api.get_capsules(
                    id=date_range['Condition ID'],
                    start=capsule_start.isoformat(),
                    end=capsule_end.isoformat())  # type: CapsulesOutputV1
                if _common.get(date_range, 'Condition Strategy') == 'Offset By':
                    capsule_index = _common.get(date_range, 'Condition Offset')
                    if date_range['Condition Reference'] == 'End':
                        capsule_index += 1
                        capsule_index *= -1
                else:
                    if date_range['Condition Reference'] == 'End':
                        capsule_index = -1
                    else:
                        capsule_index = 0
                if (0 <= capsule_index < len(capsules_output.capsules)) or \
                        (capsule_index < 0 and abs(capsule_index) - 1 < len(capsules_output.capsules)):
                    capsule = capsules_output.capsules[capsule_index]
                    get_screenshot_kwargs['range_formula'] = f"capsule('{capsule.start.replace('?', '')}', " \
                                                             f"'{capsule.end.replace('?', '')}')"
            else:
                get_screenshot_kwargs['range_formula'] = f"capsule('{capsule_start.isoformat()}', " \
                                                         f"'{capsule_end.isoformat()}')"

        status.add_job(embedded_content_id,
                       (_get_screenshot, embedded_content_id, get_screenshot_kwargs),
                       _on_success)

    job_count = len(status.jobs)
    status.update(f'Pulling {job_count} pieces of embedded content', Status.RUNNING)
    try:
        status.execute_jobs(errors)
        status.update(f'Pulled {job_count} pieces of embedded content', Status.SUCCESS)
        report.rendered_content_images = images
    except BaseException as e:
        status.exception(e)
        if errors == 'raise':
            raise


def get_rendered_topic_folder(workbook_folder: str):
    return os.path.join(workbook_folder, 'RenderedTopic')


def save(report, workbook_folder: str):
    if report.rendered_content_images is None:
        raise ValueError(f'Embedded content for {report.worksheet} has not been pulled. '
                         'Use include_embedded_content=True when calling spy.workbooks.pull()')

    rendered_topic_folder = get_rendered_topic_folder(workbook_folder)
    os.makedirs(rendered_topic_folder, exist_ok=True)
    _common.save_image_files(report.rendered_content_images, rendered_topic_folder)
    _common.save_image_files(report.images, rendered_topic_folder)
    img_matches = re.finditer(r'<img[^>]*>', report.html, re.IGNORECASE)
    new_html = ''
    cursor = 0

    for img_match in img_matches:
        image_file = None
        img_html = img_match.group(0)
        embedded_content_match = re.search(r' id="([^"]*)"', img_html)
        static_image_match = re.search(r' src="/api(/annotations/(.*?)/images/(.*?))"', img_html)
        if embedded_content_match:
            embedded_content_id = embedded_content_match.group(1)
            if (embedded_content_id, 'Content.png') in report.rendered_content_images:
                image_file = _common.get_image_file(rendered_topic_folder, (embedded_content_id, 'Content.png'))
        elif static_image_match:
            image_id_tuple = (static_image_match.group(2), static_image_match.group(3))
            if image_id_tuple in report.images:
                image_file = _common.get_image_file(rendered_topic_folder, image_id_tuple)

        new_html += report.html[cursor:img_match.start()]
        if image_file:
            image_file = os.path.basename(system.cleanse_path(image_file, windows_long_path=False))
            src_match = re.search(r' src="([^"]*)"', img_html)
            img_html = img_html[0:src_match.start(1)] + image_file + img_html[src_match.end(1):]

        new_html += img_html
        cursor = img_match.end()

    new_html += report.html[cursor:]

    new_html = textwrap.dedent(f"""
            <html>
            <head>
              <link rel="stylesheet" href="app.css">
              <title>{report.worksheet.name}</title>
            </head>
            <body style="overflow: auto;">
            <div class="p10">
            {new_html}
            </div>
            </body>
            </html>
        """)

    with open(os.path.join(rendered_topic_folder, f'{report.id}.html'), 'w', encoding='utf-8') as f:
        f.write(new_html)

    system.copyfile(os.path.join(os.path.dirname(__file__), 'app.css'),
                    os.path.join(rendered_topic_folder, 'app.css'))


def toc(workbook, workbook_folder: str):
    rendered_topic_folder = get_rendered_topic_folder(workbook_folder)

    worksheet_html = [textwrap.dedent(f"""
        <li class="list-group-item"><a class="h2" href="{worksheet.document.id}.html">{worksheet.name}</a></li>        
    """) for worksheet in workbook.worksheets]

    worksheets_html = '\n'.join(worksheet_html)

    new_html = textwrap.dedent(f"""
            <html>
            <head>
              <link rel="stylesheet" href="app.css">
              <title>{workbook.name}</title>
            </head>            
            <body style="overflow: auto;">
            <div class="p10">
            <p class="h1">{workbook.name}</p>
            <ul>
            {worksheets_html}
            </ul>
            </div>
            </body>
            </html>
        """)

    index_filename = os.path.join(rendered_topic_folder, 'index.html')
    os.makedirs(os.path.dirname(index_filename), exist_ok=True)
    with open(index_filename, 'w', encoding='utf-8') as f:
        f.write(new_html)
