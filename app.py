import customtkinter as ctk
from downloader import download_video
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")



def clear_status_after(delay_ms=4000):
    app.after(delay_ms, lambda: status.configure(text=""))



def start_download():
    url = entry.get().strip()

    if not url:
        status.configure(text="⚠️ Pega un enlace primero")
        clear_status_after()
        return

    status.configure(text="Descargando...")

    def task():
        try:
            success = download_video(url)

            if success:
                app.after(0, lambda: status.configure(text="✅ Descarga completa"))
                clear_status_after()
            else:
                app.after(0, lambda: status.configure(text="❌ Cancelado"))
                clear_status_after()

        except Exception as e:
            app.after(0, lambda: status.configure(text="❌ Error"))
            clear_status_after()
            print(e)

    threading.Thread(target=task, daemon=True).start()



app = ctk.CTk()
app.geometry("420x200")
app.title("YouTube Downloader")

title = ctk.CTkLabel(app, text="YouTube Video Downloader", font=("Arial", 18))
title.pack(pady=10)

entry = ctk.CTkEntry(
    app,
    width=320,
    placeholder_text="Pega aquí el enlace de YouTube..."
)
entry.pack(pady=15)

btn = ctk.CTkButton(app, text="Descargar", command=start_download)
btn.pack(pady=10)

status = ctk.CTkLabel(app, text="")
status.pack(pady=10)

app.mainloop()