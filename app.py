from tkinter import *
from tkinter import ttk, messagebox
from threading import Timer
import subprocess
import datetime 
import os


def get_processes_text():
    myoutput = open('procesos.txt', 'w')
    subprocess.call(['tasklist'], stdout=myoutput)
    tasks = open('procesos.txt') 
    tasks.readline()
    tasks.readline()
    tasks.readline()
    tasks.readline()
    texto = tasks.readlines()
    arreglo = []
    texto_total = ""
    for line in texto:
        texto_total = texto_total + line + "\n"
        linea = line.strip().split()
        arreglo.append({"Nombre":linea[0], "ID": linea[1], "Tipo": linea[2], "Num Sesión": linea[3], "Memoria": linea[4]})
    return texto_total

class NumeroApp:
  def __init__(self):
    self.num = 0
    f = open("abierto.txt", "w")
    f.write("")
    f.close()

numero_apps = NumeroApp()

def abrir_apps():
    f = open("abierto.txt", "a")
    app = "APP" + str(numero_apps.num)
    f.write(app + "\n")
    numero_apps.num = numero_apps.num + 1
    f.close()
    return app

def cierre_apps():
    f = open("abierto.txt")
    log = open('log.txt','a')
    for app in f.readlines():
        log.write('{cmd:stop, src: '+str(app.strip())+', dest:kernel, msg ="Se cerró"} -> '+str(datetime.datetime.now())+'\n')
    log.close()
    f.close()
    
    f = open("abierto.txt", "w")
    f.write("")
    f.close()


arreglo = get_processes_text()


