import tkinter as tk

# Función para manejar el evento de cambio en la caja de entrada
def entry_changed(event):
    try:
        value = float(entry.get())
        label.config(text="Sueldo Bruto: $" + str(value), bg="#%02x%02x%02x" % (window.winfo_rgb(window["bg"])))
        slider_changed(slider.get(), slider2.get(), slider3.get(), label2, label21, label22, label3)
    except ValueError:
        label.config(text="¡Valor inválido! Introduzca un valor numérico", bg="red")

# Botón para aplicar el descuento sindical
def apply_discount():
    discount = 0.02
    initial_value = float(entry.get())
    sindical_discount = initial_value * discount
    label.config(text="Sueldo Bruto: $" + str(initial_value))
    label4.config(text="Descuento Sindical (2%): $" + str(sindical_discount))

# Función para manejar los controles deslizantes
def slider_changed(value, value1, value2, label2=None, label21=None, label22=None, label3=None):
    discount = float(value) / 100
    discount1 = float(value1) / 100
    discount2 = float(value2) / 100
    initial_value = float(entry.get())
    
    if discount + discount1 + discount2 <= 1:
        if label2:
            label2.config(text="Jubilacion(%): " + str(value))
        if label21:
            label21.config(text="Obra Social(%): " + str(value1))
        if label22:
            label22.config(text="PAMI(%): " + str(value2))
        
        if label3:
            discounted_value = initial_value * (1 - discount - discount1 - discount2)
            label3.config(text="Sueldo Neto: $" + str(round(discounted_value,3)))
            
            label_sliders.config(text="Elija porcentajes para cada categoría:\n", bg="#%02x%02x%02x" % (window.winfo_rgb(window["bg"])))

    else:
        label_sliders.config(text="¡Los porcentajes suman más que el 100%!\n Cambie los valores", bg="red")
  
# Crear la ventana principal
window = tk.Tk()

# Establecer el tamaño y la posición de la ventana
window.geometry("350x510")

# Crear la caja de entrada
entry = tk.Entry(window)
entry.bind("<Return>", entry_changed)  # Manejar el evento de cambio al presionar Enter

# Crear los controles deslizantes
slider = tk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL, command=lambda value: slider_changed(value, slider2.get(), slider3.get(), label2, label21, label22, label3))
slider2 = tk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL, command=lambda value: slider_changed(slider.get(), value, slider3.get(), label2, label21, label22, label3))
slider3 = tk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL, command=lambda value: slider_changed(slider.get(), slider2.get(), value, label2, label21, label22, label3))

# Crear las etiquetas
label = tk.Label(window, text="Ingresar Sueldo Bruto: ", font=("Arial", 9, "bold"))
label_sliders = tk.Label(window, text="Elija porcentajes para cada categería:\n", font=("Arial", 9, "bold"))
label2 = tk.Label(window, text="Jubilacion(%): ")
label21 = tk.Label(window, text="Obra Social(%): ")
label22 = tk.Label(window, text="PAMI(%): ")
label3 = tk.Label(window, text="Sueldo Neto: $0.00", bg="yellow", font=("Arial", 12, "bold"))
label4 = tk.Label(window, text="Descuento Sindical: $0.00")
apply_button = tk.Button(window, text="Calcular Descuento Sindical", command=apply_discount)

# Crear un widget de espacio
space_label = tk.Label(window, text="")
space_label1 = tk.Label(window, text="")
space_label2 = tk.Label(window, text="")
space_label3 = tk.Label(window, text="")
space_label4 = tk.Label(window, text="")
space_label5 = tk.Label(window, text="")
space_label6 = tk.Label(window, text="")

# Colocar los elementos en la ventana
space_label.pack()
label.pack()
entry.pack()
space_label1.pack()
apply_button.pack()
space_label2.pack()
label_sliders.pack()
space_label3.pack()
label2.pack()
slider.pack()
space_label4.pack()
label21.pack()
slider2.pack()
space_label5.pack()
label22.pack()
slider3.pack()
space_label6.pack()
label3.pack()
label4.pack()

# Ejecutar el bucle principal de la interfaz
window.mainloop()
