import os
import shutil
from busie_flask.loaders import Loader

def test_loader_init(root_dir):
    """
    Should set _SRC_DIR to the absolute path of the root dir provided
    """
    loader = Loader(root_dir=root_dir)
    assert loader._SRC_DIR == os.path.abspath(root_dir)
    assert loader._APP_MODULE == os.path.basename(os.path.abspath(root_dir))

def test_get_modules(root_dir):
    """
    Should yield an array of dot-notated module paths
    """
    loader = Loader(root_dir)
    tmp_dir = os.path.abspath(os.path.join(root_dir, '_tmp'))
    os.mkdir(tmp_dir)
    open(f'{tmp_dir}/__init__.py', 'w')
    open(f'{tmp_dir}/foo.py', 'w')
    open(f'{tmp_dir}/bar.py', 'w')
    modules = []
    for module in loader.get_modules('_tmp'):
        modules.append(module)
    shutil.rmtree(tmp_dir)
    tmp_module = '.'.join(tmp_dir.split('/')[-2:])
    assert f'{tmp_module}.foo' in modules
    assert f'{tmp_module}.bar' in modules

def test_dynamic_loader(mocker, root_dir):
    """
    - should call get_modules with provided module directory
    - should import each module
    - should return a list of modules that have __all__ and pass the compare callback
    """
    get_modules_mock = mocker.patch('busie_flask.loaders.Loader.get_modules')
    import_module_mock = mocker.patch('busie_flask.loaders.import_module')
    get_modules_mock.return_value = ['foo', 'bar']
    module_stub = mocker.stub(name='module')
    module_stub.__all__ = ('FOO', 'BAR')
    module_stub.FOO = {'name': 'foo'}
    module_stub.BAR = {'name': 'bar'}
    import_module_mock.return_value = module_stub
    mock_compare = mocker.stub(name='compare')
    mock_compare.return_value = True

    loader = Loader(root_dir=root_dir)
    
    res = loader.dynamic_loader('desired_module', mock_compare)
    get_modules_mock.assert_called_once_with('desired_module')
    import_module_mock.assert_has_calls([mocker.call('foo'), mocker.call('bar')])
    assert len(mock_compare.mock_calls) == 4
    assert res == [{'name': 'foo'}, {'name': 'bar'}]

def test_get_models(mocker, root_dir):
    """
    - dynamically loads all models from the provided dir that meet the is_model criteria
    """
    mock = mocker.patch('busie_flask.loaders.Loader.dynamic_loader')
    loader = Loader(root_dir=root_dir)
    res = loader.get_models('some/dir')
    mock.assert_called_once_with('some/dir', loader.is_model)
    assert res == mock.return_value

def test_is_model(mocker, root_dir):
    class Base(mocker.MagicMock):
        @classmethod
        def __ignore__(cls):
            return cls.__name__ in ('Base',)
    mocker.patch('busie_flask.loaders.Model', new=Base)
    loader = Loader(root_dir=root_dir)
    class Valid(Base):
        pass
    class Invalid:
        pass

    assert loader.is_model(Valid)
    assert not loader.is_model(Invalid)
    assert not loader.is_model(Base)

def test_get_views(mocker, root_dir):
    """
    - Dynamically load all views from the provided dir which meet is_view
    """
    mock = mocker.patch('busie_flask.loaders.Loader.dynamic_loader')
    loader = Loader(root_dir=root_dir)
    res = loader.get_views('some/dir')
    mock.assert_called_once_with('some/dir', loader.is_view)
    assert res == mock.return_value

def test_is_view(mocker, root_dir):
    class Base(mocker.MagicMock):
        @classmethod
        def __ignore__(cls):
            return cls.__name__ in ('Base',)
    mocker.patch('busie_flask.loaders.MethodView', new=Base)
    loader = Loader(root_dir=root_dir)
    class Valid(Base):
        """Mock Valid Class"""
    class Invalid:
        """Invalid Class"""
    
    assert loader.is_view(Valid)
    assert not loader.is_view(Base)
    assert not loader.is_view(Invalid)

def test_load_models(mocker, root_dir):
    """
    - adds models dynamically loaded from `models_dir` to system modules
    """
    import string
    import random
    from sys import modules
    mock_get_models = mocker.patch('busie_flask.loaders.Loader.get_models')
    mock_models = [mocker.stub(name='Foo'), mocker.stub(name='Bar')]
    for mock in mock_models:
        mock.__name__ = ''.join(random.choice(string.ascii_letters) for i in range(8))
    mock_get_models.return_value = mock_models
    loader = Loader(root_dir=root_dir)
    loader.load_models('some/dir')
    mock_get_models.assert_called_once_with('some/dir')
    assert hasattr(
        modules['busie_flask.loaders'],
        mock_models[0].__name__
    )
    assert hasattr(
        modules['busie_flask.loaders'],
        mock_models[1].__name__,
    )