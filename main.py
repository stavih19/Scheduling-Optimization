import tkinter as tk
from tkinter import filedialog
from convertCSV import run
from measurement import measurement

tasks_list_file = None
tasks_ids_file = None
soldiers_list_file = None


def main():
    create_window()


def create_window():
    window = tk.Tk()
    window.resizable(tk.FALSE, tk.FALSE)
    create_first_window(window)
    window.mainloop()


def create_first_window(window):
    window.title("Covid 19")
    window.geometry('730x750')
    background_color = '#e6d9b8'
    canvas = tk.Canvas(window, width=window.winfo_width(), height=window.winfo_height())
    canvas.pack(fill="both", expand=True)
    # image_background(canvas, "soldier_image.png")
    canvas.create_text(350, 100, text="SOLDIERS SHIFTS", font=("Bahnschrift Bold", 50))
    canvas.create_text(350, 155, text="Finding a schedule that satisfies all constraints", font=("Calibri", 20))

    add_button_choose(canvas, window, column_button=10, row_buttomn=18)


def image_background(canvas, img_file):
    background_label = tk.Label(canvas)
    background_label.image = tk.PhotoImage(file=img_file)
    background_label['image'] = background_label.image
    canvas.create_image(0, 0, image=background_label.image, anchor=tk.NW)


def add_button_choose(canvas, window, column_button, row_buttomn):
    ok_btn = tk.PhotoImage(file='images/ok2.png')
    img_label = tk.Label(canvas)
    img_label.image = ok_btn
    img_label['image'] = img_label.image
    # button 1
    btn = canvas.create_image(370, 235, image=ok_btn, anchor=tk.NW)
    canvas.tag_bind(btn, "<Button-1>", lambda eff: clicked_button_choose1(window, eff))
    canvas.create_text(200, 250, text="please upload 'tasks_list' file", font=("Bahnschrift", 15))

    # button 2
    btn = canvas.create_image(370, 285, image=ok_btn, anchor=tk.NW)
    canvas.tag_bind(btn, "<Button-1>", lambda eff: clicked_button_choose2(window, eff))
    canvas.create_text(200, 300, text="please upload 'tasks_ids' file", font=("Bahnschrift", 15))

    # button 3
    btn = canvas.create_image(370, 335, image=ok_btn, anchor=tk.NW)
    canvas.tag_bind(btn, "<Button-1>", lambda eff: clicked_button_choose3(window, eff))
    canvas.create_text(200, 350, text="please upload 'soldiers_list' file", font=("Bahnschrift", 15))

    # button 4
    btn = canvas.create_image(680, 370, image=ok_btn, anchor=tk.NW)
    canvas.tag_bind(btn, "<Button-1>", lambda eff: clicked_button_choose4(window, eff))
    canvas.create_text(630, 380, text="continue", font=("Bahnschrift", 15))


def clicked_button_choose1(window, eff=None):
    filename = filedialog.askopenfilename()
    globals()['tasks_list_file'] = filename


def clicked_button_choose2(window, eff=None):
    filename = filedialog.askopenfilename()
    globals()['tasks_ids_file'] = filename


def clicked_button_choose3(window, eff=None):
    filename = filedialog.askopenfilename()
    globals()['soldiers_list_file'] = filename


def clicked_button_choose4(window, eff=None):
    run(tasks_list_file, tasks_ids_file, soldiers_list_file, "first")
    measurement("first")
    run(tasks_list_file, tasks_ids_file, soldiers_list_file, "middle")
    measurement("middle")
    run(tasks_list_file, tasks_ids_file, soldiers_list_file, "last")
    measurement("last")
    print('finish!\n'
          'open "soldiers_shifts.csv" for solution')
    window.destroy()


# Display a Error Message Box
def _msgBox(window):
    window.showerror('Python Error Message', 'Error: You are Clicked ErrorMessage')


if __name__ == '__main__':
    main()
