import os
import tkinter as tk
from tkinter import PhotoImage

class AdventureGame:
    def __init__(self, master, story_file):
        self.master = master
        master.title("Adventure Game")
        self.master.geometry('760x1000')
        self.master.minsize(760, 950)
        self.master.maxsize(760, 1200)
        self.story_file = story_file
        self.story = {}
        self.load_story()
        self.current_moment = 'start'
        self.create_widgets()
        self.update_moment()

    def load_story(self):
        with open(self.story_file, 'r') as f:
            lines = f.readlines()
            moment_name = ''
            moment_text = ''
            moment_image = ''
            moment_choices = []
            story_folder = os.path.dirname(self.story_file)
            for line in lines:
                if line.startswith('moment:'):
                    if moment_name:
                        self.story[moment_name] = {
                            'text': moment_text,
                            'image': moment_image,
                            'choices': moment_choices
                        }
                    moment_name = line.split(':')[1].strip()
                    moment_text = ''
                    moment_image = ''
                    moment_choices = []
                elif line.startswith('text:'):
                    moment_text = line.split(':')[1].strip()
                elif line.startswith('image:'):
                    image_filename = line.split(':')[1].strip()
                    moment_image = os.path.join(story_folder, image_filename)
                elif line.startswith('choice:'):
                    choice_text, choice_moment = line.split(':')[1].split('->')
                    choice_text = choice_text.strip()
                    choice_moment = choice_moment.strip()
                    moment_choices.append((choice_text, choice_moment))
            if moment_name:
                self.story[moment_name] = {
                    'text': moment_text,
                    'image': moment_image,
                    'choices': moment_choices
                }

    def create_widgets(self):
        self.image_label = tk.Label(self.master)
        self.image_label.pack(fill=tk.BOTH)
        self.text_label = tk.Label(self.master, wraplength=740, font=("roboto", 13))
        self.text_label.pack(fill=tk.X, expand=True)
        self.choice_frame = tk.Frame(self.master)
        self.choice_frame.pack(fill=tk.Y, anchor="center")

    def update_moment(self):
        moment_data = self.story[self.current_moment]
        image_file = moment_data['image']
        image = PhotoImage(file=image_file)
        self.image_label.config(image=image)
        self.image_label.image = image
        text = moment_data['text']
        self.text_label.config(text=text)
        choices = moment_data['choices']
        for widget in self.choice_frame.winfo_children():
            widget.destroy()
        for choice_text, choice_moment in choices:
            button = tk.Button(self.choice_frame, text=choice_text, font=("roboto", 11),
                               command=lambda m=choice_moment: self.choose(m))
            button.pack(side=tk.LEFT)

    def choose(self, moment):
        if moment == 'game_over':
            self.current_moment = 'start'
        elif moment == 'main_menu':
            self.master.destroy()
            root = tk.Tk()
            main_menu = MainMenu(root)
            root.mainloop()
        else:
            self.current_moment = moment
        self.update_moment()

class MainMenu:
    def __init__(self, master):
        self.master = master
        self.master.geometry('400x400')
        self.master.minsize(400, 400)
        self.master.maxsize(400, 800)
        master.title("Game Selection")
        self.create_widgets()

    def create_widgets(self):
        story_folders = [folder for folder in os.listdir("stories") if os.path.isdir(os.path.join("stories", folder))]
        for folder in story_folders:
            button = tk.Button(self.master, text=folder, font=("roboto", 11), command=lambda f=folder: self.start_story(f))
            button.pack(pady=5)

    def start_story(self, folder, moment='start'):
        story_file = os.path.join("stories", folder, f"{folder}.txt")
        self.master.destroy()
        root = tk.Tk()
        game = AdventureGame(root, story_file)
        game.current_moment = moment
        root.mainloop()

def main():
    root = tk.Tk()
    main_menu = MainMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()