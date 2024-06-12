import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

class ContactApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical')
        self.display_banner(root)

        # Create a layout for the buttons and center it
        buttons_layout = BoxLayout(orientation='vertical', size_hint=(None, None), size=(300, 400))
        buttons_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Add buttons for different actions
        add_contact_button = Button(text='Add Contact', size_hint=(None, None), size=(250, 50))
        add_contact_button.bind(on_press=self.add_new_contact)
        show_contacts_button = Button(text='Show Contacts', size_hint=(None, None), size=(250, 50))
        show_contacts_button.bind(on_press=self.display_contacts)
        search_contact_button = Button(text='Search Contact', size_hint=(None, None), size=(250, 50))
        search_contact_button.bind(on_press=self.search_for_contact)
        delete_contact_button = Button(text='Delete Contact', size_hint=(None, None), size=(250, 50))
        delete_contact_button.bind(on_press=self.delete_contact)
        update_contact_button = Button(text='Update Contact', size_hint=(None, None), size=(250, 50))
        update_contact_button.bind(on_press=self.update_contact)

        buttons_layout.add_widget(add_contact_button)
        buttons_layout.add_widget(show_contacts_button)
        buttons_layout.add_widget(search_contact_button)
        buttons_layout.add_widget(delete_contact_button)
        buttons_layout.add_widget(update_contact_button)

        root.add_widget(buttons_layout)

        return root

    def display_banner(self, root):
        banner = Label(text="CONTACT INFORMATION MANAGER", font_size='24sp')
        root.add_widget(banner)

    def add_new_contact(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10)
        name_input = TextInput(hint_text='Name')
        phone_input = TextInput(hint_text='Phone Number')
        email_input = TextInput(hint_text='Email')
        address_input = TextInput(hint_text='Address')
        save_button = Button(text='Save')
        save_button.bind(on_press=lambda instance: self.save_contact(name_input.text, phone_input.text, email_input.text, address_input.text))
        content.add_widget(name_input)
        content.add_widget(phone_input)
        content.add_widget(email_input)
        content.add_widget(address_input)
        content.add_widget(save_button)

        popup = Popup(title='Add New Contact',
                      content=content,
                      size_hint=(None, None), size=(400, 300))
        popup.open()

    def save_contact(self, name, phone, email, address):
        # Change the path to the desired location
        file_path = "python/projects/contact list/contacts.txt"
        with open(file_path, "a") as file_out:
            file_out.write(f"Name: {name}, Phone: {phone}, Email: {email}, Address: {address}\n")

        success_popup = Popup(title='Success',
                              content=Label(text='Contact successfully saved!'),
                              size_hint=(None, None), size=(200, 100))
        success_popup.open()

    def display_contacts(self, instance):
        # Change the path to the desired location
        file_path = "python/projects/contact list/contacts.txt"
        contacts_str = ""
        try:
            with open(file_path, "r") as file:
                contacts_str = file.read()
        except FileNotFoundError:
            contacts_str = "No contacts available."

        content = Label(text=contacts_str)
        popup = Popup(title='All Contacts',
                      content=content,
                      size_hint=(None, None), size=(400, 300))
        popup.open()

    def search_for_contact(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10)
        search_input = TextInput(hint_text='Enter name or phone number to search')
        search_button = Button(text='Search')
        content.add_widget(search_input)
        content.add_widget(search_button)

        popup = Popup(title='Search Contact',
                      content=content,
                      size_hint=(None, None), size=(400, 300))
        popup.open()

    def delete_contact(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10)
        delete_input = TextInput(hint_text='Enter name or phone number to delete')
        delete_button = Button(text='Delete')
        delete_button.bind(on_press=lambda instance: self.perform_delete(delete_input.text))
        content.add_widget(delete_input)
        content.add_widget(delete_button)

        popup = Popup(title='Delete Contact',
                      content=content,
                      size_hint=(None, None), size=(400, 300))
        popup.open()

    def perform_delete(self, contact_info):
        # Change the path to the desired location
        file_path = "python/projects/contact list/contacts.txt"
        try:
            with open(file_path, "r") as file:
                lines = file.readlines()
            with open(file_path, "w") as file:
                for line in lines:
                    if contact_info not in line:
                        file.write(line)
        except FileNotFoundError:
            pass

        success_popup = Popup(title='Success',
                              content=Label(text='Contact successfully deleted!'),
                              size_hint=(None, None), size=(200, 100))
        success_popup.open()

    def update_contact(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10)
        update_input = TextInput(hint_text='Enter name or phone number to update')
        update_button = Button(text='Update')
        content.add_widget(update_input)
        content.add_widget(update_button)

        popup = Popup(title='Update Contact',
                      content=content,
                      size_hint=(None, None), size=(400, 300))
        popup.open()

if __name__ == "__main__":
    ContactApp().run()
