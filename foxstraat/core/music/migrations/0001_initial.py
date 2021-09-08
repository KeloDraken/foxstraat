# Generated by Django 3.2.4 on 2021-09-08 09:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.CharField(max_length=11)),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('cover_art', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='bulletin/music/cover_art/')),
                ('artists', models.CharField(blank=True, max_length=1000, null=True)),
                ('genre', models.CharField(choices=[('Rock', 'Rock'), ('Punk rock', 'Punk rock'), ('Indie rock', 'Indie rock'), ('Alternative rock', 'Alternative rock'), ('Pop rock', 'Pop rock'), ('Hard rock', 'Hard rock'), ('Heavy metal', 'Heavy metal'), ('Grunge', 'Grunge'), ('Emo', 'Emo'), ('Pop', 'Pop'), ('Indie', 'Indie'), ('Hip hop', 'Hip hop'), ('Country', 'Country'), ('Afro pop', 'Afro pop'), ('K-pop', 'K-pop'), ('Reggae', 'Reggae'), ('RnB', 'RnB'), ('Ballad', 'Ballad'), ('Gospel', 'Gospel'), ('Dance', 'Dance'), ('House music', 'House music'), ('Deep house', 'Deep house'), ('Opera', 'Opera'), ('Classical', 'Classical'), ('Soundtrack', 'Soundtrack'), ('Trance', 'Trance'), ('Lo-fi', 'Lo-fi'), ('New wave', 'New wave'), ('Ambient music', 'Ambient music'), ('World music', 'World music'), ('Folk', 'Folk'), ('Jazz', 'Jazz')], default='Rock', max_length=100)),
                ('is_explicit', models.BooleanField(default=False, null=True)),
                ('spotify', models.URLField(blank=True, null=True)),
                ('soundcloud', models.URLField(blank=True, null=True)),
                ('youtube', models.URLField(blank=True, null=True)),
                ('score', models.IntegerField(default=0)),
                ('downvotes', models.PositiveIntegerField(default=0)),
                ('upvotes', models.PositiveIntegerField(default=0)),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VoteSong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0)),
                ('has_voted', models.BooleanField(default=False)),
                ('bulletin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.song')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
