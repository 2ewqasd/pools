from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from .models import Pool
from .models import Question
from .models import Answer
from .models import SuggestedAnswer
from .serializers import PoolSerializer
from .serializers import PoolExtendentSerializer
from .serializers import PoolAnswersSerializer
from .serializers import AnsweredPoolSerializer


class PoolViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing pools.
    """
    def get_queryset(self):
        return Pool.objects.filter(start_date__lte=timezone.now()).filter(end_date__gte=timezone.now())

    def get_serializer_class(self):
        if self.action == 'list':
            return PoolSerializer
        if self.action == 'publish_answers':
            return PoolAnswersSerializer
        return PoolExtendentSerializer

    @action(detail=True, methods=['post'])
    def publish_answers(self, request, pk=None):
        serializer = PoolAnswersSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.data['uid']
            if Answer.objects.filter(question__pool=pk, user_id=user_id):
                return Response({'Error': 'Already answered'},
                                status=status.HTTP_400_BAD_REQUEST)
            answers = []
            question_set = []
            for answer in serializer.data['answers']:
                if answer.get('chosen_answers') and answer.get('text_answer'):
                    return self.roll_back('answer contains suggested and text answers simultaneously', answers)
                if not (answer.get('chosen_answers') or answer.get('text_answer')):
                    return self.roll_back('there is no answer', answers)
                if answer['question'] in question_set:
                    return self.roll_back('double answer', answers)
                else:
                    question_set.append(answer['question'])
                question = Question.objects.get(pk=answer['question'])
                if question.pool.pk != int(pk):
                    return self.roll_back('Wrong question ID', answers)
                if question.question_type in ('radio', 'checkbox') and answer.get('text_answer'):
                    return self.roll_back('Wrong answer type', answers)
                if question.question_type == 'text' and answer.get('chosen_answers'):
                    return self.roll_back('Wrong answer type', answers)
                if question.question_type == 'radio' and len(answer['chosen_answers']) > 1:
                    return self.roll_back('Too much answer', answers)
                for i in answer['chosen_answers']:
                    if SuggestedAnswer.objects.get(pk=i).question.pk != answer['question']:
                        return self.roll_back('Wrong answer ID', answers)
                if question.pool.pk != int(pk):
                    return self.roll_back('Wrong question ID', answers)
                obj = Answer.objects.create(user_id=user_id,
                                            question=question,
                                            text_answer=answer['text_answer'])
                for i in answer['chosen_answers']:
                    obj.chosen_answers.add(i)
                answers.append(obj)
            if len(answers) != Pool.objects.get(pk=pk).question_set.count():
                return self.roll_back('Not all answers', answers)
            return Response({'Success': 'answers recorded'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def roll_back(self, message, answers):
        for answer in answers:
            answer.delete()
        return Response({'Error': message},
                        status=status.HTTP_400_BAD_REQUEST)


class AnsweredPoolsViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for viewing answered pools.
    """
    def list(self, request, user_id):
        pools_pk = Answer.objects.filter(user_id=user_id).values_list('question__pool', flat=True).distinct()
        queryset = Pool.objects.filter(pk__in=pools_pk)
        serializer = AnsweredPoolSerializer(queryset, many=True, context={'request': request,
                                                                          'user_id': user_id})
        return Response(serializer.data)