def main(arreglo):
    log = open('log.txt','w')
    log_operaciones = "Inicio aplicación \n\n"
    window = Tk()
    window.title("Task manager Sistemas Operativos")
    window.geometry("500x500")
    tab_control = ttk.Notebook(window)
    # Funciones del Modulo GUI
    #Cerrando todas las instancias y procesos
    def destroy():
        if messagebox.askokcancel("Salir", "¿De verdad quiere cerrar?"):
            cierre_apps()
            log = open('log.txt','a')
            log.write('\n Etapa de finalización\n\n{cmd:END, src: aplicación, dest:kernel, msg ="Se cerró la aplicación por un modulo"} -> '+str(datetime.datetime.now())+'\n')
            log.close()
            window.destroy()

    # Inicialización de MODULO GUI
    tab1 = ttk.Frame(tab_control)
    tab_control.add(tab1, text='Modulo GUI')
    lbl1 = Label(tab1, text= "Cierra todo")
    btn = Button(tab1, text = 'Cerrar todas las instancias', bd = '5', command=destroy)
    btn.grid(column=1, row=0)
    lbl1.grid(column=0, row=0)
    
    
    
    def mod_app():
        tab3 = ttk.Frame(tab_control)
        tab_control.add(tab3, text='Modulo de aplicaciones')
        btn = Button(tab3, text = 'Cerrar todas las instancias', bd = '5', command=destroy)
        btn.grid(column=0, row=0)
        def destroy_tab():
            if messagebox.askokcancel("Salir", "¿De verdad quiere cerrar?"):
                cierre_apps()
                def destroy_all():
                    for widget in window.winfo_children():
                        if isinstance(widget, Toplevel):
                            widget.destroy()
                destroy_all()
                tab3.destroy()
        btn = Button(tab3, text = 'Cierra el modulo de aplicaciones', bd = '5', command=destroy_tab)
        btn.grid(column=1, row=0)
        btn = Button(tab3, text = 'Abrir aplicación', bd = '5', command=openNewWindow)
        lbl3 = Label(tab3, text= 'Solo se abrira multiples instancias de una app')
        lbl3.grid(column=0, row=1)
        btn.grid(column=1, row=1)
    lbld = Label(tab1, text= "Crear nuevo modulo de Aplicaciones")
    btn = Button(tab1, text = 'Crear modulo de aplicaciones', bd = '5', command=mod_app)
    btn.grid(column=1, row=1)
    lbld.grid(column=0, row=1)

    
    arreglo_var=StringVar()
    arreglo_var.set(arreglo)

    def mod_app_ac():
        arreglo = get_processes_text()
        arreglo_var.set(arreglo)
        lbl_texto = Label(tab1, text= arreglo)
        lbl_texto.grid(column = 0, row= 4)

    lbl0 = Label(tab1, text= "Lista de procesos")
    btn = Button(tab1, text = 'Actualizar', bd = '5', command=mod_app_ac)
    btn.grid(column=1, row=2)
    lbl0.grid(column=0, row=2)

    lbl_texto = Label(tab1, text= arreglo)
    lbl_texto.grid(column = 0, row= 4)






    log_operaciones = log_operaciones + "{cmd: info, src:GUI, dst: Kernel, msg: 'Listo'}-> "+str(datetime.datetime.now())+"\n"
    
    #Inicialiazicón modulo de archivos
    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab2, text='Modulo de archivos')
    lbl2 = Label(tab2, text= 'Cierra Todo')
    lbl2.grid(column=0, row=0)
    btn = Button(tab2, text = 'Cerrar todas las instancias', bd = '5', command=destroy)
    btn.grid(column=1, row=0)

    def mod_app_log():
        log = open('log.txt')
        texto = ""
        for line in log.readlines():
            texto = texto + line + "\n"
        lbl_texto = Label(tab2, text= texto)
        lbl_texto.grid(column = 0, row= 6)

    lbl0 = Label(tab2, text= "Log")
    btn = Button(tab2, text = 'Ver Log', bd = '5', command=mod_app_log)
    btn.grid(column=1, row=5)
    lbl0.grid(column=0, row=5)
    
    name_var=StringVar()
    passw_var=StringVar()
            
    # creating a label for
    # name using widget Label
    name_label = Label(tab2, text = 'Nombre carpeta a crear:', font=('calibre',10, 'bold'))
    name_label.grid(column=0, row=1)
    # creating a entry for input
    # name using widget Entry
    name_entry = Entry(tab2,textvariable = name_var, font=('calibre',10,'normal'))
    name_entry.grid(column=1,row=1)
    # creating a label for password
    passw_label = Label(tab2, text = 'Nombre carpeta a borrar:', font = ('calibre',10,'bold'))
    passw_label.grid(column=0,row=2)
    # creating a entry for password
    passw_entry= Entry(tab2, textvariable = passw_var, font = ('calibre',10,'normal'))
    passw_entry.grid(column=1,row=2)
    # creating a button using the widget
    # Button that will call the submit function
    def crear_carpeta():
        name=name_var.get()
        directory = name
        log = open('log.txt','a')
        log.write('{cmd:info, src: Modulo de archivos, dest:kernel, msg ="Se creo la carpeta '+name+'"} -> '+str(datetime.datetime.now())+'\n')
        log.close()
        parent_dir = "C:/Users/user/OneDrive - SociaBPO SAS 900.562.737-5/Escritorio/Proyecto sistemas operativos"
        path = os.path.join(parent_dir, directory) 
        os.mkdir(path) 

        name_var.set("")
        

    sub_btn=Button(tab2,text = 'Crear', command = crear_carpeta)
    sub_btn.grid(column=2,row=1)

    def eliminar_carpeta():
        password=passw_var.get()
        log = open('log.txt','a')
        log.write('{cmd:info, src: Modulo de archivos, dest:kernel, msg ="Se elemino la carpeta '+password+'"} -> '+str(datetime.datetime.now())+'\n')
        log.close()
        parent_dir = "C:/Users/user/OneDrive - SociaBPO SAS 900.562.737-5/Escritorio/Proyecto sistemas operativos"
        file_path = os.path.join(parent_dir, password)
        os.rmdir(file_path)

        passw_var.set("")

    sub_btn=Button(tab2,text = 'Borrar', command = eliminar_carpeta)
    sub_btn.grid(column=2,row=2)
    log_operaciones = log_operaciones + "{cmd: info, src:Modulo de archivos, dst: Kernel, msg: 'Listo'}-> "+str(datetime.datetime.now())+"\n"

    #Inicialización modulo de aplicaciones 
    tab3 = ttk.Frame(tab_control)
    tab_control.add(tab3, text='Modulo de aplicaciones')
    btn = Button(tab3, text = 'Cerrar todas las instancias', bd = '5', command=destroy)
    btn.grid(column=0, row=0)
    def destroy_tab():
        cierre_apps()
        def destroy_all():
            if messagebox.askokcancel("Salir", "¿De verdad quiere cerrar?"):
                for widget in window.winfo_children():
                    if isinstance(widget, Toplevel):
                        widget.destroy()
        destroy_all()
        tab3.destroy()
    btn = Button(tab3, text = 'Cierra el modulo de aplicaciones', bd = '5', command=destroy_tab)
    btn.grid(column=1, row=0)
    
    def openNewWindow():
        app = abrir_apps()
        log = open('log.txt','a')
        log.write('{cmd:info, src: '+str(app.strip())+', dest:kernel, msg ="'+str(app.strip())+'"} -> '+str(datetime.datetime.now())+'\n')
        log.close()
        # Toplevel object which will
        # be treated as a new window
        newWindow = Toplevel()
        newWindow.title(app)
        newWindow.geometry("500x500")
        lbl1 = Label(newWindow, text= "Cierra esta instancia")
        def mini_destroy():
            if messagebox.askokcancel("Salir", "¿De verdad quiere cerrar?"):
                f = open("abierto.txt")
                nuevo_texto = ""
                for app_num in f.readlines():
                    if app_num.strip() == app:
                        pass
                    else:
                        nuevo_texto = nuevo_texto + app_num.strip() + "\n"
                f.close()
                f = open("abierto.txt", "w")
                f.write(nuevo_texto)
                f.close()
                log = open('log.txt','a')
                log.write('{cmd:stop, src: '+str(app.strip())+', dest:kernel, msg ="Se cerró"} -> '+str(datetime.datetime.now())+'\n')
                log.close()
                newWindow.destroy()
        btn = Button(newWindow, text = 'Cerrar esta instancia', bd = '5', command=mini_destroy)
        btn.grid(column=1, row=0)
        lbl1.grid(column=0, row=0)


        lbl2 = Label(newWindow, text= "Enviar Error")
        def error():
            log = open('log.txt','a')
            log.write('{cmd:error, src: ' + app + ', dst:kernel, codterm:2,msg:"Err"} -> '+str(datetime.datetime.now())+'\n')
            log.close()
        btn = Button(newWindow, text = 'Generar Error', bd = '5', command=error)
        btn.grid(column=1, row=1)
        lbl2.grid(column=0, row=1)


        lbl3 = Label(newWindow, text= "Procesado")
        def procesado():
            log = open('log.txt','a')
            log.write('{cmd:proceso, src: ' + app + ', dst:kernel, codterm:0,msg:"OK"} -> '+str(datetime.datetime.now())+'\n')
            log.close()
        btn = Button(newWindow, text = 'Procesado', bd = '5', command=procesado)
        btn.grid(column=1, row=2)
        lbl3.grid(column=0, row=2)


        lbl4 = Label(newWindow, text= "Ocupado")
        def procesado():
            log = open('log.txt','a')
            log.write('{cmd:ocupado, src: ' + app + ', dst:kernel, codterm:1,msg:"0"} -> '+str(datetime.datetime.now())+'\n')
            
            def display():
                print("Esta ocupado")
            t = Timer(3, display)  
            t.start()
            log.write('{cmd:proceso, src: ' + app + ', dst:kernel, codterm:0,msg:"OK"}\n')
            log.close()
        btn = Button(newWindow, text = 'Ocupado', bd = '5', command=procesado)
        btn.grid(column=1, row=3)
        lbl4.grid(column=0, row=3)


        # sets the geometry of topleve
        def on_closing_app():
            if messagebox.askokcancel("Salir", "¿De verdad quiere cerrar?"):
                f = open("abierto.txt")
                nuevo_texto = ""
                for app_num in f.readlines():
                    if app_num.strip() == app:
                        pass
                    else:
                        nuevo_texto = nuevo_texto + app_num.strip() + "\n"
                f.close()
                f = open("abierto.txt", "w")
                f.write(nuevo_texto)
                f.close()
                log = open('log.txt','a')
                log.write('{cmd:stop, src: '+str(app.strip())+', dest:kernel, msg ="Se cerró"} -> '+str(datetime.datetime.now())+'\n')
                log.close()
                newWindow.destroy()
        newWindow.protocol("WM_DELETE_WINDOW", on_closing_app)


    btn = Button(tab3, text = 'Abrir aplicación', bd = '5', command=openNewWindow)
    lbl3 = Label(tab3, text= 'Solo se abrira multiples instancias de una app')
    lbl3.grid(column=0, row=1)
    btn.grid(column=1, row=1)


    log_operaciones = log_operaciones + "{cmd: info, src:Modulo de aplicaciones, dst: Kernel, msg: 'Listo'} -> "+str(datetime.datetime.now())+"\n"
    
    
    # Cuando se cierra con la ventana de windows
    def on_closing():
        if messagebox.askokcancel("Salir", "¿De verdad quiere cerrar?"):
            cierre_apps()
            log = open('log.txt','a')
            log.write('\n Etapa de finalización\n\n{cmd:END, src: aplicación, dest:kernel, msg ="Se cerró la aplicación desde windows"} -> '+str(datetime.datetime.now())+'\n')
            log.close()
            window.destroy()
    
    
    window.protocol("WM_DELETE_WINDOW", on_closing)
    log.write(log_operaciones + "\nEtapa de Mensajería\n")
    log.close()
    tab_control.pack(expand=1, fill='both')
    window.mainloop()


if __name__ == "__main__":
    #input(datetime.datetime.now())
    main(arreglo)
