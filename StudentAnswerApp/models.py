# coding:utf-8
"""
@author:weiwei
@time:2018.01.23
@version:0.1
"""
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save, m2m_changed
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from notifications.signals import notify
from tagging.fields import TagField


class PersonInformation(models.Model):
    gender_choices = ((None, _('secrecy')),
                      (True, _('male')),
                      (False, _('female')))

    user = models.OneToOneField(User, related_name='person_information', primary_key=True, editable=False)  # 账户
    nickname = models.CharField(max_length=20, verbose_name=_('Nickname'), blank=True)  # 昵称
    gender = models.NullBooleanField(verbose_name=_('Gender'), choices=gender_choices, default=None, )  # 性别
    age = models.PositiveSmallIntegerField(verbose_name=_('Age'), default=20)  # 年龄

    # head_portrait = ProcessedImageField(verbose_name=_('Head Portrait'), processors=[ResizeToFill(85, 85)])  # 头像

    class Meta:
        verbose_name = _('Person Information')

    def __unicode__(self):
        return str(self.user)


class Question(models.Model):
    # content_description = models.TextField(verbose_name=_('Content Description'))  # 内容描述
    content_description = RichTextUploadingField(verbose_name=_('Content Description'))
    creator = models.ForeignKey(User, related_name='created_questions', verbose_name=_('Creator'),
                                editable=False)  # 创建者
    created_date_time = models.DateTimeField(verbose_name=_('Created Date Time'), auto_now_add=True,
                                             editable=False)  # 创建日期
    accessible_groups = models.ManyToManyField(Group, verbose_name=_('Accessible Groups'), null=True)  # 私密性
    share_classes = models.ManyToManyField('Class', verbose_name=_('Share To Classes'), null=True, default='null')
    tags = TagField(verbose_name=_('Tags'))
    favorite_users = models.ManyToManyField(User, related_name='favorite', verbose_name=('Favorite User'))

    class Meta:
        verbose_name = _('Question')
        ordering = ['-created_date_time']

    def __unicode__(self):
        return _('question') + str(self.id)


class SubQuestion(models.Model):
    kind_choices = (('choice', _('choice')),
                    ('gap filling', _('gap filling')),
                    ('short answer', _('short answer')),
                    ('other', _('other')))

    order_number = models.PositiveSmallIntegerField(verbose_name=_('Order Number'))  # 序号
    content = models.TextField(verbose_name=_('Content'))  # 内容
    # kind = models.CharField(max_length=100)  # 类型，主观或者客观
    # label = models.CharField(max_length=100)  # 学科门类
    auto_correction = models.BooleanField(verbose_name=_('Is Auto Correction'), default=False)  # 是否由系统自动批改
    kind = models.CharField(verbose_name=_('Kind'), max_length=20, choices=kind_choices, default='other')  # 问题类型
    # category = models.CharField(max_length=50, verbose_name=_('Category'))  # 学科分类
    # subject = models.CharField(max_length=50, verbose_name=_('Subject'))  # 课程科目
    # related_knowledge_point = models.CharField(max_length=50, verbose_name=_('Related Knowledge Point'))  # 主要涉及的知识点
    standard_answer = models.ForeignKey('SubAnswer', verbose_name=_('Standard Answer'))  # 标准答案
    belong_to_question = models.ForeignKey(Question, related_name='sub_questions',
                                           verbose_name=_('Belong To Queston'))  # 所属于的题目

    class Meta:
        verbose_name = _('Sub Question')

    def __unicode__(self):
        return str(self.order_number) + ' ' + self.content


