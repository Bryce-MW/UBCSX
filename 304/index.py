#! /usr/bin/python3
from ubcsx import cursor, redirect, user

cursor.execute("SELECT 1 FROM owners WHERE owner=%s", (user,))
if cursor.rowcount:
    redirect("main.py")
else:
    redirect("new_user.py")
