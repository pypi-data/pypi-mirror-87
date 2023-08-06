from kustomize.generators import generate, clean_data
from tests.base import assert_yaml_dirs_equal


def test_generates_simple_dict(cd_fixtures, create_build_path):
    fixtures_path = cd_fixtures('simple_dict')
    build_path = create_build_path()
    python_path = fixtures_path / 'python'
    reference_path = fixtures_path / 'reference'

    generate(python_path, build_path, 'my_kustomization')

    assert_yaml_dirs_equal(build_path, reference_path)


def test_generates_simple_dict_defaults(cd_fixtures, create_build_path):
    fixtures_path = cd_fixtures('simple_dict_defaults')
    build_path = create_build_path()
    python_path = fixtures_path / 'python'
    reference_path = fixtures_path / 'reference'

    generate(python_path, build_path)

    assert_yaml_dirs_equal(build_path, reference_path)


def test_generates_dataclasses(cd_fixtures, create_build_path):
    fixtures_path = cd_fixtures('dataclasses_')
    build_path = create_build_path()
    python_path = fixtures_path / 'python'
    reference_path = fixtures_path / 'reference'

    generate(python_path, build_path)

    assert_yaml_dirs_equal(build_path, reference_path)


def test_generates_base_and_overlays(cd_fixtures, create_build_path):
    fixtures_path = cd_fixtures('base_and_overlays')
    build_path = create_build_path()
    python_path = fixtures_path / 'python'
    reference_path = fixtures_path / 'reference'

    generate(python_path, build_path)

    assert_yaml_dirs_equal(build_path, reference_path)


def test_generates_patchesJson6902(cd_fixtures, create_build_path):
    fixtures_path = cd_fixtures('patchesJson6902')
    build_path = create_build_path()
    python_path = fixtures_path / 'python'
    reference_path = fixtures_path / 'reference'

    generate(python_path, build_path)

    assert_yaml_dirs_equal(build_path, reference_path)


def test_generates_to_dict(cd_fixtures, create_build_path):
    fixtures_path = cd_fixtures('to_dict')
    build_path = create_build_path()
    python_path = fixtures_path / 'python'
    reference_path = fixtures_path / 'reference'

    generate(python_path, build_path)

    assert_yaml_dirs_equal(build_path, reference_path)


def test_generates_attributes_as_dict(cd_fixtures, create_build_path):
    fixtures_path = cd_fixtures('attributes_as_dict')
    build_path = create_build_path()
    python_path = fixtures_path / 'python'
    reference_path = fixtures_path / 'reference'

    generate(python_path, build_path)

    assert_yaml_dirs_equal(build_path, reference_path)


def test_generates_attrs(cd_fixtures, create_build_path):
    fixtures_path = cd_fixtures('attrs')
    build_path = create_build_path()
    python_path = fixtures_path / 'python'
    reference_path = fixtures_path / 'reference'

    generate(python_path, build_path)

    assert_yaml_dirs_equal(build_path, reference_path)


def test_generates_tuple_multiple(cd_fixtures, create_build_path):
    fixtures_path = cd_fixtures('tuple_multiple')
    build_path = create_build_path()
    python_path = fixtures_path / 'python'
    reference_path = fixtures_path / 'reference'

    generate(python_path, build_path)

    assert_yaml_dirs_equal(build_path, reference_path)


def test_generates_tuple_multiple_attr(cd_fixtures, create_build_path):
    fixtures_path = cd_fixtures('tuple_multiple_attr')
    build_path = create_build_path()
    python_path = fixtures_path / 'python'
    reference_path = fixtures_path / 'reference'

    generate(python_path, build_path)

    assert_yaml_dirs_equal(build_path, reference_path)


def test_generates_kubernetes(cd_fixtures, create_build_path):
    fixtures_path = cd_fixtures('kubernetes')
    build_path = create_build_path()
    python_path = fixtures_path / 'python'
    reference_path = fixtures_path / 'reference'

    generate(python_path, build_path)

    assert_yaml_dirs_equal(build_path, reference_path)


def test_generates_kubernetes11(cd_fixtures, create_build_path):
    fixtures_path = cd_fixtures('kubernetes11')
    build_path = create_build_path()
    python_path = fixtures_path / 'python'
    reference_path = fixtures_path / 'reference'

    generate(python_path, build_path)

    assert_yaml_dirs_equal(build_path, reference_path)


class TestCleanData:
    def test_cleans_up_inner_list_of_dicts(self):
        data = {
            'foo': {
                'bar': {
                    'baz': [
                        {
                            'FOO': 'foo',
                            'BAR': None,
                        }
                    ]
                }
            }
        }

        assert clean_data(data) == {
            'foo': {
                'bar': {
                    'baz': [
                        {
                            'FOO': 'foo',
                        }
                    ]
                }
            }
        }

    def test_cleans_up_inner_dict(self):
        data = {
            'foo': {
                'bar': {
                    'baz': {
                        'FOO': 'foo',
                        'BAR': None,
                    }
                }
            }
        }

        assert clean_data(data) == {
            'foo': {
                'bar': {
                    'baz': {
                        'FOO': 'foo',
                    }
                }
            }
        }
