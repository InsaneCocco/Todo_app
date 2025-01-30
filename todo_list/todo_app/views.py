from django.views.generic import ListView, CreateView, UpdateView
from .models import ToDoList, ToDoItem
from django.urls import reverse


class ListListView(ListView):
    model = ToDoList
    template_name = 'todo_app/index.html'


class ItemListView(ListView):
    model = ToDoItem
    template_name = 'todo_app/todo_list.html'

    def get_queryset(self):
        ToDoItem.objects.filter(todo_list_id=self.kwargs['list_id'])

    def get_context_data(self):
        context = super().get_context_data()
        context['todo_list'] = ToDoList.objects.get(id=self.kwargs['list_id'])
        return context


class ListCreate(CreateView):
    model = ToDoList
    fields = ['title']

    def get_context_data(self):
        contex = super(ListCreate, self).get_context_data()
        contex['title'] = 'Add a new list'
        return contex


class ItemCreate(CreateView):
    model = ToDoItem
    fields = ['todo_list', 'title', 'description', 'due_date']

    def get_initial(self):
        initial_data = super(ItemCreate, self).get_context_data()
        todo_list = ToDoList.objects.get(id=self.kwargs['list_id'])
        initial_data['todo_list'] = todo_list
        return initial_data

    def get_context_data(self):
        context = super(ItemCreate, self).get_context_data()
        todo_list = ToDoList.objects.get(id=self.kwargs['list_id'])
        context['todo_list'] = todo_list
        context['title'] = 'Create a new item'

    def get_success_url(self):
        return reverse(viewname='list', args=[self.object.todo_list_id])


class ItemUpdate(UpdateView):
    model = ToDoItem
    fields = ['todo_list', 'title', 'description', 'due_date']

    def get_context_data(self, **kwargs):
        context = super(ItemUpdate, self).get_context_data()
        context['todo_list'] = self.object.todo_list
        context['title'] = 'Edit item'
        return context

    def get_success_url(self):
        return reverse(viewname='list', args=[self.object.todo_list_id])

