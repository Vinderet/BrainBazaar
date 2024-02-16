from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from .models import Test, Question, Answer, Marks_Of_User
from .forms import RegistrationForm, LoginForm


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tests')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('tests')
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def test(request, test_id):
    test = Test.objects.get(id=test_id)
    questions = test.question_set.all()
    answers = []
    for question in questions:
        answers.append(question.answer_set.all())
    if request.method == 'POST':
        score = 0
        for i, answer in enumerate(request.POST.getlist('answer')):
            if Answer.objects.get(id=answer).correct:
                score += 1
        Marks_Of_User.objects.create(user=request.user, test=test, score=score)
        return redirect('marks')
    return render(request, 'test.html', {'questions': questions, 'answers': answers})


@login_required
def marks(request):
    user_marks = Marks_Of_User.objects.filter(user=request.user)
    return render(request, 'marks.html', {'user_marks': user_marks})


@staff_member_required
def test_management(request):
    tests = Test.objects.all()
    return render(request, 'test_management.html', {'tests': tests})


@staff_member_required
def add_test(request):
    if request.method == 'POST':
        name = request.POST['name']
        desc = request.POST['desc']
        number_of_questions = request.POST['number_of_questions']
        Test.objects.create(name=name, desc=desc, number_of_questions=number_of_questions)
        return redirect('test_management')
    return render(request, 'add_test.html')


@staff_member_required
def edit_test(request, test_id):
    test = Test.objects.get(id=test_id)
    if request.method == 'POST':
        test.name = request.POST['name']
        test.desc = request.POST['desc']
        test.number_of_questions = request.POST['number_of_questions']
        test.save()
        return redirect('test_management')
    return render(request, 'edit_test.html', {'test': test})


@staff_member_required
def delete_test(request, test_id):
    test = Test.objects.get(id=test_id)
    test.delete()
    return redirect('test_management')


@staff_member_required
def add_question(request, test_id):
    test = Test.objects.get(id=test_id)
    if request.method == 'POST':
        content = request.POST['content']
        Question.objects.create(content=content, quiz=test)
        return redirect('edit_test', test_id=test_id)
    return render(request, 'add_question.html', {'test': test})


@staff_member_required
def delete_question(request, question_id):
    question = Question.objects.get(id=question_id)
    test_id = question.quiz.id
    question.delete()
    return redirect('edit_test', test_id=test_id)

@staff_member_required
def edit_question(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.method == 'POST':
        question.content = request.POST['content']
        question.save()
        test_id = question.quiz.id
        return redirect('edit_test', test_id=test_id)
    return render(request, 'edit_question.html', {'question': question})

@staff_member_required
def add_answer(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.method == 'POST':
        content = request.POST['content']
        correct = request.POST.get('correct') == 'on'
        Answer.objects.create(content=content, correct=correct, question=question)
        return redirect('edit_question', question_id=question_id)
    return render(request, 'add_answer.html', {'question': question})

@staff_member_required
def delete_answer(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    question_id = answer.question.id
    answer.delete()
    return redirect('edit_question', question_id=question_id)

@staff_member_required
def edit_answer(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    if request.method == 'POST':
        answer.content = request.POST['content']
        answer.correct = request.POST.get('correct') == 'on'
        answer.save()
        question_id = answer.question.id
        return redirect('edit_question', question_id=question_id)
    return render(request, 'edit_answer.html', {'answer': answer})