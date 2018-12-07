# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-11-30 07:56
from __future__ import unicode_literals

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('phone', models.CharField(max_length=11, null=True, unique=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=1)),
                ('content', models.TextField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '文章表',
                'verbose_name_plural': '文章表',
            },
        ),
        migrations.CreateModel(
            name='Blogroll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_name', models.CharField(blank=True, max_length=100, null=True)),
                ('image_url', models.CharField(blank=True, max_length=255, null=True)),
                ('parse_url', models.CharField(blank=True, max_length=255, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('code_img', models.CharField(blank=True, max_length=120, null=True)),
            ],
            options={
                'verbose_name_plural': '友情链接表',
            },
        ),
        migrations.CreateModel(
            name='Conpanys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_name', models.CharField(max_length=64, verbose_name='公司名称')),
                ('c_number', models.CharField(max_length=11, verbose_name='账号')),
                ('c_pwd', models.CharField(max_length=64, verbose_name='密码')),
                ('c_nature', models.CharField(blank=True, max_length=64, null=True, verbose_name='企业性质')),
                ('c_city', models.CharField(blank=True, max_length=36, null=True, verbose_name='所在地区')),
                ('c_industry', models.CharField(blank=True, max_length=64, null=True, verbose_name='所属行业')),
                ('c_scale', models.IntegerField(blank=True, default=0, null=True, verbose_name='企业规模')),
                ('c_phone', models.CharField(blank=True, max_length=11, null=True, verbose_name='电话')),
                ('c_linkman', models.CharField(blank=True, max_length=12, null=True, verbose_name='法人代表')),
                ('c_create_time', models.DateTimeField(blank=True, null=True, verbose_name='创建时间')),
                ('c_type', models.CharField(blank=True, max_length=64, null=True, verbose_name='企业类型')),
                ('c_site', models.CharField(blank=True, max_length=64, null=True, verbose_name='详细地址')),
                ('c_time', models.CharField(blank=True, max_length=64, null=True, verbose_name='注册时间')),
                ('c_capital', models.CharField(blank=True, max_length=64, null=True, verbose_name='注册资本')),
                ('c_manage', models.CharField(blank=True, max_length=255, null=True, verbose_name='经营范围')),
                ('c_business', models.CharField(blank=True, max_length=100, null=True, verbose_name='营业执照')),
                ('c_brief', models.TextField(blank=True, max_length=1000, null=True, verbose_name='企业简介')),
            ],
            options={
                'verbose_name_plural': '企业表',
            },
        ),
        migrations.CreateModel(
            name='Float',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('f_title', models.CharField(max_length=10)),
                ('a_title', models.CharField(max_length=50)),
                ('a_desc', models.CharField(max_length=255)),
                ('f_desc', models.CharField(max_length=30)),
                ('status', models.CharField(max_length=1)),
                ('content', models.TextField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '浮动表',
                'verbose_name_plural': '浮动表',
            },
        ),
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('i_name', models.CharField(blank=True, max_length=32, null=True, verbose_name='标题')),
                ('i_data', models.DateTimeField(blank=True, null=True, verbose_name='招聘时间')),
                ('i_city', models.CharField(blank=True, max_length=36, null=True, verbose_name='招聘城市')),
                ('i_sponsor', models.CharField(blank=True, max_length=36, null=True, verbose_name='招聘主办方')),
                ('i_type', models.CharField(blank=True, max_length=1, null=True, verbose_name='招聘类型')),
                ('i_content', models.TextField(blank=True, max_length=1000, null=True, verbose_name='招聘会内容')),
            ],
            options={
                'verbose_name_plural': '招聘会表',
            },
        ),
        migrations.CreateModel(
            name='NewsArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image_url', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=1)),
                ('content', models.TextField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '新闻文章表',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, unique=True)),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类',
            },
        ),
        migrations.CreateModel(
            name='Teachin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_title', models.CharField(blank=True, max_length=36, null=True, verbose_name='宣讲标题')),
                ('x_time', models.DateTimeField(blank=True, null=True, verbose_name='宣讲时间')),
                ('x_city', models.CharField(blank=True, max_length=36, null=True, verbose_name='宣讲城市')),
                ('x_school', models.CharField(blank=True, max_length=36, null=True, verbose_name='宣讲学校')),
                ('x_detail', models.TextField(blank=True, null=True, verbose_name='宣讲会详情')),
                ('x_status', models.CharField(default='0', max_length=1, verbose_name='宣讲会状态')),
                ('x_company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='info.Conpanys')),
            ],
            options={
                'verbose_name_plural': '宣讲会表',
            },
        ),
        migrations.CreateModel(
            name='Zhaopin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('z_position', models.CharField(blank=True, max_length=64, null=True, verbose_name='招聘职位名称')),
                ('z_number', models.IntegerField(blank=True, null=True, verbose_name='招聘人数')),
                ('z_salary', models.CharField(blank=True, max_length=64, null=True, verbose_name='月薪')),
                ('z_education', models.CharField(blank=True, max_length=64, null=True, verbose_name='学历要求')),
                ('z_experience', models.CharField(blank=True, max_length=500, null=True, verbose_name='岗位要求')),
                ('z_nature', models.CharField(blank=True, max_length=1, null=True, verbose_name='招聘类型')),
                ('z_data', models.DateTimeField(blank=True, null=True, verbose_name='面试时间')),
                ('z_city', models.CharField(blank=True, max_length=36, null=True, verbose_name='面试地点')),
                ('z_email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='投递邮箱')),
                ('z_detail', models.TextField(blank=True, null=True, verbose_name='招聘会详情')),
                ('z_company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='info.Conpanys')),
            ],
            options={
                'verbose_name_plural': '招聘信息表',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='info.Tag'),
        ),
    ]
