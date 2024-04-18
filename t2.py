import tkinter
import sqlite3

cnt=sqlite3.connect("shop.db")
session=False
#--------------functions-----------------     
def Login():
    global session
    user=txt_user.get()
    pas=txt_pass.get()
    sql=f'''SELECT * FROM users WHERE username="{user}" AND password="{pas}" '''
    result=cnt.execute(sql)
    rows=result.fetchall()
    if len(rows)<1:
        lbl_msg.configure(text="wrong username or passsword!", fg="red")    
    else:
        print(rows)
        session=rows[0][0]
        lbl_msg.configure(text='welcome to your account!', fg="green")
        txt_user.delete(0,"end")
        txt_pass.delete(0,"end")
        btn_Login.configure(state="disabled")
        btn_logout.configure(state="active")
        btn_shop.configure(state="active")
        
def logout():
    global session
    session=False
    btn_Login.configure(state="active")
    btn_logout.configure(state="disabled")
    lbl_msg.configure(text="you are logged out now!",fg="green")
    btn_shop.configure(state="disabled")

def submit():
    global session
    win_submit=tkinter.Toplevel(win)
    win_submit.title("Submit Panel")
    win_submit.geometry("500x400")
    lbl_info=tkinter.Label(win_submit,text="please fill the blanks: ",fg="pink")
    lbl_info.pack()
    lbl_username=tkinter.Label(win_submit,text="username: ")
    lbl_username.pack()
    
    user_entry=tkinter.Entry(win_submit)
    user_entry.pack()
    lbl_password=tkinter.Label(win_submit, text="password: ")
    lbl_password.pack()
    
    pas_entry=tkinter.Entry(win_submit)
    pas_entry.pack()
    lbl_addr=tkinter.Label(win_submit,text="address: ")
    lbl_addr.pack()
    addr_entry=tkinter.Entry(win_submit)
    addr_entry.pack()
    
    btn_NewSubmit=tkinter.Button(win_submit,text="submit",fg="green")
    btn_NewSubmit.pack()
    
    suser=user_entry.get()
    saddr=addr_entry.get()
    spas=pas_entry.get()
    
    sql='''INSERT into users(usernamr,password,address) VALUES("{suser}","{saddr}","{spas}")'''
    cnt.execute(sql)
    cnt.commit()
    win_submit.mainloop()
    
    
    
def view_chart():
    global session
    print("View Chart Button")
win=tkinter.Tk()
win.title("shopping cart")

shopping_cart_items=['Item 1', 'Item 2', 'Item 3']

pid=int(input("pid"))
pqnt=int(input("pqnt"))
sql=f'''SELECT * FROM products WHERE id="{pid}"'''
result=cnt.execute(sql)
rows=result.fetchall()


btn_view_chart=tkinter.Button(win,text="View Chart",fg="black")
btn_view_chart.pack()


def shop():
    def updateList():
         sql='''SELECT * FROM products'''
    result = cnt.execute(sql)
    rows=result.fetchall()
    
    for product in rows:
       info=f"product id:{product[0]}  name:{product[1]}  price:{product[2]}  quantity:{product[3]}"
       lst_product.insert("end", info)
        
    def pvalidate(pid,pqnt):
        if pid=="" or pqnt=="":
            return False,"please fill the blanks!"
        #--
        pid=int(pid)
        pqnt=int(pqnt)
        sql=f'''SELECT * FROM products WHERE id={pid}'''
        cnt.execute(sql)
        result=cnt.execute(sql)
        rows=result.fetchall()
        if len(rows)<1:
            return False, "invalid product id!"
        #--
        sql=f'''SELECT * FROM products WHERE id={pid} and qnt>{pqnt}'''
        result=cnt.execute(sql)
        rows=result.fetchall()
        if len(rows)<1:
            return False, "not enough products!"
        #--
        return True,""
    
    def buy():
        pid=txt_id.get()
        pqnt=txt_qnt.get()
        result,errorMSG=pvalidate(pid,pqnt)
        if  not result:
            lbl_msg2.configure(text=errorMSG,fg="red")
            return
        pid=int(pid)
        pqnt=int(pqnt)
        sql=f'''INSERT INTO cart(uid, pid,qnt) VALUES ({session},{pid},{pqnt})'''
        cnt.execute(sql)
        cnt.commit()
    #--
        sql=f'''UPDATE products SET qnt=qnt-{pqnt} WHERE id={pid}'''
        cnt.execute(sql)
        cnt.commit()
     #--
    lst_product.delete(0, "end")
    updateList()
            
    #--   
    txt_id.delete(0,"end")
    txt_qnt.delete(0,"end")
    lbl_msg2.configure(text="product has been added to your cart!",fg="green")
    
    win_shop=tkinter.Toplevel(win)
    win_shop.title("shop panel")
    win_shop.geometry("500x400")
   
    lst_product=tkinter.Listbox(win_shop,width=70,height=10,font="arial")
    lst_product.pack(pady=10)
    
    updateList()
    
    lbl_id=tkinter.Label(win_shop,text="Products id: ")
    lbl_id.pack()
    txt_id=tkinter.Entry(win_shop)
    txt_id.pack()

    lbl_qnt=tkinter.Label(win_shop,text="Product number: ")
    lbl_qnt.pack()
    txt_qnt=tkinter.Entry(win_shop)
    txt_qnt.pack()


    lbl_msg2=tkinter.Label(win_shop,text="")
    lbl_msg2.pack()
    
    btn_buy=tkinter.Button(win_shop,tex="BUY NOW!",command=buy)
    btn_buy.pack()
    
    win_shop.mainloop()
    
#---------------create window-------------
win=tkinter.Tk()
win.geometry("300x250")

lbl_user=tkinter.Label(win,text="Username: ")
lbl_user.pack()
txt_user=tkinter.Entry(win)
txt_user.pack()

lbl_pass=tkinter.Tk()
win.geometry("300x250")
lbl_pass=tkinter.Label(win,text="Password: ")
lbl_pass.pack()
txt_pass=tkinter.Entry(win)
txt_pass.pack()

lbl_msg=tkinter.Label(win,text="")
lbl_msg.pack()

btn_Login=tkinter.Button(win,text="Login",command=Login)
btn_Login.pack()

btn_logout=tkinter.Button(win, text="logout", command=logout, state="disabled")
btn_logout.pack()

btn_shop=tkinter.Button(win,text="shop", command=shop, state="disabled")
btn_shop.pack()

entry_username=tk.Entry(win)
entry_username.pack()

entry_password=tk.Entry(win, show="*")
entry_password.pack()

lbl_result=tk.Label(win, text="", fg="blue")
lbl_result.pack()

btn_submit=tkinter.Button(win,text="Submit",command=submit,fg="red")
btn_submit.pack()

lbl_cart=tkinter.Label(win, text="Shopping Cart Items")
lbl_cart.pack()

for items in shopping_cart_items:
    lbl_item=tkinter.Label(win,text="item")
    lbl_item.pack()
btn_view_chart=tkinter.Button(win, text="View Chart", command=view_chart)
btn_view_chart.pack() 

win.mainloop()
