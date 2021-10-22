import pytest
from django.conf import settings

from .confest import django_db_setup
from bot.services import (
    get_random_voice_path,
    get_random_sticker_path,
    get_generated_text,
    is_contains_swearing,
    is_admin,
    get_current_weather_data,
    prepare_weather_forecast,
)


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_random_voice() -> None:
    """Тестирует, что путь до голосового сообщения корректный"""
    path = await get_random_voice_path()
    assert '/app/media/voices/' in path


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_random_sticker() -> None:
    """Тестирует, что путь до стикера корректный"""
    path = await get_random_sticker_path()
    assert '/app/media/stickers/' in path


@pytest.mark.asyncio
async def test_generated_text_with_phrase() -> None:
    """Тестирует работу функции с непустой фразой"""
    phrase = 'Тестовая фраза'
    is_empty_phrase, generated_text = await get_generated_text(phrase)
    assert not is_empty_phrase
    assert generated_text


@pytest.mark.asyncio
async def test_generated_text_with_empty_phrase() -> None:
    """Тестирует работу функции с пустой фразой"""
    phrase = ''
    is_empty_phrase, generated_text = await get_generated_text(phrase)
    assert is_empty_phrase
    assert not generated_text


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_contains_swearing() -> None:
    """Тестирует наличие ругательных слов в сообщении"""
    msg = 'Тестовое сообщения с матом, блять'
    assert await is_contains_swearing(msg)


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_not_contains_swearing() -> None:
    """Тестирует отсутствие ругательных слов в сообщении"""
    msg = 'Тестовое сообщения без мата'
    assert not await is_contains_swearing(msg)


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_is_admin() -> None:
    """Тестирует проверку на админа. Кейс с админом"""
    assert await is_admin(336211006)


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_is_not_admin() -> None:
    """Тестирует проверку на админа. Кейс с обычным пользователем"""
    assert not await is_admin(123456789)


@pytest.mark.asyncio
async def test_current_weather() -> None:
    """Тестирует корректное получение прогноза"""
    city_name = 'Москва'
    weather_data = await get_current_weather_data(city_name)
    assert weather_data['cod'] == 200
    assert weather_data['name'] == city_name


@pytest.mark.asyncio
async def test_prepare_weather_forecast() -> None:
    """Тестирует форматирование прогноза перед его отправкой"""
    city_names = ['Москва', 'Якутск', 'Лондон']
    for city_name in city_names:
        weather_data = await get_current_weather_data(city_name)
        forecast = await prepare_weather_forecast(weather_data)
        assert 'Прогноз погоды в городе' in forecast
        assert 'За окном' in forecast
        assert 'Температура' in forecast
        assert 'Ощущается как' in forecast
        assert 'Влажность' in forecast
        assert 'Скорость ветра' in forecast

        if round(weather_data['main']['temp']) < 0:
            assert 'Я бы советовал одеться потеплее' in forecast
        else:
            assert 'Я бы советовал одеться потеплее' not in forecast
        if -10 > round(weather_data['main']['temp']) > -50:
            assert 'Точнее без подштанников я бы не выходил' in forecast
        else:
            assert 'Точнее без подштанников я бы не выходил' not in forecast
        if round(weather_data['main']['temp']) > 30:
            assert 'Лето, плавки, рок-н-ролл' in forecast
        else:
            assert 'Лето, плавки, рок-н-ролл' not in forecast
        for weather in weather_data['weather']:
            if weather['main'] == 'Rain':
                assert 'Не забудь зонт' in forecast
            else:
                assert 'Не забудь зонт' not in forecast
