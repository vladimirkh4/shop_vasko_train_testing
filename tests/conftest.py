import pytest


@pytest.fixture()
def start_finish():
    '''Фикстура пишет "тест начат/тест закончен". Применяется для всех тестов проекта'''

    print("\nStart test")
    yield
    print("\nFinish test")