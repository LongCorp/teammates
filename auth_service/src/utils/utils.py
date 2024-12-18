
def get_validated_user_dict_from_tuple(data: tuple) -> dict:
    public_id, secret_id, nickname, email, description, image_path = data
    return {
        'public_id': public_id,
        'secret_id': secret_id,
        'nickname': nickname,
        "email": email,
        'description': description,
        'image_path': image_path
    }
