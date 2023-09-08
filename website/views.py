import telebot
from django.shortcuts import render
from django.views import View

from website.models import Contact
from workbench import settings


class WebSiteView(View):
    template_name = 'website/index.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        message = request.POST.get('message')

        # Сохранение данных в базе данных
        contact = Contact(name=name, phone_number=phone_number, message=message)
        contact.save()

        bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)
        chat_id = settings.TELEGRAM_CHAT_ID
        message_text = f"❕Новая заявка❕\n\n⚜️Имя:{name}.\n\n⚜️Телефон: {phone_number}\n\n⚜️Сообщение: {message}"
        bot.send_message(chat_id, message_text)

        return render(request, self.template_name)


class AboutView(View):
    template_name = 'website/about.html'

    def get(self, request):
        return render(request, self.template_name)


class ContactsView(View):
    template_name = 'website/contacts.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        message = request.POST.get('message')

        # Сохранение данных в базе данных
        contact = Contact(name=name, phone_number=phone_number, message=message)
        contact.save()

        bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)
        chat_id = settings.TELEGRAM_CHAT_ID
        message_text = f"❕Новая заявка❕\n\n⚜️Имя:{name}.\n\n⚜️Телефон: {phone_number}\n\n⚜️Сообщение: {message}"
        bot.send_message(chat_id, message_text)

        return render(request, self.template_name)


class Collaboration(View):
    template_name = 'website/collaboration.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        message = request.POST.get('message')

        # Сохранение данных в базе данных
        contact = Contact(name=name, phone_number=phone_number, message=message)
        contact.save()

        bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)
        chat_id = settings.TELEGRAM_CHAT_ID
        message_text = f"❕Новая заявка❕\n\n⚜️Имя:{name}.\n\n⚜️Телефон: {phone_number}\n\n⚜️Сообщение: {message}"
        bot.send_message(chat_id, message_text)

        return render(request, self.template_name)


class CoursesView(View):
    template_name = 'website/courses.html'

    def get(self, request):
        return render(request, self.template_name)


class FullStackView(View):

    def get(self, request):
        return render(request, 'website/full_stack.html')




class HtmlCssView(View):

    def get(self, request):
        return render(request, 'website/html_css.html')




class PythonView(View):

    def get(self, request):
        return render(request, 'website/python.html')



class PythonDjangoView(View):

    def get(self, request):
        return render(request, 'website/python_django.html')


class ComputerLiteracyView(View):

    def get(self, request):
        return render(request, 'website/computer_literacy.html')



class TermsView(View):

    def get(self, request):
        return render(request, 'website/terms.html')


class PrivacyView(View):

    def get(self,request):
        return render(request, 'website/privacy.html')