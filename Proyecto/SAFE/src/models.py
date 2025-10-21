# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AppUser(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    password_hash = models.CharField(max_length=255, blank=True, null=True)
    role = models.TextField(blank=True, null=True)  # This field type is a guess.
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'app_user'


class Assignment(models.Model):
    type = models.TextField(blank=True, null=True)  # This field type is a guess.
    max_score = models.IntegerField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assignment'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Content(models.Model):
    module = models.ForeignKey('Module', models.DO_NOTHING, db_column='module')
    title = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    content_type = models.TextField()  # This field type is a guess.
    exam = models.ForeignKey('Exam', models.DO_NOTHING, blank=True, null=True)
    assignment = models.ForeignKey(Assignment, models.DO_NOTHING, blank=True, null=True)
    material = models.ForeignKey('Material', models.DO_NOTHING, blank=True, null=True)
    previous_content = models.ForeignKey('self', models.DO_NOTHING, db_column='previous_content', blank=True, null=True)
    next_content = models.ForeignKey('self', models.DO_NOTHING, db_column='next_content', related_name='content_next_content_set', blank=True, null=True)
    is_mandatory = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content'


class ContentProgress(models.Model):
    content = models.ForeignKey(Content, models.DO_NOTHING, db_column='content')
    course_inscription = models.ForeignKey('CourseInscription', models.DO_NOTHING, db_column='course_inscription')
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    file = models.BinaryField(blank=True, null=True)
    results = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_completed = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_progress'


class Course(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    duration_hours = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(AppUser, models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    header_img = models.BinaryField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'course'


class CourseInPath(models.Model):
    learning_path = models.ForeignKey('LearningPath', models.DO_NOTHING, db_column='learning_path')
    course = models.ForeignKey(Course, models.DO_NOTHING, db_column='course')
    previous_course = models.ForeignKey(Course, models.DO_NOTHING, db_column='previous_course', related_name='courseinpath_previous_course_set', blank=True, null=True)
    next_course = models.ForeignKey(Course, models.DO_NOTHING, db_column='next_course', related_name='courseinpath_next_course_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_in_path'


class CourseInscription(models.Model):
    app_user = models.ForeignKey(AppUser, models.DO_NOTHING, db_column='app_user')
    course = models.ForeignKey(Course, models.DO_NOTHING, db_column='course')
    enrollment_date = models.DateTimeField(blank=True, null=True)
    completion_date = models.DateTimeField(blank=True, null=True)
    progress = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'course_inscription'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Exam(models.Model):
    total_questions = models.IntegerField(blank=True, null=True)
    passing_score = models.IntegerField(blank=True, null=True)
    duration_minutes = models.IntegerField(blank=True, null=True)
    max_tries = models.IntegerField(blank=True, null=True)
    questions = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'exam'


class LearningPath(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    estimated_duration = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(AppUser, models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    header_img = models.BinaryField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'learning_path'


class Material(models.Model):
    type = models.TextField(blank=True, null=True)  # This field type is a guess.
    file = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'material'


class Module(models.Model):
    course = models.ForeignKey(Course, models.DO_NOTHING, db_column='course')
    name = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    previous_module = models.ForeignKey('self', models.DO_NOTHING, db_column='previous_module', blank=True, null=True)
    next_module = models.ForeignKey('self', models.DO_NOTHING, db_column='next_module', related_name='module_next_module_set', blank=True, null=True)
    duration_hours = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'module'


class PathInscription(models.Model):
    app_user = models.ForeignKey(AppUser, models.DO_NOTHING, db_column='app_user')
    learning_path = models.ForeignKey(LearningPath, models.DO_NOTHING, db_column='learning_path')
    enrollment_date = models.DateTimeField(blank=True, null=True)
    completion_date = models.DateTimeField(blank=True, null=True)
    progress = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'path_inscription'


class Team(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    supervisor = models.ForeignKey(AppUser, models.DO_NOTHING, db_column='supervisor', blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'team'


class TeamUser(models.Model):
    app_user = models.ForeignKey(AppUser, models.DO_NOTHING, db_column='app_user')
    team = models.ForeignKey(Team, models.DO_NOTHING, db_column='team')
    assigned_at = models.DateTimeField(blank=True, null=True)
    role_in_team = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'team_user'
