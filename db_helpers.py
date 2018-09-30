import json


def is_file_exist(file_name):
    try:
        open(file_name)
    except FileNotFoundError:
        return False
    return True


def get_data_from_json_file(file_name):
    with open(file_name) as f_obj:
        data = json.loads(f_obj.read())
    return data


def dump_data_to_json_file(file_name, data):
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)


def delete_scheduled_posts_from_db(posts, scheduled_posts_count, file_name):
    db_without_scheduled_posts = posts[scheduled_posts_count:]
    dump_data_to_json_file(file_name, db_without_scheduled_posts)
