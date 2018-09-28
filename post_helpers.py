import time


def fetch_groups_posts(api, group_posts_count, group_ids):
    all_groups_posts = []
    for group_id in group_ids:
        current_group_posts = api.wall.get(
            owner_id="-%s" % group_id,
            filter="owner",
            count=group_posts_count,
        )

        all_groups_posts += [
            post for post in current_group_posts['items']
            if post not in all_groups_posts
        ]
    return all_groups_posts


def get_most_popular_posts(api, all_posts, posts_count):
    sorted_posts = sorted(
        all_posts,
        key=lambda k: (
            k['likes']['count'],
            k['reposts']['count']
        ),
        reverse=True,
    )
    most_liked_posts = []

    while len(sorted_posts) and posts_count != 0:
        current_post = sorted_posts[0]
        if not current_post['marked_as_ads']:
            most_liked_posts.append(current_post)
            posts_count -= 1

        del sorted_posts[0]

    return most_liked_posts


def get_photo_attachment(post):
    photo_info = post['attachments'][0]['photo']
    photo_attachment = 'photo{owner_id}_{photo_id}'.format(
        owner_id=photo_info['owner_id'],
        photo_id=photo_info['id'],
    )
    return photo_attachment


def create_scheduled_posts(api, posts, group_id):
    current_time = int(time.time())
    two_hours_in_seconds = 7200

    for post in posts:
        message = post['text']
        photo_attachment = get_photo_attachment(post)
        api.wall.post(
            owner_id=group_id,
            from_group=1,
            message=message,
            attachments=photo_attachment,
            publish_date=current_time+two_hours_in_seconds,
        )
        current_time += two_hours_in_seconds
        time.sleep(0.1)
