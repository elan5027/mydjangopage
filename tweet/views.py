
# tweet/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from .models import TweetModel, TweetComment  # 글쓰기 모델 -> 가장 윗부분에 적어주세요!



def home(request):
    user = request.user.is_authenticated  # 사용자가 인증을 받았는지 (로그인이 되어있는지)
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')

def tweet(request):
    if request.method == 'GET':  # 요청하는 방식이 GET 방식인지 확인하기
        user = request.user.is_authenticated  # 사용자가 로그인이 되어 있는지 확인하기
        if user:  # 로그인 한 사용자라면
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html', {'tweet': all_tweet})
        else:  # 로그인이 되어 있지 않다면
            return redirect('/sign-in')
    elif request.method == 'POST':  # 요청 방식이 POST 일때
        user = request.user  # 현재 로그인 한 사용자를 불러오기
        tags = request.POST.get('tag', '').split(',')
        content = request.POST.get('my-content', '')  # 모델에 글 저장

        if content == '':
            all_tweet = TweetModel.objects.all().order_by('-created_at')

            return render(request, 'tweet/home.html', {'error': "게시글에 내용이 없습니다.", 'tweet': all_tweet})
        else:
            my_tweet = TweetModel.objects.create(author=user, content=content)
            for tag in tags:
                tag = tag.strip()
                if tag != '':
                    my_tweet.tags.add(tag)

            my_tweet.save()
            return redirect('/tweet')


@login_required
def delete_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet')

@login_required
def detail_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    tweet_commnet = TweetComment.objects.filter(tweet_id=id).order_by('-created_at')
    return render(request, 'tweet/tweet_detail.html', {'tweet': my_tweet, 'comment':tweet_commnet})

@login_required
def write_comment(request, id):
    if request.method == 'POST':  # 요청 방식이 POST 일때
        my_tweet = TweetComment()  # 글쓰기 모델 가져오기
        my_tweet.comment = request.POST.get('comment', '')
        my_tweet.author = request.user
        my_tweet.tweet = TweetModel.objects.get(id=id)
        my_tweet.save()
        return redirect('/tweet/'+str(id))


@login_required
def delete_comment(request, id):
    my_tweet = TweetComment.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet/'+str(my_tweet.tweet.id))

class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'


class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = TweetModel

    def get_queryset(self):
        return TweetModel.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context