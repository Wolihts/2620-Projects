import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import subprocess, os, sys, re

def fit_preview(img, max_dim=450):
    w, h = img.size
    s = min(1.0, max_dim / max(w, h))
    if s < 1.0:
        return img.resize((int(w * s), int(h * s)), Image.LANCZOS)
    return img

class App:
    def __init__(self, root):
        self.root = root
        root.title("Posterization")

        self.input_path = None
        self.tk_orig = None
        self.tk_post = None

        self.k = tk.IntVar(value=2)
        self.iters = tk.IntVar(value=1)

        top = tk.Frame(root)
        top.pack(padx=10, pady=8)

        tk.Button(top, text="load image", command=self.load).grid(row=0, column=0, padx=5)

        tk.Label(top, text="k").grid(row=0, column=1)
        tk.Scale(top, from_=2, to=20, orient="horizontal", variable=self.k, length=180)\
            .grid(row=0, column=2)

        tk.Label(top, text="iterations").grid(row=1, column=1)
        tk.Scale(top, from_=1, to=10, orient="horizontal", variable=self.iters, length=180)\
            .grid(row=1, column=2)

        self.btn_run = tk.Button(top, text="run", command=self.run, state="disabled")
        self.btn_run.grid(row=0, column=3, rowspan=2, padx=10)

        self.status = tk.Label(root, text="load an image")
        self.status.pack(pady=4)

        pics = tk.Frame(root)
        pics.pack(padx=10, pady=8)

        tk.Label(pics, text="original").grid(row=0, column=0)
        tk.Label(pics, text="posterized").grid(row=0, column=1)

        self.lbl_orig = tk.Label(pics, bg="#333")
        self.lbl_orig.grid(row=1, column=0, padx=6)

        self.lbl_post = tk.Label(pics, bg="#333")
        self.lbl_post.grid(row=1, column=1, padx=6)

    def load(self):
        path = filedialog.askopenfilename(
            filetypes=[("images", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("all", "*.*")]
        )
        if not path:
            return

        self.input_path = path
        img = fit_preview(Image.open(path))

        self.tk_orig = ImageTk.PhotoImage(img)
        self.lbl_orig.config(image=self.tk_orig)

        self.lbl_post.config(image="")
        self.tk_post = None

        self.btn_run.config(state="normal")
        self.status.config(text="ready")

    def patch_script_temp(self, script_path, k, iters, temp_path):
        txt = open(script_path, "r", encoding="utf-8").read()
        txt = re.sub(r'^\s*k\s*=\s*\d+\s*$', f'k = {k}', txt, flags=re.M)
        txt = re.sub(r'^\s*iterations\s*=\s*\d+\s*$', f'iterations = {iters}', txt, flags=re.M)
        open(temp_path, "w", encoding="utf-8").write(txt)

    def run(self):
        if not self.input_path:
            return

        base_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(base_dir, "posterization_ColorReduction_KMEANS.py")
        if not os.path.exists(script_path):
            self.status.config(text="missing posterization_ColorReduction_KMEANS.py next to index.py")
            return

        work_dir = os.path.dirname(self.input_path)
        old_cwd = os.getcwd()
        os.chdir(work_dir)

        with open(self.input_path, "rb") as f:
            data = f.read()
        with open("eagle.jpg", "wb") as f:
            f.write(data)

        k = self.k.get()
        it = self.iters.get()

        tmp_script = os.path.join(work_dir, "_tmp_run_posterize.py")
        self.patch_script_temp(script_path, k, it, tmp_script)

        self.status.config(text=f"running k={k}, iters={it}")
        self.root.update_idletasks()

        subprocess.run([sys.executable, tmp_script])

        if os.path.exists("posterized20.png"):
            out = fit_preview(Image.open("posterized20.png"))
            self.tk_post = ImageTk.PhotoImage(out)
            self.lbl_post.config(image=self.tk_post)
            self.status.config(text="done")
        else:
            self.status.config(text="ran script but posterized20.png not found")

        os.chdir(old_cwd)

root = tk.Tk()
App(root)
root.mainloop()
