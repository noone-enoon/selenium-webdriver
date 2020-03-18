import pytest
from page_object.appl.application import Application


@pytest.fixture
def app(request):
    app = Application()
    request.addfinalizer(app.quit)
    return app
