from confluence_poster.poster_config import Config, Page
from dataclasses import fields
from utils import mk_tmp_file
import toml
import pytest

pytestmark = pytest.mark.offline


def test_repo_sample_config():
    """General wellness test. The default config from repo should always work."""
    _ = Config("config.toml")
    # Just some random checks
    assert _.pages[0].page_title == "Some page title"
    assert len(_.pages) == 2
    assert _.author == "author_username"


def test_no_auth(tmp_path):
    """Checks for error if there is no auth section at all"""
    config_file = mk_tmp_file(tmp_path=tmp_path, key_to_pop='auth')
    with pytest.raises(KeyError):
        _ = Config(config_file)


def test_bad_auth_mandatory_params(tmp_path):
    """Checks for proper error if one of the mandatory parameters is missing in auth """
    for param in ["confluence_url", "username", "is_cloud"]:
        config_file = mk_tmp_file(tmp_path, filename=param, key_to_pop=f"auth.{param}")
        with pytest.raises(KeyError) as e:
            _ = Config(config_file)
        assert e.value.args[0] == f"{param} not in auth section"


def test_auth_no_password_ok(tmp_path):
    """Passwords may come from environment or option to the main file. This test ensures that there is no exception
    in this case"""
    config_file = mk_tmp_file(tmp_path, key_to_pop=f"auth.password")
    _ = Config(config_file)
    assert _.auth.password is None


def test_no_author_use_from_auth(tmp_path):
    """In case author was not specified at all - use authentication username for checking who last updated pages"""
    config_file = mk_tmp_file(tmp_path, key_to_pop=f"author")

    _ = Config(config_file)
    assert _.author == _.auth.username


@pytest.mark.parametrize("author_name", [1, ""])
def test_author_name_bad_value(tmp_path, author_name):
    """Checks that exception is thrown if author is not a string or is a bad one"""
    config_file = mk_tmp_file(tmp_path, key_to_update="author", value_to_update=author_name)

    with pytest.raises(ValueError):
        _ = Config(config_file)


def test_default_space(tmp_path):
    """Tests that space definition is applied from default section and
     it does not override specific definition from page """
    config_file = mk_tmp_file(tmp_path, key_to_pop="pages.page1.page_space",
                              key_to_update="pages.page2", value_to_update={'page_title': 'Page2',
                                                                            'page_file': '',
                                                                            'page_space': 'some_space_key'})
    _ = Config(config_file)
    # check if the default value was applied for page without full definition
    assert _.pages[0].page_space == "DEFAULT_SPACE_KEY"
    # make sure the fully defined page definition is not overwritten
    assert _.pages[1].page_space == "some_space_key"


def test_default_space_multiple_pages_default(tmp_path):
    """Checks that the default space is applied if there are two pages with no space specified - default is applied"""
    config_file = mk_tmp_file(tmp_path, key_to_pop="pages.page1.page_space",
                              key_to_update="pages.page2", value_to_update={'page_title': 'Page2',
                                                                            'page_file': ''})
    _ = Config(config_file)
    for page in _.pages:
        assert page.page_space == "DEFAULT_SPACE_KEY"


def test_no_default_space(tmp_path):
    """Tests that if there is no space definition in the default node, and there is no space in page definition,
    there will be an exception"""
    clean_config = toml.load("config.toml")
    config_file = tmp_path / str("no_default_space")
    clean_config['pages']['page1'].pop('page_space')
    clean_config['pages'].pop('default')
    config_file.write_text(toml.dumps(clean_config))

    with pytest.raises(ValueError) as e:
        _ = Config(config_file)
    assert "neither is default space" in e.value.args[0]


def test_default_page_space_not_str(tmp_path):
    config_file = mk_tmp_file(tmp_path,
                              key_to_update="pages.default.page_space", value_to_update=1)
    with pytest.raises(ValueError) as e:
        _ = Config(config_file)
    assert "should be a string" in e.value.args[0]


def test_page_section_not_dict(tmp_path):
    config_file = mk_tmp_file(tmp_path, key_to_update='pages.page1', value_to_update=1)
    with pytest.raises(ValueError) as e:
        _ = Config(config_file)
    assert "Pages section is malformed" in e.value.args[0]


