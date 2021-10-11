import random
import tkinter as tk
import tkinter.messagebox as tmsg

def ButtonClick():
    b = editbox1.get()

    isok = False
    if len(b) != 4:
        tmsg.showerror("Error")
    else:
        kazuok = True
        for i in range(4):
            if (b[i] < "0") or (b[i] > "9"):
                tmsg.showerror("Error")
                kazuok = False
                break
        if kazuok:
            isok = True

    if isok:
        hit = 0
        for i in range(4):
            if a[i] == int(b[i]):
                hit = hit + 1
        blow = 0
        for j in range(4):
            for i in range(4):
                if (int(b[j]) == a[i]) and (a[i] != int(b[i])) and (a[j] != int(b[j])):
                    blow = blow + 1
                    break
        if hit == 4:
            tmsg.showinfo("Bingo")
            root.destroy()
        else:
            rirekibox.insert(tk.END, b + " /H:" + str(hit) + " B:" + str(blow) + "\n")

# ランダムな4つの整数を作る
a = [random.randint(0,9),
    random.randint(0,9),
    random.randint(0,9),
    random.randint(0,9)]

print(str(a[0]) + str(a[1]) + str(a[2]) + str(a[3]))

root = tk.Tk()
root.geometry("600x400")
root.title("hit&blow")

rirekibox = tk.Text(root, font=("Helvetica" , 14))
rirekibox.place(x = 400 , y = 0 , width = 200 , height = 400)

labell = tk.Label(root, text = "input a four digit number", font=("Helvetica",14))
labell.place(x = 20, y = 20)

editbox1 = tk.Entry(width = 4, font=("Helvetica", 28))
editbox1.place(x = 120, y = 60)

button1 = tk.Button(root, text = "check", font=("Helvetica",14), command=ButtonClick)
button1.place(x = 220, y = 60)

root.mainloop()    