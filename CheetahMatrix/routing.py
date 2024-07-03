from django.urls import re_path
from ChatGptHelper.ChatGptHiringAssistant.consumers import InterviewSessionConsumer
from InterrogaBot_V2.consumers import InterviewSessionConsumerV2

websocket_urlpatterns = [
    # re_path(r'ws/interview/(?P<my_interview_id>[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})/?$', InterviewSessionConsumer.as_asgi()),
    # re_path(r'ws/interview/v2/(?P<my_interview_id>[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})/?$', InterviewSessionConsumerV2.as_asgi()),
]