# class ExaminationPaper(models.Model):
#     name = models.CharField(max_length=100, verbose_name=_('Name'))  # 名称
#     creator = models.ForeignKey(User, editable=False)  # 创建者
#     created_date_time = models.DateTimeField(verbose_name=_('Created Date Time'), auto_now_add=True,
#                                              editable=False)  # 创建日期
#     accessible_groups = models.ManyToManyField(Group, verbose_name=_('Accessible Groups'), null=True)  # 私密性
#     total_score = models.PositiveSmallIntegerField(verbose_name=_('Total Score'))  # 总分
#
#     class Meta:
#         verbose_name = _('Examination Paper')
#
#
# class ExaminationQuestionGroup(models.Model):
#     description = models.TextField(verbose_name=_('Description'))  # 题组相关描述
#     belong_to_examination_paper = models.ForeignKey(ExaminationPaper,
#                                                     verbose_name=_('Belong To Examination Paper'))  # 所属于的试卷
#     group_order_number = models.PositiveSmallIntegerField(verbose_name=_('Group Order Number'))  # 组序号
#     total_score = models.PositiveSmallIntegerField(verbose_name=_('Total Score'))  # 总分
#
#     class Meta:
#         verbose_name = _('Examination Question Group')
#
#
# class ExaminationQuestion(models.Model):
#     question = models.ForeignKey(Question, verbose_name=_('Question'))  # 问题
#     score = models.PositiveSmallIntegerField(verbose_name=_('Score'))  # 分数
#     belong_to_group = models.ForeignKey(ExaminationQuestionGroup, verbose_name=_('Belong To Group'))  # 所属于的试题组
#     order_number = models.PositiveSmallIntegerField(verbose_name=_('Order Number'))  # 序号
#
#     class Meta:
#         verbose_name = _('Examination Question')
#
#
# class SubExaminationQuestion(models.Model):
#     sub_Question = models.ForeignKey(SubQuestion, verbose_name=_('SubQuestion'))  # 子问题
#     score = models.PositiveSmallIntegerField(verbose_name=_('Score'))  # 分数
#     belong_to_examination_question = models.ForeignKey(ExaminationQuestion,
#                                                        verbose_name=_('Belong To Examination Question'))  # 所属于的试题
#     order_number = models.PositiveSmallIntegerField(verbose_name=_('Order Number'))  # 序号
#
#     class Meta:
#         verbose_name = _('Sub Examination Question')
#
#
# class Examination(models.Model):
#     name = models.CharField(max_length=100, verbose_name=_('Examination'))  # 名称
#     kind = models.CharField(max_length=100, verbose_name=_('Kind'))  # 考试类型
#     creator = models.ForeignKey(User, editable=False)  # 创建者
#     created_date_time = models.DateTimeField(verbose_name=_('Created Date Time'), auto_now_add=True,
#                                              editable=False)  # 创建时间
#     begin_date_time = models.DateTimeField(verbose_name=_('Begin Date Time'))  # 开始时间
#     end_date_time = models.DateTimeField(verbose_name=_('End Date Time'))  # 结束时间
#     time_length = models.DurationField(verbose_name=_('Time Length'))  # 时长
#     examination_paper = models.ForeignKey(ExaminationPaper, verbose_name=_('Examinaton Paper'))  # 所用试卷
#     can_submit_num = models.PositiveSmallIntegerField(verbose_name=_('Can Submit Number'))  # 可提交次数
#
#     class Meta:
#         verbose_name = _('Examination')


class Answer(models.Model):
    question = models.ForeignKey(Question, verbose_name=_('Question'))  # 问题
    # content = models.TextField()  # 内容
    creator = models.ForeignKey(User, related_name='created_answers', editable=False)  # 创建者
    created_date_time = models.DateTimeField(verbose_name=_('Created Date Time'), auto_now_add=True,
                                             editable=False)  # 创建时间

    class Meta:
        verbose_name = _('Answer')
        ordering = ['-created_date_time']

    def __unicode__(self):
        return str(self.id) + ' ' + str(self.question.id)


class SubAnswer(models.Model):
    # sub_question = models.ForeignKey(SubQuestion)  # 子问题
    content = models.TextField(verbose_name=_('Content'))  # 内容
    order_number = models.PositiveSmallIntegerField(verbose_name=_('Order Number'))  # 序号
    belong_to_answer = models.ForeignKey(Answer, related_name='sub_answers', verbose_name=_('Belong To Answer'),
                                         null=True)  # 所属于的答案
    correction_rate = models.PositiveSmallIntegerField(verbose_name=_('Correction Rate'), default=0)  # 正确率

    class Meta:
        verbose_name = _('Sub Answer')

    def __unicode__(self):
        return str(self.order_number) + ' ' + self.content


