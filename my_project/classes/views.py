from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import LessonClass, UserClassProgress

@login_required
def class_list(request):
    classes = LessonClass.objects.all().order_by('id')
    user_progress = UserClassProgress.objects.filter(user=request.user)
    completed = [p.lesson_class.id for p in user_progress if p.completed]

    return render(request, 'classes/class_list.html', {
        'classes': classes,
        'completed': completed,
    })


@login_required
def class_detail(request, class_id):
    lesson_class = get_object_or_404(LessonClass, id=class_id)
    progress, _ = UserClassProgress.objects.get_or_create(user=request.user, lesson_class=lesson_class)

    if request.method == 'POST':
        progress.completed = True
        progress.completed_at = timezone.now()
        progress.save()
        return redirect('classes:class_list')

    return render(request, 'classes/class_detail.html', {
        'lesson_class': lesson_class,
        'progress': progress,
    })
