
def get_validated_user_dict_from_tuple(data: tuple) -> dict:
    public_id, secret_id, nickname, email, description, image_path = data
    return {
        'public_id': public_id,
        'secret_id': secret_id,
        'nickname': nickname,
        'email': email,
        'description': description,
        'image_path': image_path
    }

def get_validated_questionnaire_dict_from_tuple(data: tuple) -> dict:
    author_id, questionnaire_id, header, description, photo_path, game = data
    return {
        'header': header,
        'questionnaire_id': questionnaire_id,
        'photo_path': photo_path,
        'description': description,
        'author_id': author_id,
        'game': game
    }