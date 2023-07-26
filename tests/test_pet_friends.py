import pytest

from api import PetFriends
from models.pet import *
from settings import valid_email, valid_password
from pydantic import *

pf = PetFriends()


# Получение api_key
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, api_key = pf.get_api_key(email, password)
    Api(**api_key)
    assert status == 200

# Получение api_key с невалидным email
def test_get_api_key_for_invalid_email(email='not_valid_email', password=valid_password):
    status, api_key = pf.get_api_key(email, password)
    with pytest.raises(TypeError):
        Api(**api_key)
    assert status == 403

# Получение api_key с невалидным password
def test_get_api_key_for_invalid_password(email=valid_email, password='not_valid_password'):
    status, api_key = pf.get_api_key(email, password)
    with pytest.raises(TypeError):
        Api(**api_key)
    assert status == 403

# получение списка питомцев с невалидным api_key
def test_get_all_pets_with_invalid_key(filter=''):
    status, result = pf.get_list_of_pets({'key': 'aaa'}, filter)
    with pytest.raises(TypeError):
        PetsCollection(**result)
    assert status == 403

# Добавление питомца с фото
def test_add_new_pet_with_valid_data(name='Stitch', animal_type='experimen626', age=2, photo='images/pet_photo.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(name, animal_type, age, auth_key, photo)
    Pet(**result)
    assert status == 200

def test_add_new_pet_without_photo_valid_data(name='Ruben', animal_type='experiment 625', age=1):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_pet_without_photo(name, animal_type, age, auth_key)
    Pet(**result)
    assert status == 200


# получение списка питомцев: всех или своих по фильтру my_pets
def test_get_all_pets_with_valid_key(filter='my_pets'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    PetsCollection(**result)
    assert status == 200


# получение списка всех питомцев и проверка полученного ответа на валидность
def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    with pytest.raises(ValidationError):
        PetsCollection(**result)
    assert status == 200


# Добавление фото последнему питомцу
def test_add_photo_valid_data(photo='images/ruben.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(result) > 0:
        pet_id = result['pets'][0]['id']
        pet_photo = result['pets'][0]['pet_photo']
        status, res = pf.add_photo(pet_id, photo, auth_key)
        assert status == 200
        Pet(**res)
    else:
        assert False


# Изменение информации о последнем добавленном питомце
def test_update_pet_with_valid_data(name='Пчелобык', animal_type='Ушастый', age=89):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(result) > 0:
        pet_id = result['pets'][0]['id']
        status, res = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
        assert status == 200
        Pet(**res)
    else:
        assert False
