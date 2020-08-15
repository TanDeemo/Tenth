from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_redis import get_redis_connection

from question.models import Label, Question, Reply
from question.serializers import LabelSerializer, GETQuestionByLabelsSerializer, CreateQuestionsSerializer, \
    QuestionDetailSerializer, ReplySerializerForCreate, LabelDetailSerializer, LabelsAllSerializer


# Create your views here.
class LabelViewSet(ModelViewSet):
    queryset = Label.objects.all().order_by('pk')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = LabelSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def users(self, request):
        if self.request.user.is_authenticated:
            labels = request.user.labels.all()
            serializer = LabelSerializer(labels, many=True)
            return Response(serializer.data)
        else:
            return Response({})

    @action(methods=['put'], detail=True, url_path='focusin')
    def focusin_label(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            label = self.get_object()
            if label in user.labels.all():
                return Response({'message': '已关注, 请勿重复点击', 'success': False})
            else:
                user.labels.add(label)
                user.save()
                return Response({'message': '关注成功', 'success': True})
        else:
            return Response({'message': '请先登录', 'success': False}, status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['put'], detail=True, url_path='focusout')
    def focusout_label(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            label = self.get_object()
            if label not in user.labels.all():
                return Response({'message': '未关注, 请勿重复点击', 'success': False})
            else:
                user.labels.remove(label)
                user.save()
                return Response({'message': '取消关注成功', 'success': True})
        else:
            return Response({'message': '请先登录', 'success': False}, status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['get'], detail=False, url_path='full')
    def label_all(self, request, *args, **kwargs):
        labels = self.get_queryset()
        serializer = LabelsAllSerializer(labels, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = LabelDetailSerializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_404_NOT_FOUND)


class QuestionViewSet(ModelViewSet):
    """问题视图集"""
    queryset = Question.objects.all()

    @action(methods=['get'], detail=True, url_path='label/new')
    def get_new_questions_by_label(self, request, pk):
        """获取最新问题"""
        if pk == '-1':
            queryset = self.get_queryset().exclude(reply=0)
        else:
            label = Label.objects.get(pk=pk)
            queryset = Question.objects.exclude(reply=0).filter(labels=label)
        serializer = GETQuestionByLabelsSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, url_path='label/hot')
    def get_hot_questions_by_label(self, request, pk):
        """获取热门问题"""
        if pk == '-1':
            queryset = self.get_queryset().exclude(reply=0).order_by('-reply')
        else:
            label = Label.objects.get(pk=pk)
            queryset = Question.objects.filter(labels=label).exclude(reply=0).order_by('-reply')
        serializer = GETQuestionByLabelsSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, url_path='label/wait')
    def get_wait_questions_by_label(self, request, pk):
        """获取等待回答的问题"""
        if pk == '-1':
            queryset = self.get_queryset().exclude(reply__gt=0)
        else:
            label = Label.objects.get(pk=pk)
            queryset = Question.objects.filter(labels=label, reply=0)
        serializer = GETQuestionByLabelsSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """发布问题"""
        user = request.user
        if user.is_authenticated:
            data = request.data
            data['user'] = user.id
            serializer = CreateQuestionsSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': '发布成功', 'success': True})
        else:
            return Response({'message': '发布失败,请先登录', 'success': False}, status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, *args, **kwargs):
        """问题详情"""
        instance = self.get_object()
        instance.visits += 1
        serializer = QuestionDetailSerializer(instance)
        instance.save()
        return Response(serializer.data)

    @action(methods=['put'], detail=True, url_path='useful')
    def question_useful(self, request, pk):
        user = request.user
        if user.is_authenticated:
            user_id = str(user.id).encode()
            redis_conn = get_redis_connection('question_reply')
            question_useful_set = redis_conn.smembers(f'question_useful_{pk}')
            question_unuseful_set = redis_conn.smembers(f'question_unuseful_{pk}')
            if user_id in question_useful_set:
                return Response({'message': '请勿重复点击', 'success': False})
            elif user_id in question_unuseful_set:
                return Response({'message': '请勿重复点击, 人生没有重来', 'success': False})
            else:
                instance = self.get_object()
                instance.useful_count += 1
                redis_conn.sadd(f'question_useful_{pk}', user.id)
                instance.save()
                return Response({'message': '评价成功', 'success': True})
        else:
            return Response({'message': '请先登录', 'success': False}, status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['put'], detail=True, url_path='unuseful')
    def question_unuseful(self, request, pk):
        user = request.user
        if user.is_authenticated:
            user_id = str(user.id).encode()
            redis_conn = get_redis_connection('question_reply')
            question_useful_set = redis_conn.smembers(f'question_useful_{pk}')
            question_unuseful_set = redis_conn.smembers(f'question_unuseful_{pk}')
            if user_id in question_useful_set:
                return Response({'message': '请勿重复点击, 人生没有重来', 'success': False})
            elif user_id in question_unuseful_set:
                return Response({'message': '请勿重复点击', 'success': False})
            else:
                instance = self.get_object()
                instance.unuseful_count += 1
                redis_conn.sadd(f'question_unuseful_{pk}', user.id)
                instance.save()
                return Response({'message': '评价成功', 'success': True})
        else:
            return Response({'message': '请先登录', 'success': False}, status=status.HTTP_401_UNAUTHORIZED)


    def destroy(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_404_NOT_FOUND)


