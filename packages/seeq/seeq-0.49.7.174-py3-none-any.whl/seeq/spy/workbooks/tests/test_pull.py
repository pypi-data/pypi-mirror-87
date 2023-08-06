import os
import pytest
import tempfile

from seeq import spy
from seeq.spy.workbooks._content import Content

from . import test_load
from .. import Workbook, Topic
from ... import _common
from ...tests import test_common

example_export_push_df = None


def setup_module():
    test_common.login()
    global example_export_push_df
    example_export_push_df = spy.workbooks.push(
        test_load.load_example_export(), refresh=False, path='test_pull', label='test_pull')
    example_export_push_df.drop(columns=['ID'], inplace=True)
    example_export_push_df.rename(columns={'Pushed Workbook ID': 'ID'}, inplace=True)
    example_export_push_df['Type'] = 'Workbook'


# The tests for pulling workbooks are light because so much of the functionality is tested in the push code. I.e.,
# the push code wouldn't work if the pull code had a problem, since the pull code is what produced the saved workbooks.
# (Same goes for the spy.workbooks.save() functionality.)

@pytest.mark.system
def test_pull():
    # Make sure the "include_references" functionality works properly by just specifying the Topic. It'll pull in
    # the Analyses
    to_pull_df = example_export_push_df[example_export_push_df['Workbook Type'] == 'Topic'].copy()

    pull_workbooks = spy.workbooks.pull(to_pull_df)

    pull_workbooks = sorted(pull_workbooks, key=lambda w: w['Workbook Type'])

    analysis = pull_workbooks[0]  # type: Workbook
    assert analysis.id == (example_export_push_df[
        example_export_push_df['Workbook Type'] == 'Analysis'].iloc[0]['ID'])
    assert analysis.name == (example_export_push_df[
        example_export_push_df['Workbook Type'] == 'Analysis'].iloc[0]['Name'])
    assert len(analysis.datasource_maps) >= 3
    assert len(analysis.item_inventory) >= 25

    assert analysis['URL'] == example_export_push_df[
        example_export_push_df['Workbook Type'] == 'Analysis'].iloc[0]['URL']

    worksheet_names = [w.name for w in analysis.worksheets]
    assert worksheet_names == [
        'Details Pane',
        'Calculated Items',
        'Histogram',
        'Metrics',
        'Journal',
        'Global',
        'Boundaries'
    ]

    topic = pull_workbooks[1]
    worksheet_names = [w.name for w in topic.worksheets]
    assert len(topic.datasource_maps) == 3
    assert worksheet_names == [
        'Static Doc',
        'Live Doc'
    ]

    # Pull specific worksheets
    to_pull_df = example_export_push_df[example_export_push_df['Workbook Type'] == 'Analysis'].copy()
    specific_worksheet_ids = {ws.id for ws in analysis.worksheets if ws.name in ['Metrics', 'Journal']}
    pull_workbooks = spy.workbooks.pull(to_pull_df, specific_worksheet_ids=list(specific_worksheet_ids))

    assert len(pull_workbooks) == 1
    assert len(pull_workbooks[0].worksheets) == 2
    worksheet_ids = {ws.id for ws in pull_workbooks[0].worksheets}
    assert worksheet_ids == specific_worksheet_ids


@pytest.mark.system
def test_render():
    search_df = spy.workbooks.search({
        'Workbook Type': 'Topic',
        'Path': 'test_pull',
        'Name': 'Example Topic'
    }, recursive=True)

    spy.options.clear_content_cache_before_render = True

    workbooks = spy.workbooks.pull(search_df, include_rendered_content=True, include_referenced_workbooks=False,
                                   include_inventory=False)

    with tempfile.TemporaryDirectory() as temp:
        spy.workbooks.save(workbooks, temp, include_rendered_content=True)
        topic = [w for w in workbooks if isinstance(w, Topic)][0]

        topic_folder = os.path.join(temp, f'Example Topic ({topic.id})')
        assert os.path.exists(topic_folder)

        render_folder = os.path.join(topic_folder, 'RenderedTopic')
        assert os.path.exists(os.path.join(render_folder, 'index.html'))
        for worksheet in topic.worksheets:
            assert os.path.exists(os.path.join(render_folder, f'{worksheet.document.id}.html'))
            for content_image in worksheet.document.rendered_content_images.keys():
                assert os.path.exists(_common.get_image_file(render_folder, content_image))

            for static_image in worksheet.document.images.keys():
                assert os.path.exists(_common.get_image_file(render_folder, static_image))
