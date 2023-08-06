import datetime
import logging
from calendar import monthrange
from collections import namedtuple

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render
from transcribe.models import Project, Task, TranscribeUser, UserTask

log = logging.getLogger(__name__)

NumberHolder = namedtuple(
    'NumberHolder',
    ['current_count', 'prev_count', 'total', 'required', 'remaining'],
)


class TaskReportHolder:
    def __init__(self):
        self.projects = []
        self.totals = TotalTaskCounter()


class TotalTaskCounter:
    def __init__(
        self,
        total_transcriptions=0,
        total_finished_transcriptions=0,
        total_reviewed=0,
    ):
        self.total_user_transcriptions = total_transcriptions
        self.total_finished_transcriptions = total_finished_transcriptions
        self.total_reviewed = total_reviewed
        self.total_ready_for_review = (
            self.total_finished_transcriptions - self.total_reviewed
        )

    def __iadd__(self, other):
        self.total_user_transcriptions += other.total_user_transcriptions
        self.total_finished_transcriptions += (
            other.total_finished_transcriptions
        )  # noqa
        self.total_reviewed += other.total_reviewed
        self.total_ready_for_review += other.total_ready_for_review
        return self

    @staticmethod
    def _query_count(
        project, start_date, end_date, for_tasks=False, **filters
    ):
        value = 'task__id' if for_tasks else 'id'
        query = (
            UserTask.objects.filter(task__project=project)
            .filter(modified__range=[start_date, end_date])
            .filter(**filters)
            .values(value)
            .annotate(tcount=Count(value))
            .order_by('tcount')
        )

        return query.count()

    @classmethod
    def from_project(cls, project, start_date, end_date):
        end_date = end_date + datetime.timedelta(days=1)
        params = {
            'project': project,
            'start_date': start_date,
            'end_date': end_date,
            'status': 'finished',
            'task_type': 'transcription',
        }

        total_transcriptions = cls._query_count(**params)

        tasks = Task.objects.filter(
            project=project
        ).annotate_num_finished_usertasks()

        tpt = project.transcribers_per_task
        total_finished_transcriptions = (
            tasks.filter(num_finished_transcriptions__gte=tpt)
            .annotate_last_transcribed()
            .filter(last_transcribed__range=[start_date, end_date])
        )
        total_finished_transcriptions = total_finished_transcriptions.count()
        total_reviewed = (
            tasks.filter(num_finished_reviews__gte=1)
            .filter(modified__range=[start_date, end_date])
            .count()
        )

        totals = cls(
            total_transcriptions, total_finished_transcriptions, total_reviewed
        )
        return totals


def _get_week_days(day):
    monday = day - datetime.timedelta(days=day.weekday())
    friday = monday + datetime.timedelta(days=5)
    return (monday, friday)


def _week_label(monday, friday):
    date_fmt = '%Y/%m/%d'
    return '-'.join([monday.strftime(date_fmt), friday.strftime(date_fmt)])


def _populate_project_for_project_report(project, start_date, end_date):
    before_time = datetime.datetime(2000, 1, 1)
    # number of completed tasks required for project to be considered finished
    required = project.num_tasks
    # number of transcription tasks completed during the time period
    current = TotalTaskCounter.from_project(project, start_date, end_date)
    # number of transcription tasks completed before the time period
    prev = TotalTaskCounter.from_project(project, before_time, start_date)
    # total number of completed transcription tasks so far
    total = (
        current.total_finished_transcriptions
        + prev.total_finished_transcriptions
    )
    # number of remaining transcription tasks to be completed
    remaining = required - total
    project.transcribed = NumberHolder(
        required=required,
        total=total,
        current_count=current.total_finished_transcriptions,
        prev_count=prev.total_finished_transcriptions,
        remaining=remaining,
    )
    total = current.total_reviewed + prev.total_reviewed
    # number of remaining review tasks to be completed
    remaining = required - total
    project.reviewed = NumberHolder(
        required=required,
        total=total,
        current_count=current.total_reviewed,
        prev_count=prev.total_reviewed,
        remaining=remaining,
    )
    return project


def _get_week(request):
    week = request.GET.get('week', datetime.date.today())
    if isinstance(week, str):
        try:
            week = datetime.datetime.strptime(week, '%Y-%m-%d').date()
        except ValueError:
            # TODO: add message if this happens
            week = datetime.date.today()

    return _get_week_days(week)


@login_required
def reports_list(request):
    today = datetime.date.today()
    first_of_month = datetime.date(day=1, month=today.month, year=today.year)
    prev_month = first_of_month - datetime.timedelta(days=1)

    current_week = _get_week_days(today)
    previous_week = _get_week_days(today - datetime.timedelta(days=7))
    prev_week = previous_week[0]
    data = {
        'current_month': today.strftime('%B'),
        'previous_month': prev_month.strftime('%B'),
        'prev_year_month': prev_month.strftime('%Y-%m'),
        'current_week': _week_label(*current_week),
        'previous_week': _week_label(*previous_week),
        'prev_week': prev_week.strftime('%Y-%m-%d'),
    }
    return render(request, 'transcribe/reports/list.html', data)


