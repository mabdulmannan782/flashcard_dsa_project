from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Subject, Question, Chapter, UserQuizAttempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

class QuestionNode:
    def __init__(self, question):
        self.question = question
        self.next = None
        self.prev = None

def build_linked_list(questions):
    """Takes a list of question objects and returns the head node of a doubly linked list."""
    head = None
    prev_node = None
    nodes = []
    for q in questions:
        node = QuestionNode(q)
        nodes.append(node)
        if prev_node:
            prev_node.next = node
            node.prev = prev_node
        else:
            head = node
        prev_node = node
    return head, nodes 

def home(request):
    subjects = Subject.objects.all()
    return render(request, 'home.html', {'subjects': subjects})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_panel')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')
        user = User.objects.create_user(username=username, password=password)
        messages.success(request, 'Registration successful! Please log in.')
        return redirect('login')
    return render(request, 'register.html')

def subject_chapters(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    chapters = subject.chapters.all()
    return render(request, 'subject_chapters.html', {'subject': subject, 'chapters': chapters})

@staff_member_required
def add_chapter(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    if request.method == 'POST':
        name = request.POST['name']
        Chapter.objects.create(subject=subject, name=name)
        messages.success(request, 'Chapter added successfully!')
        return redirect('subject_chapters', subject_id=subject.id)
    return render(request, 'add_chapter.html', {'subject': subject})

@staff_member_required
def edit_chapter(request, chapter_id):
    chapter = Chapter.objects.get(id=chapter_id)
    if request.method == 'POST':
        chapter.name = request.POST['name']
        chapter.save()
        messages.success(request, 'Chapter updated successfully!')
        return redirect('subject_chapters', subject_id=chapter.subject.id)
    return render(request, 'edit_chapter.html', {'chapter': chapter})

@staff_member_required
def delete_chapter(request, chapter_id):
    chapter = Chapter.objects.get(id=chapter_id)
    subject_id = chapter.subject.id
    if request.method == 'POST':
        chapter.delete()
        messages.success(request, 'Chapter deleted successfully!')
        return redirect('subject_chapters', subject_id=subject_id)
    return render(request, 'delete_chapter.html', {'chapter': chapter})


@staff_member_required
def admin_chapters(request):
    chapters = Chapter.objects.select_related('subject').all()
    return render(request, 'admin_chapters.html', {'chapters': chapters})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


@login_required
def profile(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        user = request.user
        user.username = username
        user.email = email
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    return render(request, 'profile.html')


def result(request, subject_id):
    score = request.session.get('score', 0)
    total = request.session.get('total', 0)
    return render(request, 'result.html', {'score': score, 'total': total})

@login_required(login_url='login')
def admin_panel(request):
    if request.user.is_superuser:
        subjects = Subject.objects.all()
        return render(request, 'admin_panel.html', {'subjects': subjects})
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')

def add_subject(request):
    if request.method == 'POST':
        subject_name = request.POST['subject_name']
        Subject.objects.create(name=subject_name)
        messages.success(request, 'Subject added successfully!')
        return redirect('admin_panel')
    return render(request, 'add_subject.html')

@staff_member_required
def admin_subjects(request):
    subjects = Subject.objects.all()
    return render(request, 'admin_subjects.html', {'subjects': subjects})

@staff_member_required
def add_question(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    if request.method == 'POST':
        question_text = request.POST['question_text']
        option1 = request.POST['option1']
        option2 = request.POST['option2']
        option3 = request.POST['option3']
        option4 = request.POST['option4']
        correct_option = int(request.POST['correct_option'])
        Question.objects.create(
            chapter=chapter,
            question_text=question_text,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_option=correct_option
        )
        messages.success(request, 'Question added successfully!')
        return redirect('subject_chapters', subject_id=chapter.subject.id)
    return render(request, 'add_question.html', {'chapter': chapter})

@login_required
def view_questions(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    questions = chapter.questions.all()
    return render(request, 'view_questions.html', {'chapter': chapter, 'questions': questions})

def edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        subject.name = request.POST['subject_name']
        subject.save()
        messages.success(request, 'Subject updated successfully!')
        return redirect('admin_panel')
    return render(request, 'edit_subject.html', {'subject': subject})

from django.shortcuts import redirect, get_object_or_404

def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted successfully!')
    return redirect('admin_panel')


# from .utils import build_linked_list

@login_required
def quiz(request, chapter_id):
    chapter = Chapter.objects.get(id=chapter_id)
    questions = list(chapter.questions.all())
    total_questions = len(questions)

    # Linked list build karo (agar use kar rahe hain)
    head, nodes = build_linked_list(questions)

    # Current question index
    q_index = int(request.GET.get('q', 0))
    if q_index < 0: q_index = 0
    if q_index >= total_questions: q_index = total_questions - 1

    current_node = nodes[q_index]
    current_question = current_node.question

    has_prev = current_node.prev is not None
    has_next = current_node.next is not None

    # Retrieve or create the user's quiz attempt
    attempt, created = UserQuizAttempt.objects.get_or_create(
        user=request.user, chapter=chapter, defaults={'answers': {}, 'submitted': False}
    )

    # Answer save logic
    if request.method == 'POST' and not attempt.submitted:
        selected_option = request.POST.get('selected_option')
        question_id = str(questions[q_index].id)
        answers = attempt.answers or {}
        # ...answer save logic...
        # Save/update answer
        if selected_option:
            answers[question_id] = int(selected_option)
            attempt.answers = answers
            attempt.save()

        # Next/Previous navigation
        if 'next' in request.POST and has_next:
            return redirect(f"{request.path}?q={q_index+1}")
        elif 'prev' in request.POST and has_prev:
            return redirect(f"{request.path}?q={q_index-1}")
        elif 'submit' in request.POST:
            attempt.submitted = True
            attempt.save()
            messages.success(request, "Quiz submitted successfully!")
            return redirect('quiz_result', chapter_id=chapter.id)
        
    selected = None
    if attempt.answers and str(current_question.id) in attempt.answers:
        selected = attempt.answers[str(current_question.id)]
    # ...rest of context...
    return render(request, 'quiz.html', {
        'chapter': chapter,
        'question': current_question,
        'q_index': q_index,
        'total_questions': total_questions,
        'has_prev': has_prev,
        'has_next': has_next,
        'selected': selected,              # <-- ADD THIS
        'submitted': attempt.submitted,    # <-- AND THIS
    })

@login_required
def quiz_result(request, chapter_id):
    user_id = request.GET.get('user_id')
    if user_id and request.user.is_staff:
        user = get_object_or_404(User, id=user_id)
    else:
        user = request.user

    chapter = get_object_or_404(Chapter, id=chapter_id)
    attempt = UserQuizAttempt.objects.filter(user=user, chapter=chapter, submitted=True).first()
    if not attempt:
        messages.error(request, "This user has not submitted this quiz yet.")
        return redirect('admin_subjects' if request.user.is_staff else 'quiz', chapter_id=chapter.id)
    questions = chapter.questions.all()
    user_answers = attempt.answers or {}
    results = []
    for q in questions:
        user_ans = user_answers.get(str(q.id))
        user_ans_text = None
        if user_ans:
            user_ans_text = getattr(q, f'option{user_ans}')
        correct_ans_text = getattr(q, f'option{q.correct_option}')
        results.append({
            'question': q.question_text,
            'user_answer': user_ans,
            'user_answer_text': user_ans_text,
            'correct_option': q.correct_option,
            'correct_answer_text': correct_ans_text,
        })
    return render(request, 'result.html', {
        'chapter': chapter,
        'results': results,
        'viewed_user': user,  # for showing whose result is this
    })

@login_required
def my_quiz_attempts(request):
    attempts = UserQuizAttempt.objects.filter(user=request.user, submitted=True).select_related('chapter__subject')
    return render(request, 'my_quiz_attempts.html', {'attempts': attempts})

def binary_search_subject(subjects, query):
    left, right = 0, len(subjects) - 1
    while left <= right:
        mid = (left + right) // 2
        if subjects[mid].name.lower() == query.lower():
            return [subjects[mid]]
        elif subjects[mid].name.lower() < query.lower():
            left = mid + 1
        else:
            right = mid - 1
    return []

def search_subject(request):
    query = request.GET.get('q', '')
    subjects = Subject.objects.all().order_by('name')
    result = []
    if query:
        subjects_list = list(subjects)
        result = binary_search_subject(subjects_list, query)
    return render(request, 'search_subject.html', {'subjects': result, 'query': query})

def binary_search(items, query, attr):
    left, right = 0, len(items) - 1
    while left <= right:
        mid = (left + right) // 2
        value = getattr(items[mid], attr).lower()
        if value == query.lower():
            return [items[mid]]
        elif value < query.lower():
            left = mid + 1
        else:
            right = mid - 1
    return []

@staff_member_required
def admin_search(request):
    query = request.GET.get('q', '')
    subjects = Subject.objects.all().order_by('name')
    users = User.objects.all().order_by('username')
    subject_result = user_result = []
    if query:
        subject_result = binary_search(list(subjects), query, 'name')
        user_result = binary_search(list(users), query, 'username')
    return render(request, 'admin_search.html', {
        'subjects': subject_result,
        'users': user_result,
        'query': query
    })

@staff_member_required
def all_users(request):
    users = User.objects.all()
    return render(request, 'all_users.html', {'users': users})

@staff_member_required
def all_quiz_results(request):
    users = User.objects.all()
    all_results = []
    for user in users:
        attempts = UserQuizAttempt.objects.filter(user=user, submitted=True).select_related('chapter__subject')
        for attempt in attempts:
            chapter = attempt.chapter
            questions = chapter.questions.all()
            user_answers = attempt.answers or {}
            results = []
            for q in questions:
                user_ans = user_answers.get(str(q.id))
                user_ans_text = getattr(q, f'option{user_ans}') if user_ans else None
                correct_ans_text = getattr(q, f'option{q.correct_option}')
                results.append({
                    'question': q.question_text,
                    'user_answer': user_ans,
                    'user_answer_text': user_ans_text,
                    'correct_option': q.correct_option,
                    'correct_answer_text': correct_ans_text,
                    'is_correct': user_ans == q.correct_option,
                })
            all_results.append({
                'user': user,
                'chapter': chapter,
                'subject': chapter.subject,
                'results': results,
            })
    return render(request, 'all_quiz_results.html', {'all_results': all_results})