from rest_framework import serializers

from .models import Pool
from .models import Question
from .models import SuggestedAnswer
from .models import Answer

class PoolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pool
        fields = ['url', 'id', 'name', 'start_date', 'end_date']


class SuggestedAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestedAnswer
        fields = ['id', 'data']


class QuestionSerializer(serializers.ModelSerializer):
    suggested_answers = SuggestedAnswerSerializer(source='suggestedanswer_set', many=True)
    class Meta:
        model = Question
        fields = ['id', 'question', 'question_type', 'suggested_answers']


class PoolExtendentSerializer(serializers.HyperlinkedModelSerializer):
    questions = QuestionSerializer(source='question_set', many=True)
    class Meta:
        model = Pool
        fields = ['url', 'id', 'name', 'start_date', 'end_date', 'questions']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['question', 'chosen_answers', 'text_answer']


class PoolAnswersSerializer(serializers.Serializer):
    uid = serializers.IntegerField()
    answers = AnswerSerializer(many=True)