class ReplyViewSet(ModelViewSet):
    """回答识图集"""
    queryset = Reply.objects.all()

    def create(self, request, *args, **kwargs):
        """创建问题回答"""
        user = request.user
        if user.is_authenticated:
            data = request.data
            data['user'] = user.id
            problem_id = data.get('problem')
            question = Question.objects.get(pk=problem_id)
            serializer = ReplySerializerForCreate(data=data)
            serializer.is_valid(raise_exception=True)
            question.reply += 1
            question.replyname = user.username
            question.replytime = timezone.now()
            serializer.save()
            question.save()
            return Response({'message': '发布成功', 'success': True})
        else:
            return Response({'message': '请登录', 'success': False}, status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['put'], detail=True, url_path='useful')
    def reply_useful(self, request, pk):
        """回答有用"""
        user = request.user
        if user.is_authenticated:
            user_id = str(user.id).encode()
            redis_conn = get_redis_connection('question_reply')
            reply_useful_set = redis_conn.smembers(f'reply_useful_{pk}')
            reply_unuseful_set = redis_conn.smembers(f'reply_unuseful_{pk}')
            if user_id in reply_useful_set:
                return Response({'message': '请勿重复点击', 'success': False})
            elif user_id in reply_unuseful_set:
                return Response({'message': '请勿重复点击, 人生不能重来', 'success': False})
            else:
                instance = self.get_object()
                instance.useful_count += 1
                redis_conn.sadd(f'reply_useful_{pk}', user.id)
                instance.save()
                return Response({'message': '评价成功', 'success': True})
        else:
            return Response({'message': '请先登录', 'success': False}, status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['put'], detail=True, url_path='unuseful')
    def reply_unuseful(self, request, pk):
        user = request.user
        if user.is_authenticated:
            user_id = str(user.id).encode()
            redis_conn = get_redis_connection('question_reply')
            reply_useful_set = redis_conn.smembers(f'reply_useful_{pk}')
            reply_unuseful_set = redis_conn.smembers(f'reply_unuseful_{pk}')
            if user_id in reply_useful_set:
                return Response({'message': '请勿重复点击, 人生不能重来', 'success': False})
            elif user_id in reply_unuseful_set:
                return Response({'message': '请勿重复点击', 'success': False})
            else:
                instance = self.get_object()
                instance.unuseful_count += 1
                redis_conn.sadd(f'reply_unuseful_{pk}', user.id)
                instance.save()
                return Response({'message': '评价成功', 'success': True})
        else:
            return Response({'message': '请先登录', 'success': False}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_404_NOT_FOUND)