@login_required
def weekly_projects_report(request, project='all'):
    week = _get_week(request)
    monday, friday = week

    if project != 'all':
        projects = Project.objects.filter(pk=int(project))
        project_label = projects[0].title.title()
    else:
        projects = Project.objects.all()
        project_label = 'All Projects'
    data = {
        'projects': [
            _populate_project_for_project_report(p, monday, friday)
            for p in projects
        ]
    }
    data['label'] = _week_label(monday, friday)
    data['project_label'] = project_label
    data['duration'] = 'Weekly'
    return render(request, 'transcribe/reports/projects.html', data)


@login_required
def monthly_projects_report(request, project='all'):
    month = request.GET.get('month', datetime.date.today().strftime('%Y-%m'))
    year, month = month.split('-')
    month = datetime.date(day=1, month=int(month), year=int(year))

    if project != 'all':
        projects = Project.objects.filter(pk=int(project))
        project_label = projects[0].title.title()
    else:
        projects = Project.objects.all()
        project_label = 'All Projects'
    _, last = monthrange(month.year, month.month)
    first = datetime.date(month.year, month.month, 1)
    last = datetime.date(month.year, month.month, last)
    data = {
        'projects': [
            _populate_project_for_project_report(p, first, last)
            for p in projects
        ]
    }
    data['label'] = month.strftime('%B')
    data['project_label'] = project_label
    data['duration'] = 'Monthly'
    return render(request, 'transcribe/reports/projects.html', data)


@login_required
def weekly_task_report(request, project='all'):
    week = _get_week(request)
    monday, friday = week

    if project == 'all':
        projects = Project.objects.all()
    else:
        projects = Project.objects.get(pk=project)

    report = TaskReportHolder()

    for project in projects:
        project.totals = TotalTaskCounter.from_project(project, monday, friday)
        report.projects.append(project)
        report.totals += project.totals

    data = {
        'report': report,
        'label': _week_label(monday, friday),
        'duration': 'Weekly',
    }

    return render(request, 'transcribe/reports/tasks.html', data)


@login_required
def monthly_task_report(request, project='all'):
    month = request.GET.get('month', datetime.date.today().strftime('%Y-%m'))
    year, month = month.split('-')
    _, last = monthrange(int(year), int(month))
    start = datetime.date(day=1, month=int(month), year=int(year))
    end = datetime.date(day=last, month=int(month), year=int(year))

    if project == 'all':
        projects = Project.objects.all()
    else:
        projects = Project.objects.get(pk=project)

    report = TaskReportHolder()

    for project in projects:
        project.totals = TotalTaskCounter.from_project(project, start, end)
        report.projects.append(project)
        report.totals += project.totals

    data = {
        'report': report,
        'label': start.strftime('%B'),
        'duration': 'Monthly',
    }

    return render(request, 'transcribe/reports/tasks.html', data)


def _user_task_reports_data(date_range, sort='username'):
    def task_count(user, status, task_type, start_date, end_date):
        return (
            user.tasks.filter(modified__gte=start_date)
            .filter(modified__lte=end_date)
            .filter(status=status)
            .filter(task_type=task_type)
            .count()
        )

    users = list(
        TranscribeUser.objects.filter(tasks__isnull=False)
        .distinct()
        .order_by('username')
    )
    for user in users:
        user.num_finished_transcriptions = task_count(
            user, 'finished', 'transcription', *date_range
        )
        user.num_finished_reviews = task_count(
            user, 'finished', 'review', *date_range
        )

    if sort == 'transcriptions':
        users = sorted(
            users, key=lambda u: u.num_finished_transcriptions, reverse=True
        )
    elif sort == 'reviews':
        users = sorted(
            users, key=lambda u: u.num_finished_reviews, reverse=True
        )
    return users


@login_required
def weekly_user_task_report(request):
    sort = request.GET.get('sort', 'username')
    week = _get_week(request)

    users = _user_task_reports_data(week, sort)
    data = {
        'users': users,
        'label': _week_label(*week),
        'duration': 'Weekly',
        'sort': sort,
    }
    return render(request, 'transcribe/reports/users.html', data)


@login_required
def monthly_user_task_report(request):
    sort = request.GET.get('sort', 'username')
    month = request.GET.get('month', datetime.date.today().strftime('%Y-%m'))
    year, month = month.split('-')
    _, last = monthrange(int(year), int(month))
    start = datetime.date(day=1, month=int(month), year=int(year))
    end = datetime.date(day=last, month=int(month), year=int(year))
    date_range = (start, end)

    users = _user_task_reports_data(date_range, sort)

    data = {
        'users': users,
        'label': start.strftime('%B'),
        'duration': 'Monthly',
        'sort': sort,
    }

    return render(request, 'transcribe/reports/users.html', data)