# class ExaminationAnswerPaper(models.Model):
#     creator = models.ForeignKey(User, editable=False)  # 创建者
#     created_date_time = models.DateTimeField(verbose_name=_('Created Date Time'), auto_now_add=True,
#                                              editable=False)  # 创建时间
#     examination_paper = models.ForeignKey(ExaminationPaper, verbose_name=_('Examination Paper'))  # 对应的试卷
#     gaven_total_score = models.PositiveSmallIntegerField(verbose_name=_('Gaven Total Score'))  # 总得分
#
#     class Meta:
#         verbose_name = _('Examination Answer Paper')
#
#
# class ExaminationAnswerGroup(models.Model):
#     belong_to_answer_paper = models.ForeignKey(ExaminationAnswerPaper,
#                                                verbose_name=_('Examintion Answer Group'))  # 所属于的试题答卷
#     group_order_number = models.PositiveSmallIntegerField(verbose_name=_('Group Order Number'))  # 组序号
#     gaven_total_score = models.PositiveSmallIntegerField(verbose_name=_('Gaven Total Score'))  # 总得分
#
#     class Meta:
#         verbose_name = _('Examination Answer Group')
#
#
# class ExaminationAnswer(models.Model):
#     belong_to_group = models.ForeignKey(ExaminationAnswerGroup, verbose_name=_('Belong To Group'))  # 所属于的组
#     group_order_number = models.PositiveSmallIntegerField(verbose_name=_('Group Order Number'))  # 试题答案序号
#     answer = models.ForeignKey(Answer, verbose_name=_('Answer'))  # 试题答案
#     gaven_score = models.PositiveSmallIntegerField(verbose_name=_('Gaven Score'))  # 得分
#
#     class Meta:
#         verbose_name = _('Examination Answer')
#
#
# class SubExaminationAnswer(models.Model):
#     sub_answer = models.ForeignKey(SubAnswer, verbose_name=_('Sub Answer'))  # 子回答
#     score = models.PositiveSmallIntegerField(verbose_name=_('Score'))  # 分数
#     belong_to_examination_answer = models.ForeignKey(ExaminationAnswer,
#                                                      verbose_name=_('Belong To Examintion Answer'))  # 所属于的试题答案
#     order_number = models.PositiveSmallIntegerField(verbose_name=_('Order Number'))  # 序号
#
#
# class UserExaminationRecord(models.Model):
#     examination = models.ForeignKey(Examination, verbose_name=_('Examination'))  # 参加的测试
#     participator = models.ForeignKey(User)  # 参加者
#     begin_date_time = models.DateTimeField(verbose_name=_('Begin Date Time'))  # 开始时间
#     end_date_time = models.DateTimeField(verbose_name=_('End Date Time'))  # 结束时间
#     submit_num = models.PositiveSmallIntegerField(verbose_name=_('Submit Number'))  # 提交次数
#     examination_answer_paper = models.ForeignKey(ExaminationAnswerPaper,
#                                                  verbose_name=_('Examination Answer Paper'))  # 答卷
#
#     class Meta:
#         verbose_name = _('User Examination Record')


class Class(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'), default='class')
    creator = models.ForeignKey(User, related_name='created_classes', null=True, editable=False)  # 创建者
    created_date_time = models.DateTimeField(verbose_name=_('Created Date Time'), auto_now_add=True,
                                             editable=True)  # 创建时间
    description = models.TextField(verbose_name=_('Description'), blank=True, default='')
    # class_questions = models.ManyToManyField(Question, verbose_name=_('Class Questions'), null=True)  # 班级题目
    # class_examination_papers = models.ManyToManyField(ExaminationPaper, verbose_name=_('Class Examination Papers'),
    #                                                   null=True)  # 班级试卷
    # class_examinations = models.ManyToManyField(Examination, verbose_name=_('Class Examintions'), null=True)  # 班级测试
    class_members = models.ManyToManyField(User, related_name='joined_classes', verbose_name=_('Class Member'),
                                           null=True)  # 班级成员
    tags = TagField()

    class Meta:
        verbose_name = _('Class')
        ordering = ['-created_date_time']

    def __unicode__(self):
        return str(self.id) + ' ' + self.name


# class Statistics(models.Model):
#     content_type = models.ForeignKey(ContentType)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')
#
#     # name = models.CharField(max_length=50)
#     sum = models.PositiveIntegerField(default=0)
#     tag = models.CharField(max_length=100, primary_key=True)
#
#
# class Discussion(models.Model):
#     creator = models.ForeignKey(User)  # 创建者
#     created_date_time = models.DateTimeField(verbose_name=_('Created Date Time'))  # 创建时间
#     related_question = models.ForeignKey(Question, verbose_name=_('Related Question'))  # 讨论的问题
#     content = models.TextField(verbose_name=_('Content'))  # 讨论的内容
#
#
# class Message(models.Model):
#     content = models.TextField()


@receiver(post_save, sender=Class)
def join_class_for_creator(sender, instance, created, **kwargs):
    if created and isinstance(instance, Class):
        creator = instance.creator
        if creator:
            creator.joined_classes.add(instance)


@receiver(m2m_changed, sender=Question)
def notify_class_sharing(sender, instance, action, reverse, model, pk_set, using, **kwargs):
    if action is 'post_add' and model == Class and pk_set is not None:
        for pk in pk_set:
            sharing_class = Class.objects.get(pk=pk)
            notify.send(sender=sender, actor=instance.creator, recipient=sharing_class.class_members.all(), verb='share',
                        action_object=instance, target=sharing_class)


@receiver(post_save, sender=Question)
def notify_class_sharing_1(sender, instance, created, **kwargs):
    if created:
        for sharing_class in instance.share_classes.all():
            # sharing_class = Class.objects.get(pk=pk)
            notify.send(instance.creator, recipient=sharing_class.class_members.all(), verb='share',
                        action_object=instance, target=sharing_class, description='share question')


@receiver(post_save, sender=User)
def create_user_information(sender, instance, created, **kwargs):
    if created:
        PersonInformation.objects.get_or_create(user=instance)

# @receiver(post_save, sender=SubAnswer)
# def count_error_answer_statistic(sender, instance, created, update_fields, **kwargs):
#     if not created and 'correction_rate' in update_fields:
#         if instance.correction_rate < 90:
#             error_answer = Statistics.objects.get(tag='error answer')
#             error_answer.sum = error_answer + 1
