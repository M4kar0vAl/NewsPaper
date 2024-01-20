from django.core.management.base import BaseCommand, CommandError
from news.models import Post


class Command(BaseCommand):
    help = 'Delete all posts in categories'

    def add_arguments(self, parser):
        parser.add_argument(
            'categories',
            nargs='+',
            type=str
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING(
                f'Are you sure you want to delete all posts in following categories: {", ".join(options["categories"])}'
            )
        )
        answer = input('y/n: ')
        if answer == 'y':
            posts_to_del = Post.objects.filter(category__name__in=options['categories'])
            if posts_to_del.exists():
                posts_to_del.delete()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully deleted posts in categories: {", ".join(options["categories"])}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        'There are no posts in these categories'
                    )
                )
            return
        self.stdout.write(
            self.style.ERROR(
                'Deletion cancelled'
            )
        )
