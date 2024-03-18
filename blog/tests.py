from django.test import TestCase

posts = [
    {
        'id': 1,
        'title': 'a'
    },
    {
        'id': 2,
        'title': 'b'
    },
    {
        'id': 3,
        'title': 'c'
    }
]

comments = [
    {
        'id': 1,
        'post': 2,
        'message': 'b2'
    },
    {
        'id': 2,
        'post': 3,
        'message': 'c2'
    },
    {
        'id': 3,
        'post': 2,
        'message': 'b2'
    },
    {
        'id': 4,
        'post': 1,
        'message': 'a2'
    },
    {
        'id': 5,
        'post': 1,
        'message': 'a2'
    },
]

result = [
    {
        'id': 1,
        'title': 'a',
        'comments': [
            {
                'id': 4,
                'post': 1,
                'message': 'a2'
            },
            {
                'id': 5,
                'post': 1,
                'message': 'a2'
            }
        ]
    },
    {
        'id': 2,
        'title': 'b',
        'comments': [
            {
                'id': 1,
                'post': 2,
                'message': 'b2'
            },
            {
                'id': 3,
                'post': 2,
                'message': 'b2'
            }
        ]
    },
    {
        'id': 3,
        'title': 'c',
        'comments': [
            {
                'id': 2,
                'post': 3,
                'message': 'c2'
            }
        ]
    },
]

for post in posts:
    a = filter(lambda x: x['post'] == post['id'], comments)
    post['comments'] = list(a)
    # for comment in comments:
    #     if post['id'] == comment['post']:
    #         if post.get('comments'):
    #             post['comments'].append(comment)
    #         else:
    #             post['comments'] = [comment]

print(posts)
