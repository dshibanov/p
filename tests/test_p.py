# python -m pytest -v --cov
import pytest, os
import docs.docs as p

@pytest.fixture
def stack():
    return 1 #Stack()

# @pytest.mark.skip(reason="not now")
def test_add_notebook():
    name = 'testp'
    assert os.path.exists(p.get_notes_path(name)) == False
    p.add_notebook(name)
    assert os.path.exists(p.get_notes_path(name)) == True

def test_delete_notebook():
    name = 'testp'
    assert os.path.exists(p.get_notes_path(name)) == True
    p.delete_notebook(name)
    assert os.path.exists(p.get_notes_path(name)) == False

# @pytest.mark.skip(reason="not now")
def test_create():
    name='testp'

    print(name, '  ', p.get_project_path(name))
    assert os.path.exists(p.get_project_path(name)) == False
    assert os.path.exists(p.get_notes_path(name)) == False

    r = p.create_project(name)
    assert os.path.exists(p.get_project_path(name)) == True
    assert os.path.exists(p.get_notes_path(name)) == True

# @pytest.mark.skip(reason="not now")
def test_delete():

    name='testp'
    assert os.path.exists(p.get_project_path(name)) == True
    p.delete_project('testp')
    assert os.path.exists(p.get_project_path(name)) == False

@pytest.mark.skip(reason="not now")
def test_do():

    name='testp'
    assert os.path.exists(p.get_project_path(name)) == True
    p.delete_project('testp')
    assert os.path.exists(p.get_project_path(name)) == False

