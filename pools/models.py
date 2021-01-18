from django.db import models


QUESTION_TYPE_CHOICES = [
    ('text', 'Text answer'),
    ('radio', 'One answer'),
    ('checkbox', 'Multiple answer'),
]


class Pool(models.Model):
    """
    Base pool class.
    """
    name = models.CharField(max_length=256,
                            help_text="Pool name")
    start_date = models.DateTimeField(editable=False,
                                      help_text="Pool start date")
    end_date = models.DateTimeField(help_text="Pool end date")

    def __str__(self):
        return self.name


class Question(models.Model):
    """
    Pool question.
    """
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE)
    question = models.TextField(help_text="Question text")
    question_type = models.CharField(choices=QUESTION_TYPE_CHOICES,
                                     max_length=8,
                                     help_text="(text, radio, checkbox)")

    def __str__(self):
        return f"{self.pool}: {self.question}"


class SuggestedAnswer(models.Model):
    """
    Suggested answer for question.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    data = models.TextField(help_text="Suggested answer")

    def __str__(self):
        return f"{self.question}: {self.data}"


class Answer(models.Model):
    """
    User`s answer.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_id = models.IntegerField(help_text="User ID")
    chosen_answers = models.ManyToManyField(SuggestedAnswer,
                                            blank=True,
                                            help_text="Set of answers for question with suggested "
                                                      "answers (leave empty if text question)")
    text_answer = models.TextField(help_text="Text answer",
                                   blank=True,
                                   default="(leave empty if radio or checkbox question)")
