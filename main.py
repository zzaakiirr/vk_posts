import os

from apscheduler.schedulers.blocking import BlockingScheduler

from vk_auth import fetch_vk_api
import db_helpers
import post_helpers


sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=22)
def main():
    api = fetch_vk_api()
    posting_group_id_ = os.environ.get('GROUP_ID')
    group_ids = db_helpers.get_data_from_json_file('group_ids.json')
    scheduled_posts_count = 12

    db_file_name = 'most_popular_posts.json'
    if db_helpers.is_file_exist(db_file_name):
        posts = db_helpers.get_data_from_json_file(db_file_name)
        if not len(posts):
            posts = post_helpers.fetch_groups_posts(api, 100, group_ids)
    else:
        posts = post_helpers.fetch_groups_posts(api, 100, group_ids)

    most_popular_posts = post_helpers.get_most_popular_posts(
        api, posts, scheduled_posts_count
    )
    post_helpers.create_scheduled_posts(
        api, most_popular_posts, posting_group_id
    )
    db_helpers.delete_scheduled_posts_from_db(
        posts, scheduled_posts_count, db_file_name
    )

sched.start()
