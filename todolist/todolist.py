import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle

class ToDoApp(App):
    def build(self):
        self.tasks = self.load_tasks()
        self.root = FloatLayout()

        # Set background image
        with self.root.canvas.before:
            self.bg_rect = Rectangle(source='images/background.jpg', pos=self.root.pos, size=Window.size)
            self.root.bind(size=self.update_bg, pos=self.update_bg)

        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(0.8, 0.9), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        self.title_label = Label(text="====== TO DO LIST ======", font_size='24sp')
        self.main_layout.add_widget(self.title_label)

        self.task_input = TextInput(hint_text='Enter your new task', size_hint_y=None, height=40, foreground_color=((1, 0, 0, 1)), hint_text_color=(0, 0, 0, 1))
        self.main_layout.add_widget(self.task_input)

        self.add_task_btn = Button(text='Add Task', size_hint_y=None, height=40, color=(0, 191, 191))
        self.add_task_btn.background_normal = 'images/add_icon.png'
        self.add_task_btn.bind(on_release=self.add_new_task)
        self.main_layout.add_widget(self.add_task_btn)

        self.show_tasks_btn = Button(text='Show Tasks', size_hint_y=None, height=40, color=(0, 191, 191))
        self.show_tasks_btn.background_normal = 'images/show_icon.png'
        self.show_tasks_btn.bind(on_release=self.show_all_tasks)
        self.main_layout.add_widget(self.show_tasks_btn)

        self.search_task_input = TextInput(hint_text='Search task', size_hint_y=None, height=40, foreground_color=(0, 1, 0, 1), hint_text_color=(0, 0, 0, 1))
        self.main_layout.add_widget(self.search_task_input)

        self.search_task_btn = Button(text='Search Task', size_hint_y=None, height=40, color=(0, 1, 0, 1))
        self.search_task_btn.background_normal = 'images/search_icon.png'
        self.search_task_btn.bind(on_release=self.search_for_task)
        self.main_layout.add_widget(self.search_task_btn)

        self.delete_task_input = TextInput(hint_text='Enter task to delete', size_hint_y=None, height=40, foreground_color=(0, 191, 191), hint_text_color=(0, 0, 0, 1))
        self.main_layout.add_widget(self.delete_task_input)

        self.delete_task_btn = Button(text='Delete Task', size_hint_y=None, height=40, color=(0, 191, 191))
        self.delete_task_btn.background_normal = 'images/delete_icon.png'
        self.delete_task_btn.bind(on_release=self.remove_task)
        self.main_layout.add_widget(self.delete_task_btn)

        self.update_task_input = TextInput(hint_text='Enter task to update', size_hint_y=None, height=40, foreground_color=(0, 191, 191), hint_text_color=(0, 0, 0, 1))
        self.main_layout.add_widget(self.update_task_input)

        self.update_task_btn = Button(text='Update Task', size_hint_y=None, height=40, color=(0, 191, 191))
        self.update_task_btn.background_normal = 'images/update_icon.png'
        self.update_task_btn.bind(on_release=self.modify_task)
        self.main_layout.add_widget(self.update_task_btn)

        self.root.add_widget(self.main_layout)
        return self.root

    def update_bg(self, *args):
        self.bg_rect.pos = self.root.pos
        self.bg_rect.size = Window.size

    def add_new_task(self, instance):
        task = self.task_input.text.strip()
        if task:
            self.save_task(task)
            self.task_input.text = ''
            self.show_popup("Success", "Task added successfully.")

    def show_all_tasks(self, instance):
        self.show_tasks_popup()

    def search_for_task(self, instance):
        task = self.search_task_input.text.strip()
        if task:
            tasks = self.load_tasks()
            found_tasks = [t for t in tasks if task in t]
            if found_tasks:
                self.show_popup("Found Tasks", "\n".join(found_tasks))
            else:
                self.show_popup("Not Found", "No matching tasks found.")

    def remove_task(self, instance):
        task = self.delete_task_input.text.strip()
        if task:
            tasks = self.load_tasks()
            if task in tasks:
                tasks.remove(task)
                self.save_all_tasks(tasks)
                self.show_popup("Success", "Task deleted successfully.")
            else:
                self.show_popup("Not Found", "Task not found.")

    def modify_task(self, instance):
        task = self.update_task_input.text.strip()
        if task:
            tasks = self.load_tasks()
            if task in tasks:
                tasks.remove(task)
                new_task = TextInput(hint_text='Enter the new task', size_hint_y=None, height=40)
                update_popup = Popup(title='Update Task', content=new_task, size_hint=(0.9, 0.5))
                update_popup.bind(on_dismiss=lambda *args: self.update_task(task, new_task.text, update_popup))
                update_popup.open()
            else:
                self.show_popup("Not Found", "Task not found.")

    def update_task(self, old_task, new_task, update_popup):
        if new_task.strip():
            tasks = self.load_tasks()
            tasks.append(new_task.strip())
            self.save_all_tasks(tasks)
            update_popup.dismiss()
            self.show_popup("Success", "Task updated successfully.")

    def show_tasks_popup(self):
        tasks = self.load_tasks()
        tasks_str = "\n".join(tasks) if tasks else "No tasks available."
        self.show_popup("All Tasks", tasks_str)

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.9, 0.5))
        popup.open()

    def save_task(self, task):
        with open("todo.txt", "a") as file_out:
            file_out.write(f"{task}\n")

    def load_tasks(self):
        if not os.path.exists("todo.txt"):
            return []
        with open("todo.txt", "r") as file_in:
            tasks = file_in.read().splitlines()
        return tasks

    def save_all_tasks(self, tasks):
        with open("todo.txt", "w") as file_out:
            for task in tasks:
                file_out.write(f"{task}\n")

if __name__ == "__main__":
    ToDoApp().run()
