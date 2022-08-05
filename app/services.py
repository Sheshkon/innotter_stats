from app.aws.dynamodb import add_stats_to_db


def calculate_stats(id: int, data: dict, start_date: str, end_date: str) -> dict:
    real_start_date = data['Items'][0]['date']
    real_end_date = data['Items'][-1]['date']
    freshest_data = data['Items'][-1]['data']
    oldest_data = data['Items'][0]['data']

    username = freshest_data['username']
    likes_amount = int(freshest_data['likes_amount'])
    likes_growth = likes_amount - int(oldest_data['likes_amount'])
    page_amount = int(freshest_data['page_amount'])

    freshest_post_amount, freshest_likes_amount, freshest_followers_amount = \
        _get_posts_likes_followers_amount(freshest_data)
    oldest_posts_amount, oldest_likes_amount, oldest_followers_amount = \
        _get_posts_likes_followers_amount(oldest_data)

    stats = dict(
        id=id,
        username=username,
        likes_amount=likes_amount,
        likes_growth=likes_growth,
        pages_amount=page_amount,
        posts_amount=freshest_post_amount,
        posts_growth=oldest_posts_amount-freshest_post_amount,
        pages_likes_amount=freshest_likes_amount,
        pages_likes_growth=oldest_likes_amount-freshest_likes_amount,
        followers_amount=freshest_followers_amount,
        followers_growth=oldest_followers_amount-freshest_followers_amount,
        start_date=real_start_date,
        end_date=real_end_date
    )
    add_stats_to_db(id, stats, start_date, end_date)
    return stats


def _get_posts_likes_followers_amount(data) -> tuple[int, int, int]:
    total_posts = 0
    total_followers = 0
    total_likes = 0

    for page in data['pages']:
        total_posts += int(page['posts_amount'])
        total_followers += int(page['followers'])
        for post in page['posts']:
            total_likes += int(post['likes'])

    return total_posts, total_likes, total_followers
