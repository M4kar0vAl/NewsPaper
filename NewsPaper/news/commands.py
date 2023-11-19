from django.contrib.auth.models import User
from news.models import *

user1 = User.objects.create_user(username='John_Doe')
user2 = User.objects.create_user(username='Jane_Doe')

auth1 = Author.objects.create(user=user1)
auth2 = Author.objects.create(user=user2)

cat1 = Category.objects.create(name='Спорт')
cat2 = Category.objects.create(name='Политика')
cat3 = Category.objects.create(name='Образование')
cat4 = Category.objects.create(name='Культура')

article1 = Post.objects.create(author=auth1,
                               type=Post.ARTICLE,
                               heading='Ar_Heading1',
                               text='Some_Ar_Text_1'
                               )
article2 = Post.objects.create(author=auth2,
                               type=Post.ARTICLE,
                               heading='Ar_Heading2',
                               text='Some_Ar_Text_2'
                               )
news1 = Post.objects.create(author=auth1,
                            type=Post.NEWS,
                            heading='News_Heading',
                            text='Some_Nw_Text'
                            )

article1.category.add(cat3)
article1.category.add(cat4)
article2.category.add(cat1)
news1.category.add(cat2)

comm1 = Comment.objects.create(post=article1, user=user1, text='Comment_Text1')
comm2 = Comment.objects.create(post=article1, user=user2, text='Comment_Text2')
comm3 = Comment.objects.create(post=article2, user=auth1.user, text='Comment_Text3')
comm4 = Comment.objects.create(post=news1, user=auth2.user, text='Comment_Text4')

article1.like()
comm1.like()
comm2.like()
article2.dislike()
comm3.like()
news1.like()
comm4.dislike()

auth1.update_rating()
auth2.update_rating()

Author.objects.order_by('-rating').values('user__username', 'rating')[0]

best_article = Post.objects.order_by('-rating')[0]
Post.objects.order_by('-rating').values('created', 'author__user__username', 'rating', 'heading')[0]
best_article.preview()

Comment.objects.filter(post=best_article).values('created', 'user', 'rating', 'text')