def test_page_definition_not_str(tmp_path):
    """Defines each field one by one as a non-str and tests that exception is thrown"""
    for page_def in [_.name for _ in fields(Page)]:
        config_file = mk_tmp_file(tmp_path, key_to_update=f"pages.page1.{page_def}", value_to_update=1)
        with pytest.raises(ValueError) as e:
            _ = Config(config_file)
        assert f"{page_def} property of a page is not a string" in e.value.args[0]


@pytest.mark.parametrize("param_to_pop", ['page_file'])
def test_page_no_name_or_path(tmp_path, param_to_pop):
    """Checks that lack of mandatory Page definition is handled with an exception"""
    config_file = mk_tmp_file(tmp_path, key_to_pop=f"pages.page1.{param_to_pop}")
    with pytest.raises(KeyError):
        _ = Config(config_file)


def test_one_page_no_name(tmp_path):
    """Tests that page's name can be none for one page case"""
    config_file = mk_tmp_file(tmp_path, key_to_pop=f"pages.page1.page_title")
    config_file = mk_tmp_file(tmp_path, config_to_clone=config_file, key_to_pop=f"pages.page2")
    _ = Config(config_file)
    assert _.pages[0].page_title is None


def test_more_pages_no_name(tmp_path):
    config_file = mk_tmp_file(tmp_path, key_to_pop="pages.page1.page_title",
                              key_to_update="pages.page2", value_to_update={'page_title': "Page2", "page_file": ''})
    with pytest.raises(ValueError) as e:
        _ = Config(config_file)
    assert "more than 1 page" in e.value.args[0]


def test_two_pages_same_name_same_space(tmp_path):
    """Tests that the config properly alerts if there are more than 1 page with the same name and space"""
    config_file = mk_tmp_file(tmp_path)
    config = Config(config_file)
    config_file = mk_tmp_file(tmp_path, config_to_clone=config_file,
                              key_to_update="pages.page2", value_to_update={'page_title': config.pages[0].page_title,
                                                                            "page_file": '',
                                                                            'page_space': config.pages[0].page_space})
    with pytest.raises(ValueError) as e:
        _ = Config(config_file)
    assert "more than 1 page called" in e.value.args[0]


def test_two_pages_same_name_different_space(tmp_path):
    """Tests that the config does not alert if there are more than 1 page with the same name and space"""
    config_file = mk_tmp_file(tmp_path)
    config = Config(config_file)
    config_file = mk_tmp_file(tmp_path, config_to_clone=config_file,
                              key_to_update="pages.page2", value_to_update={'page_title': config.pages[0].page_title,
                                                                            "page_file": '',
                                                                            'page_space': ''})
    _ = Config(config_file)
    assert len(_.pages) == 2
    for page in _.pages:
        assert page.page_title == config.pages[0].page_title


def test_page_parent_specified(tmp_path):
    """Tests that the page parent is applied from the config file"""
    parent_title = "Some parent title"
    config_file = mk_tmp_file(tmp_path,
                              key_to_update="pages.page1.page_parent_title", value_to_update=parent_title)
    config = Config(config_file)
    assert config.pages[0].parent_page_title == parent_title


@pytest.mark.parametrize(
    "page_1_title,page_1_space,page_2_title,page_2_space,result",
    [("A", "A", "A", "A", "equal"),
     ("A", "B", "B", "B", "not equal"),
     ("A", "A", "B", "B", "not equal"),
     ("A", "A", "A", "B", "not equal"),
     ]
)
def test_pages_equal(page_1_title, page_1_space, page_2_title, page_2_space, result):
    page_1 = Page(page_title=page_1_title, page_space=page_1_space, page_file="A", parent_page_title=None)
    page_2 = Page(page_title=page_2_title, page_space=page_2_space, page_file="A", parent_page_title=None)
    assert (page_1 == page_2) == (result == "equal")


def test_compare_page_to_not_page():
    with pytest.raises(ValueError):
        assert Page("Title", "File", "Space", None) == 1
