import customtkinter as tk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def run(model):

    #functions
    def change_params():
        model.params['k'] = int(ans_k.get())
        model.params['a'] = int(ans_a.get())
        model.params['b'] = int(ans_b.get())
        model.params['A'] = int(ans_A.get())
        ans_k.delete(0, "end")
        ans_a.delete(0, "end")
        ans_b.delete(0, "end")
        ans_A.delete(0, "end")

    def view_model():
        # additional window init
        img_window = tk.CTkToplevel(window)
        img_window.geometry("500x100")
        img_window.title("Model")
        img_window.grab_set()

        canvas = tk.CTkCanvas(img_window, width=600, height=120)
        canvas.pack()
        canvas.create_image(0,0,image = model_img, anchor ="nw")

    def view_plot():
        canvas = FigureCanvasTkAgg(model.fig, master=window)
        canvas.get_tk_widget().place(x=565, y=120)

    def stability_status():
        if model.check_stability():
            status = "stable"
        else: status = "not stable"

        tk.CTkLabel(window,
                    text=f"Model is {status}",
                    font=("None", 15, "bold"),
                    fg_color="transparent",
                    text_color="#f3ffff").place(x=640, y=600)

    #window init
    window = tk.CTk()
    window.geometry("1200x700")
    window.configure(bg="#202020")
    tk.set_appearance_mode("dark")
    window.title("Symulacja układu zamkniętego z regulatorem P")

    #img init
    model_img = ImageTk.PhotoImage( Image.open("assets/model.png").resize((600, 120)))
    square_img = ImageTk.PhotoImage(Image.open("assets/square_signal.png").resize((180,40)))
    step_img = ImageTk.PhotoImage(Image.open("assets/step_signal.png").resize((180,40)))
    sin_img = ImageTk.PhotoImage(Image.open("assets/sin_signal.png").resize((180,40)))
    image_img = ImageTk.PhotoImage(Image.open("assets/image.png").resize((30,30)))

    #entries
    ans_k = tk.CTkEntry(window, width=100, corner_radius=5)
    ans_k.place(x=96, y= 70)
    ans_a = tk.CTkEntry(window, width=100, corner_radius=5)
    ans_a.place(x=96, y= 120)
    ans_b = tk.CTkEntry(window, width=100, corner_radius=5)
    ans_b.place(x=96, y= 170)
    ans_A = tk.CTkEntry(window, width=100, corner_radius=5)
    ans_A.place(x=96, y= 220)

    #text
    tk.CTkLabel(window,
                text = "Choose parameters",
                font=("None", 15, "bold"),
                fg_color="transparent",
                text_color="#f3ffff").place(x=20, y=27)

    tk.CTkLabel(window,
                text="Parameter k",
                fg_color="transparent",
                text_color="#f3ffff").place(x=20, y= 70)

    tk.CTkLabel(window,
                text="Parameter a",
                fg_color="transparent",
                text_color="#f3ffff").place(x=20, y= 120)

    tk.CTkLabel(window,
                text="Parameter b",
                fg_color="transparent",
                text_color="#f3ffff").place(x=20, y= 170)

    tk.CTkLabel(window,
                text="Parameter A",
                fg_color="transparent",
                text_color="#f3ffff").place(x=20, y= 220)

    tk.CTkLabel(window,
                text = "Choose input signal",
                font=("None", 15, "bold"),
                fg_color="transparent",
                text_color="#f3ffff").place(x=20, y=330)

    #buttons
    submit_button = tk.CTkButton(window,
                                 text="Submit",
                                 fg_color="#c258f8",
                                 hover_color="#844af7",
                                 text_color="#f3ffff",
                                 width=100,
                                 corner_radius=5,
                                 command=change_params)
    submit_button.place(x=96, y= 260)

    square_input = tk.CTkButton(window,
                                text = None,
                                fg_color="#c258f8",
                                hover_color="#844af7",
                                image=square_img,
                                width=170,
                                height=40,
                                corner_radius=5,
                                command = lambda:[model.generate_square_input(), model.draw_response(), view_plot()])
    square_input.place(x=20, y= 370)

    step_input = tk.CTkButton(window,
                              text = None,
                              fg_color="#c258f8",
                              hover_color="#844af7",
                              image=step_img,
                              width=170,
                              height=40,
                              corner_radius=5,
                              command=lambda:[model.generate_step_input(), model.draw_response(), view_plot()])
    step_input.place(x=20, y= 425)

    sin_input = tk.CTkButton(window,
                             text = None,
                             fg_color="#c258f8",
                             hover_color="#844af7",
                             image=sin_img,
                             width=170,
                             height=40,
                             corner_radius=5,
                             command=lambda:[model.generate_sin_input(), model.draw_response(), view_plot()])
    sin_input.place(x=20, y= 480)

    stability_button = tk.CTkButton(window,
                                    text ="Check stability",
                                    font=("None", 13, "bold"),
                                    fg_color="#c258f8",
                                    hover_color="#844af7",
                                    width=170,
                                    height=40,
                                    corner_radius=5,
                                    command=stability_status)
    stability_button.place(x=20, y=580)

    root_button = tk.CTkButton(window,
                               text ="Draw root locus",
                               font=("None", 13, "bold"),
                               fg_color="#c258f8",
                               hover_color="#844af7",
                               width=170,
                               height=40,
                               corner_radius=5,
                               command=lambda:[model.draw_root_locus(), view_plot()])
    root_button.place(x=20, y=630)

    model_button = tk.CTkButton(window,
                                text = None,
                                fg_color="transparent",
                                hover_color="#844af7",
                                image=image_img,
                                width=30,
                                height=30,
                                corner_radius=5,
                                command=view_model)
    model_button.place(x=1140, y=25)


    window.mainloop()



