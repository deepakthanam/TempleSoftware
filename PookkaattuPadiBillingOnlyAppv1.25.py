
#!/usr/bin/python

import mysql.connector
import datetime
import os
import codecs
from escpos import printer
from escpos.printer import Usb

#from PrintFunctions2 import PrintPoojaOfferings
#from PrintFunctions import PrintPoojaOfferings
from tkcalendar import Calendar, DateEntry

from DatabaseFunctions import *
from PrintFunctions import *
from PrintFunctions import PrintPoojaOfferings
from GeneralFunctions import *

global PoojaNameSelected
global ChangeFlag 
OPTIONSBOOKEDINFORMATION = []


def AddPoojaDatabase(top,PoojaName,PoojaAmount):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="templeadmin",
    database="pkt_temple",
    auth_plugin='mysql_native_password'
    )
    mycursor = mydb.cursor()
#   a =  str(value)
#   PoojaNameSelected = a
#   print("Pooja selected in first function is "+PoojaNameSelected) 

    try:


        SQL1 = 'SELECT MAX(POOJAID) FROM pkt_temple.POOJAINFORMATION';

        mycursor.execute(SQL1)
        Maxvalue =  mycursor.fetchone()
#    Maxvalue = Maxvalue
 #   print Maxvalue[0]

        newmaxvalue = Maxvalue[0] + 1
         
        SQL2 = "insert into pkt_temple.POOJAINFORMATION values ("+str(newmaxvalue)+','+"'"+str(PoojaName).upper()+"'"+","+"1,"+"'2100-12-31',"+str(PoojaAmount)+",'BOTH');"
        print SQL2 
  
        mycursor.execute(SQL2)
        mydb.commit()
        top.destroy()
    
    except mysql.connector.Error, e:
        MessageBox.showerror("Error", "Please check the values")  
    

    mycursor.close()
    mydb.close()


def AddPoojaList(AppRoot):
    top = Toplevel(AppRoot)        
    PoojaNameLabel = Label(top, font=('calibri',8,'bold'), text="Pooja Name", bd=16, anchor='w',width=15,bg="white")
    PoojaNameLabel.grid(row=0,column=0,sticky="ew")
    PoojaNameEntry = Entry(top, font=('calibri', 8, 'bold'), text='PoojaName', bd=3,bg="white",width=30)
    PoojaNameEntry.grid(row=0,column=1,sticky="ew")
    PoojaAmountLabel = Label(top, font=('calibri',8,'bold'), text="Pooja Amount", bd=16, anchor='w',width=15,bg="white")
    PoojaAmountLabel.grid(row=0,column=2,sticky="ew")
    PoojaAmountEntry = Entry(top, font=('calibri', 8, 'bold'), text='PoojaAmount', bd=3,bg="white",width=10)
    PoojaAmountEntry.grid(row=0,column=3,sticky="ew")
    SubmitPoojaButton = Button(top, font=('calibri',8,'bold'), text="Submit", activebackground="white", width=15, padx=2, pady=2,
        bg='red', bd=3, fg='white', justify=CENTER, command= lambda : AddPoojaDatabase(top,str(Entry(top).getvar("PoojaName")),str(Entry(top).getvar("PoojaAmount"))))
    SubmitPoojaButton.grid(row=1,column=0,sticky="ew")
    top.mainloop()
     


def WriteManualPooja(PoojaEntry):
    file1 = open("Mode.txt","w")
    file1.write("2")
    file1.close

    PoojaValueEntered = PoojaEntry.get()

    file1 = open("MyFile.txt","a")
    file1.write("PoojaNameSelected:"+PoojaValueEntered+"&")
    file1.close()


#..........................Selecting the pooja amount value for the Pooja..................
def ComboFunction(event):

    Selection = event.widget.get()
    print str(Selection)

    
    PoojaNameSelected = str(Selection)
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="templeadmin",
    database="pkt_temple",
    auth_plugin='mysql_native_password'
    )
    mycursor = mydb.cursor()
#   a =  str(value)
#   PoojaNameSelected = a
#   print("Pooja selected in first function is "+PoojaNameSelected)
    SQL = "select POOJAAMOUNT from pkt_temple.POOJAINFORMATION where POOJANAME="+"'"+str(PoojaNameSelected)+"'"+";"
    mycursor.execute(SQL)
    a=[i[0] for i in mycursor.fetchall()]
    AmountValue = a[0]
    AmountMenu = Label(BillingFrame, font=('calibri',8,'bold'), text=AmountValue, bd=16, anchor='w')
    AmountMenu.configure(width=15,bg="white")
    AmountMenu.grid(row=2,column=1,sticky="ew")

    file1 = open("MyFile.txt","a")
    file2 = open("Poojaamount.txt","w")
    file3 = open("Poojacount.txt","r")

    file1.write("PoojaNameSelected:"+PoojaNameSelected+"&")
    file1.write("PoojaAmount:"+str(AmountValue)+"&")

    file2.write(str(AmountValue))

    Poojacount = file3.read()

    file1.close()
    file2.close()
    file3.close()

    if( str(PoojaNameSelected) == 'DONATION' ):
        print('Inside function donation')
	top = Toplevel(AppRoot)        
	LabelDonation = Label(top, font=('calibri',8,'bold'), text="Donation Amount", bd=16, anchor='w')
	LabelDonation.configure(width=15,bg="white")
	LabelDonation.grid(row=0,column=0)

        DonationAmount = Entry(top, font=('calibri',8,'bold'), text="Amount", bd=16)
        DonationAmount.grid(row=0,column=1,sticky="ew")


        SubmitButton = Button(top, font=('calibri',8,'bold'), text="Submit Donation", activebackground="white", padx=2, pady=2,
        bg='red', bd=3, fg='white', justify=CENTER, command= lambda : Donationvaluesubmit(str(Entry(top).getvar("Amount")),top))
        SubmitButton.configure(width=15)
        SubmitButton.grid(row=1,column=10,sticky="ew")

	top.mainloop()

        file2 = open("Poojaamount.txt","r")
        AmountValue = float(file2.read())
        file2.close()


    if( str(PoojaNameSelected) == 'ENNA'):
        print('Inside function donation')
	top = Toplevel(AppRoot)        
	LabelEnna= Label(top, font=('calibri',8,'bold'), text="ENNA", bd=16, anchor='w')
	LabelEnna.configure(width=15,bg="white")
	LabelEnna.grid(row=0,column=0)

        DonationAmount = Entry(top, font=('calibri',8,'bold'), text="Amount", bd=16)
        DonationAmount.grid(row=0,column=1,sticky="ew")


        SubmitButton = Button(top, font=('calibri',8,'bold'), text="Submit Enna", activebackground="white", padx=2, pady=2,
        bg='red', bd=3, fg='white', justify=CENTER, command= lambda : Ennavaluesubmit(str(Entry(top).getvar("Amount")),top))
        SubmitButton.configure(width=15)
        SubmitButton.grid(row=1,column=10,sticky="ew")

	top.mainloop()

        file2 = open("Poojaamount.txt","r")
        AmountValue = float(file2.read())
        file2.close()

    if( str(PoojaNameSelected) == 'HUNDI COLLECTION'): 
        #print('Inside function donation')
	top = Toplevel(AppRoot)        
	LabelEnna= Label(top, font=('calibri',8,'bold'), text="Hundi collection", bd=16, anchor='w')
	LabelEnna.configure(width=15,bg="white")
	LabelEnna.grid(row=0,column=0)

        DonationAmount = Entry(top, font=('calibri',8,'bold'), text="Amount", bd=16)
        DonationAmount.grid(row=0,column=1,sticky="ew")


        SubmitButton = Button(top, font=('calibri',8,'bold'), text="Submit Hundi", activebackground="white", padx=2, pady=2,
        bg='red', bd=3, fg='white', justify=CENTER, command= lambda : Ennavaluesubmit(str(Entry(top).getvar("Amount")),top))
        SubmitButton.configure(width=15)
        SubmitButton.grid(row=1,column=10,sticky="ew")

	top.mainloop()

        file2 = open("Poojaamount.txt","r")
        AmountValue = float(file2.read())
        file2.close()

 #   print("Poojacount is"+Poojacount)
    if str(Poojacount)=="":
        Poojacount=str(1)
  #      print("Poojacount is"+Poojacount)

    if int(Poojacount)>1:
        TotalAmountValue = float(AmountValue)*int(Poojacount)
        TotalAmountPooja = Label(BillingFrame, font=('calibri',8,'bold'), text="Total Amount", bd=16, anchor='w')
        TotalAmountPooja.configure(width=15,bg="white")
        TotalAmountPooja.grid(row=2,column=2,sticky="ew")
        TotalAmountPoojaValue = Label(BillingFrame, font=('calibri',8,'bold'), text=str(TotalAmountValue), bd=16, anchor='w')
        TotalAmountPoojaValue.configure(width=15,bg="white")
        TotalAmountPoojaValue.grid(row=2,column=3,sticky="ew")
    else:
        if int(Poojacount)==1:
  #          print("Pooja amount total"+ str(AmountValue))
            TotalAmountPooja = Label(BillingFrame, font=('calibri',8,'bold'), text="Total Amount", bd=16, anchor='w')
            TotalAmountPooja.configure(width=15,bg="white")
            TotalAmountPooja.grid(row=2,column=2,sticky="ew")
            TotalAmountPoojaValue = Label(BillingFrame, font=('calibri',8,'bold'), text=str(AmountValue), bd=16, anchor='w')
            TotalAmountPoojaValue.configure(width=15,bg="white")
            TotalAmountPoojaValue.grid(row=2,column=3,sticky="ew")

    mycursor.close()
    mydb.close()



def WriteManualPoojaAmoun(PoojaAmountEntry):

    file1 = open("Mode.txt","w")
    file1.write("2")
    file1.close

    PoojaAmountValueEntered = PoojaAmountEntry.get()

    file1 = open("MyFile.txt","a")
    file1.write("PoojaAmount:"+str(PoojaAmountValueEntered)+"&")
    file1.close()


def ManualEntry():

    PoojaEntry = Entry(BillingFrame, font=('calibri', 8, 'bold'), text='PoojaSelectedManual', command=lambda : WriteManualPooja(PoojaEntry), bd=3)
    PoojaEntry.config(bg="white",width=15)
    PoojaEntry.grid(row=1,column=1,sticky="ew")

    PoojaAmountEntry = Entry(BillingFrame, font=('calibri', 8, 'bold'), text='PoojaAmountManual',command=lambda : WriteManualPoojaAmount(PoojaAmountEntry), bd=3)
    PoojaAmountEntry.config(bg="white",width=5)
    PoojaAmountEntry.grid(row=2,column=1,sticky="ew")    


def DeleteBilling():
    DeleteBookingEntry = Entry(BillingFrame, font=('calibri', 8, 'bold'), text='BookingID', bd=16)
    DeleteBookingEntry.configure(width=15)
    DeleteBookingEntry.insert(0, "ENTER BOOKING NO")
    DeleteBookingEntry.grid(row=13, column=0)

    DeletePoojaButton = Button(BillingFrame, font=('calibri',8,'bold'), text="DELETE BOOKING", activebackground="white", padx=2,
    pady=2,bg='red',bd=3, fg='white', command=lambda : DeleteBookingDB(DeleteBookingEntry.get()), justify=CENTER)
    DeletePoojaButton.configure(width=30)
    DeletePoojaButton.grid(row=13, column=1)


def DeleteBookingDB(BookingNo):

    LabelBlankSpace4 = Label(BillingFrame, font=('calibri',8,'bold'), text="", bd=16, anchor='w')
    LabelBlankSpace4.configure(bg="white")
    LabelBlankSpace4.configure(width=25,bg="white",fg="white")
    LabelBlankSpace4.grid(row=13, column=0)

    LabelBlankSpace4 = Label(BillingFrame, font=('calibri',8,'bold'), text="", bd=16, anchor='w')
    LabelBlankSpace4.configure(bg="white")
    LabelBlankSpace4.configure(width=25,bg="white",fg="white")
    LabelBlankSpace4.grid(row=13, column=1)

    LabelBlankSpace4 = Label(BillingFrame, font=('calibri',8,'bold'), text="", bd=16, anchor='w')
    LabelBlankSpace4.configure(bg="white")
    LabelBlankSpace4.configure(width=25,bg="white",fg="white")
    LabelBlankSpace4.grid(row=13, column=2)

    LabelBlankSpace4 = Label(BillingFrame, font=('calibri',8,'bold'), text="", bd=16, anchor='w')
    LabelBlankSpace4.configure(bg="white")
    LabelBlankSpace4.configure(width=25,bg="white",fg="white")
    LabelBlankSpace4.grid(row=14, column=0)

    LabelBlankSpace4 = Label(BillingFrame, font=('calibri',8,'bold'), text="", bd=16, anchor='w')
    LabelBlankSpace4.configure(bg="white")
    LabelBlankSpace4.configure(width=25,bg="white",fg="white")
    LabelBlankSpace4.grid(row=14, column=2)

    LabelBlankSpace4 = Label(BillingFrame, font=('calibri',8,'bold'), text="", bd=16, anchor='w')
    LabelBlankSpace4.configure(bg="white")
    LabelBlankSpace4.configure(width=25,bg="white",fg="white")
    LabelBlankSpace4.grid(row=14, column=3)
    
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="templeadmin",
    database="pkt_temple",
    auth_plugin='mysql_native_password'
    )
  
    intBookingNo = int(BookingNo)

    SQL = "DELETE FROM pkt_temple.BOOKINGHISTORY WHERE BOOKINGID="+BookingNo+";"
    mycursor = mydb.cursor()
    mycursor.execute(SQL)
    mydb.commit()
    
    mycursor.close()
    mydb.close()
   


def viewPoojaDetailsonDay(Epson, BookedPooja,Datevalue): 

    viewPoojaname = BookedPooja
    viewDatevalue = str(Datevalue)    
  
#   print(BookedPooja+viewDatevalue)

   
    Epson.text('\n'+viewPoojaname+'\n'+'\n')
    

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="templeadmin",
        database="pkt_temple",
        auth_plugin='mysql_native_password'
    )

    mycursor = mydb.cursor()

    SQL = "select DEVOTEE1NAME,DEVOTEE2NAME,DEVOTEE3NAME,DEVOTEE4NAME,DEVOTEE5NAME,DEVOTEE1STAR,DEVOTEE2STAR,DEVOTEE3STAR,DEVOTEE4STAR,DEVOTEE5STAR from pkt_temple.BOOKINGHISTORY where POOJANAME=" + "'" +viewPoojaname+ "'" + "and POOJADATE=" + "'" +viewDatevalue+ "'"+';'
#    print SQL

    mycursor.execute(SQL)

#    print('PoojaName:'+viewPoojaname)

    for row in mycursor.fetchall():
	print('\t'+row[0].upper()+'\n'+'\t'+row[5].upper()+'\n')
        Epson.text('\t'+row[0].upper()+'\n'+'\t'+row[5].upper()+'\n'+'\n')
#       file1.write(row[0]+'\t'+row[5]+'\t')
#        fullline = row[0]+'\t'+row[5]+'\t'
        if row[1]!='No':
#            line1 = row[1]+'\t'+row[6]+'\t'
#            file1.write(line1)
#            fullline = fullline + line1
             print(row[1]+'\t'+row[6]+'\t')
             Epson.text('\t'+row[1].upper()+'\n'+'\t'+row[6].upper()+'\n'+'\n')
        if row[2]!= 'No':
#            line2 = row[2]+'\t'+row[7]+'\t'
#            file1.write(line2)
#            fullline = fullline + line2
            print(row[2]+'\t'+row[7]+'\t')
            Epson.text('\t'+row[2].upper()+'\n'+'\t'+row[7].upper()+'\n'+'\n')
        if row[3]!= 'No':
#            file1.write('\n')
#            line3 = row[3]+'\t'+row[8]+'\t'
#            file1.write(line3)
            print(row[3]+'\t'+row[8]+'\t')
            Epson.text('\t'+row[3].upper()+'\n'+'\t'+row[8].upper()+'\n'+'\n')
        if row[4]!= 'No':
#            line4 = row[4]+'\t'+row[9]+'\t'
#            file1.write(line4)
#            fullline = fullline + line4
            print(row[4]+'\t'+row[9]+'\t')
            Epson.text('\t'+row[4].upper()+'\n'+'\t'+row[9].upper()+'\n'+'\n')
            

   #     print(fullline)
   #      if(len(fullline)>25):
   #          file1.write('\n')
   #        fullline =""


    Epson.text('**************************')

    Epson.text('\n')
    Epson.text('\n')
    Epson.text('\n')
    Epson.text('\n')    
    Epson.text('\n')


 #   os.startfile(Filename, "print")


    mycursor.close()
    mydb.close()


def RemoveDuplicate(BookedPoojaList): 
    UniquePoojas = [] 
    for num in BookedPoojaList: 
        if num not in UniquePoojas: 
            UniquePoojas.append(num) 
    return UniquePoojas 

def viewPoojaBookedPoojaDetailsonDay(Datevalue): 

    print('Date selected:'+str(Datevalue))

    Epson = Usb(0x04b8, 0x0046)
    Epson = printer.Usb(0x04b8, 0x0046)
    Epson.text('POOJAS BOOKED :'+str(Datevalue)+'\n')

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="templeadmin",
    database="pkt_temple",
    auth_plugin='mysql_native_password'
    )

    mycursor = mydb.cursor()

    Query1 = 'SELECT POOJANAME from pkt_temple.BOOKINGHISTORY where POOJADATE='+"'"+str(Datevalue)+"'"+';'
    print(Query1)
 
    mycursor.execute(Query1)
    AllBookedPoojas=[i[0] for i in mycursor.fetchall()]

    UniquePoojas = RemoveDuplicate(AllBookedPoojas) 

    for BookedPooja in UniquePoojas:
        print(BookedPooja) 
        viewPoojaDetailsonDay(Epson,BookedPooja,Datevalue)


    Epson.text('\n')
    Epson.text('\n')
    Epson.text('\n')
    Epson.text('\n')
    Epson.text('\n')
    Epson.text('\n')
    Epson.text('\n')
    Epson.text('\n')
    Epson.text('\n')
    Epson.text('\n')
    Epson.text('\n')
    Epson.text('\n')    
    Epson.text('\n')
    Epson.text('\n')
 
    mycursor.close()
    mydb.close()


def ViewPooja(Root):

    OPTIONSBOOKEDINFORMATION = []

#    ViewPooja1Entry = Entry(BillingFrame, font=('calibri', 8, 'bold'), text='viewPoojaValue', bd=16)
#    ViewPooja1Entry.configure(width=15)
#    ViewPooja1Entry.insert(0, "ENTER POOJA NAME")
#    ViewPooja1Entry.grid(row=13, column=0)

    ViewPoojaDate1Entry = DateEntry(BillingFrame, width=12, font=('calibri',8,'bold'), background='darkblue', foreground='white', borderwidth=2)
    ViewPoojaDate1Entry.grid(row=13, column=0)
    

    ViewPoojaButton1 = Button(BillingFrame, font=('calibri', 8, 'bold'), name='printBookedPoojas', text="PRINT BOOKED POOJAS", command=lambda : viewPoojaBookedPoojaDetailsonDay(ViewPoojaDate1Entry.get_date()), padx=2, pady=2, bg='red', bd=3)
    ViewPoojaButton1.configure(width=30, bg="red")
    ViewPoojaButton1.grid(row=13, column=1)

    ViewPoojaButton2 = Button(BillingFrame, font=('calibri', 8, 'bold'), name='viewBookedPoojas', text="VIEW BOOKED POOJAS", command=lambda : setPoojaBookedPoojaDetailsonDay(ViewPoojaDate1Entry.get_date(),Root), padx=2, pady=2, bg='red', bd=3)
    ViewPoojaButton2.configure(width=25, bg="red")
    ViewPoojaButton2.grid(row=13, column=2)


    #...........Pooja selection.............

    OPTIONSBOOKEDINFORMATION = GetBookedInformation(str(ViewPoojaDate1Entry.get_date()))

    print OPTIONSBOOKEDINFORMATION

    OPTIONSBOOKEDINFORMATION.sort()

    OPTIONSALLBOOKEDPOOJANAME = [i[0] for i in OPTIONSBOOKEDINFORMATION]

    OPTIONSBOOKEDPOOJAS = RemoveDuplicate(OPTIONSALLBOOKEDPOOJANAME)

    PoojaMenu1 = OptionMenu(BillingFrame, variable10, *OPTIONSBOOKEDPOOJAS, command=func8)
    PoojaMenu1.config(font=('calibri',8,'bold'),bg="white",)
    PoojaMenu1.config(width=15)
    StringPooja1 = str(OPTIONSBOOKEDPOOJAS[0])
    PoojaMenu1.setvar(StringPooja1)
    PoojaMenu1.grid(row=14,column=0,sticky="ew")


#    ViewPoojaDate1Entry = Entry(BillingFrame, font=('calibri', 8, 'bold'), text='viewPoojaDateEntry', bd=16)
#    ViewPoojaDate1Entry.configure(width=15)
#    ViewPoojaDate1Entry.insert(0, "ENTER DATE")
#    ViewPoojaDate1Entry.grid(row=13, column=1)

#    ViewPoojaDateButton = Button(BillingFrame, font=('calibri', 8, 'bold'), name='viewDetails', text="VIEW DETAILS", command=lambda : viewPoojaDetailsonDay(), padx=2, pady=2, bg='red', bd=3)
#    ViewPoojaDateButton.configure(width=15, bg="white")
#    ViewPoojaDateButton.grid(row=13, column=2)


def setPoojaBookedPoojaDetailsonDay(Datevalue,Root):

       
    OPTIONSPOOJANAME= []
    OPTIONSPOOJAAMOUNT= []
    OPTIONSBOOKEDINFORMATION= []
    OPTIONSBOOKEDPOOJAS= []

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="templeadmin",
    database="pkt_temple",
    auth_plugin='mysql_native_password'
    )

    mycursor = mydb.cursor()

    Query1 = "select POOJANAME,POOJAAMOUNT from pkt_temple.BOOKINGHISTORY where POOJADATE="+"'"+str(Datevalue)+"'"+";"
    print("Set query is"+Query1)
    mycursor.execute(Query1)
    OPTIONSPOOJAINFORMATION = mycursor.fetchall()
#    OPTIONSPOOJANAME = [i[0] for i in mycursor.fetchall()]
#    print(OPTIONSPOOJAINFORMATION)
#    OPTIONSPOOJAAMOUNT = [i[1] for i in mycursor.fetchall()]
    mycursor.close()
    mydb.close()
    # print("Hallo")
    # print(OPTIONSPOOJAAMOUNT.len())
    # print(OPTIONSPOOJAINFORMATION[0])
    # print(OPTIONSPOOJAINFORMATION[1])
#    OPTIONSPOOJANAME = OPTIONSPOOJAINFORMATION[][0]


    #...........Pooja selection.............

    OPTIONSBOOKEDINFORMATION = GetBookedInformation(str(Datevalue))

    #print OPTIONSBOOKEDINFORMATION

    OPTIONSBOOKEDINFORMATION.sort()

    OPTIONSALLBOOKEDPOOJANAME = [i[0] for i in OPTIONSBOOKEDINFORMATION]

    OPTIONSBOOKEDPOOJAS = RemoveDuplicate(OPTIONSALLBOOKEDPOOJANAME)

    print OPTIONSBOOKEDPOOJAS

    PoojaMenu1 = OptionMenu(BillingFrame, variable10, *OPTIONSBOOKEDPOOJAS, command=func8)
    PoojaMenu1.config(font=('calibri',8,'bold'),bg="white",)
    PoojaMenu1.config(width=15)
    StringPooja1 = str(OPTIONSBOOKEDPOOJAS[0])
    PoojaMenu1.setvar(StringPooja1)
    PoojaMenu1.grid(row=14,column=0,sticky="ew")

    ViewPoojaButton2 = Button(BillingFrame, font=('calibri', 8, 'bold'), name='viewSelectedPoojas', text="VIEW SELECTED POOJAS", command=lambda : viewPoojaSelectedPooja(str(Datevalue),Root), padx=2, pady=2, bg='red', bd=3)
    ViewPoojaButton2.configure(width=25, bg="red")
    ViewPoojaButton2.grid(row=14, column=1)

    ViewPoojaButton3 = Button(BillingFrame, font=('calibri', 8, 'bold'), name='printSelectedPoojas', text="PRINT SELECTED POOJAS", command=lambda : printPoojaSelectedPooja(str(Datevalue),Root), padx=2, pady=2, bg='red', bd=3)
    ViewPoojaButton3.configure(width=25, bg="red")
    ViewPoojaButton3.grid(row=14, column=2)

#    return OPTIONSPOOJAINFORMATION


def ResetBilling():

    NOOFPOOJAMENU = [
    1,2,3,4,5
    ]

    variable7.set(NOOFPOOJAMENU[0])
 
    file2 = open("MyFile.txt","w")
    file2.write("")
    file2.close()
    NoofPoojaMenu = OptionMenu(BillingFrame, variable7, *NOOFPOOJAMENU, command=func6)
    NoofPoojaMenu.config(font=('calibri',8,'bold'),bg="white",takefocus=1)
    NoofPoojaMenu.config(width=15)
    NoofPoojaMenu.grid(row=10,column=1,sticky="ew")
    file3 = open("Poojacount.txt","w")
    file3.write(str(1))
    file3.close()

    LabelDateValue.set_date(datetime.date.today())
#    LabelDateValue = DateEntry(BillingFrame, width=12, font=('calibri',8,'bold'), background='darkblue', foreground='white', borderwidth=2)
#    LabelDateValue.grid(row=9,column=1)

    EntryName1.delete(0,50)
    EntryName2.delete(0,50)
    EntryName3.delete(0,50)
    EntryName4.delete(0,50)
    EntryName5.delete(0,50)
    EntryPhone1.delete(0,50)
   
def viewPoojaSelectedPooja(Date1,Root):    
    file3 = open("SelectedPooja.txt","r")
    PoojaName =  file3.readline()

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="templeadmin",
    database="pkt_temple",
    auth_plugin='mysql_native_password'
    )

    mycursor = mydb.cursor()

    Query ="SELECT BOOKINGID,DEVOTEE1NAME,DEVOTEE2NAME,DEVOTEE3NAME,DEVOTEE4NAME,DEVOTEE5NAME,DEVOTEE1STAR,DEVOTEE2STAR,DEVOTEE3STAR,DEVOTEE4STAR,DEVOTEE5STAR from pkt_temple.BOOKINGHISTORY where POOJANAME="+"'"+str(PoojaName)+"'"+" and POOJADATE="+"'"+str(Date1)+"'"+";"
    print(Query)

    mycursor.execute(Query)
#    BOOKEDINFO = mycursor.fetchall()

    win = Toplevel(Root)
    win.config(bg='red',padx=10,pady=10)

    win.wm_title(PoojaName)
    win.config(width=150)

    scrollbar = Scrollbar(win)
    scrollbar.pack( side = RIGHT, fill=Y )
 
    mylist = Listbox(win, yscrollcommand = scrollbar.set, width=40, height=600)

    x=1

    for row in mycursor.fetchall():
	line = 'BOOKING ID: '+ str(row[0])+'   '
        mylist.insert(END, "" + str(line)) 
        mylist.pack( side = LEFT, fill = BOTH )
        
        line = '      '+ str(x)+")  "+ row[1].upper()+'   '+row[6].upper()+'   '
 #   	print('\t'+row[0].upper()+'\n'+'\t'+row[5].upper()+'\n')
        mylist.insert(END, "" + str(line)) 
        mylist.pack( side = LEFT, fill = BOTH )
        scrollbar.config( command = mylist.yview )
        mylist.insert(END, "" + "")
        mylist.pack( side = LEFT, fill = BOTH ) 
        x=x+1

  #   	Entry1Name = Label(win, font=('calibri',8,'bold'), text=row[0], bd=16, anchor='w')
  #  	Entry1Name.configure(width=15,bg="white")
   #   	Entry1Name.grid(row=x,column=0)
  #       Entry1Nakshatram = Label(win, font=('calibri',8,'bold'), text=row[5], bd=16, anchor='w')
   #  	Entry1Nakshatram.configure(width=15,bg="white")
   #  	Entry1Nakshatram.grid(row=x,column=1)

    #Epson.text('\t'+row[0].upper()+'\n'+'\t'+row[5].upper()+'\n'+'\n')
#       file1.write(row[0]+'\t'+row[5]+'\t')
#        fullline = row[0]+'\t'+row[5]+'\t'
        if row[2]!='No':
             line ='     '+str(x)+")  "+row[2].upper()+' '+row[7].upper()+'   '
 #   	print('\t'+row[0].upper()+'\n'+'\t'+row[5].upper()+'\n')
             mylist.insert(END, "" + str(line)) 
             mylist.pack( side = LEFT, fill = BOTH )
             scrollbar.config( command = mylist.yview )             
             mylist.insert(END, "" + "")
             mylist.pack( side = LEFT, fill = BOTH ) 
             x=x+1

#             Entry2Name = Label(win, font=('calibri',8,'bold'), text=row[1], bd=16, anchor='w')
#    	     Entry2Name.configure(width=15,bg="white")
#    	     Entry2Name.grid(row=x,column=2)
#             Entry2Nakshatram = Label(win, font=('calibri',8,'bold'), text=row[6], bd=16, anchor='w')
#    	     Entry2Nakshatram.configure(width=15,bg="white")
#    	     Entry2Nakshatram.grid(row=x,column=3)
#            line1 = row[1]+'\t'+row[6]+'\t'
#            file1.write(line1)
#            fullline = fullline + line1
             print(row[1]+'\t'+row[6]+'\t')
#              Epson.text('\t'+row[1].upper()+'\n'+'\t'+row[6].upper()+'\n'+'\n')
        if row[3]!= 'No':
             line ='      '+str(x)+")  "+row[3].upper()+' '+row[8].upper()+'   '
 #   	print('\t'+row[0].upper()+'\n'+'\t'+row[5].upper()+'\n')
             mylist.insert(END, "" + str(line)) 
             mylist.pack( side = LEFT, fill = BOTH )
             scrollbar.config( command = mylist.yview )

             mylist.insert(END, "" + "")
             mylist.pack( side = LEFT, fill = BOTH ) 
             x=x+1

#              Entry3Name = Label(win, font=('calibri',8,'bold'), text=row[2], bd=16, anchor='w')
#     	     Entry3Name.configure(width=15,bg="white")
#     	     Entry3Name.grid(row=x,column=4)
#              Entry3Nakshatram = Label(win, font=('calibri',8,'bold'), text=row[7], bd=16, anchor='w')
#     	     Entry3Nakshatram.configure(width=15,bg="white")
#     	     Entry3Nakshatram.grid(row=x,column=5)
#            line2 = row[2]+'\t'+row[7]+'\t'
#            file1.write(line2)
#            fullline = fullline + line2
             print(row[2]+'\t'+row[7]+'\t')
#              Epson.text('\t'+row[2].upper()+'\n'+'\t'+row[7].upper()+'\n'+'\n')
        if row[4]!= 'No':
             line ='      '+str(x)+")  "+row[4].upper()+' '+row[9].upper()+'   '
 #   	print('\t'+row[0].upper()+'\n'+'\t'+row[5].upper()+'\n')
             mylist.insert(END, "" + str(line)) 
             mylist.pack( side = LEFT, fill = BOTH )
             scrollbar.config( command = mylist.yview )
             mylist.insert(END, "" + "")
             mylist.pack( side = LEFT, fill = BOTH ) 
             x=x+1

#            Entry4Name = Label(win, font=('calibri',8,'bold'), text=row[3], bd=16, anchor='w')
#    	     Entry4Name.configure(width=15,bg="white")
#    	     Entry4Name.grid(row=x,column=6)
#            Entry4Nakshatram = Label(win, font=('calibri',8,'bold'), text=row[8], bd=16, anchor='w')
#    	     Entry4Nakshatram.configure(width=15,bg="white")
#    	     Entry4Nakshatram.grid(row=x,column=7)

#            file1.write('\n')
#            line3 = row[3]+'\t'+row[8]+'\t'
#            file1.write(line3)
             print(row[3]+'\t'+row[8]+'\t')
#             Epson.text('\t'+row[3].upper()+'\n'+'\t'+row[8].upper()+'\n'+'\n')

        if row[5]!= 'No':
             line ='      '+str(x)+")  "+row[5].upper()+'\t'+row[10].upper()+'   '
 #   	print('\t'+row[0].upper()+'\n'+'\t'+row[5].upper()+'\n')
             mylist.insert(END, "" + str(line)) 
             mylist.pack( side = LEFT, fill = BOTH )
             scrollbar.config( command = mylist.yview )
             mylist.insert(END, "" + "")
             mylist.pack( side = LEFT, fill = BOTH )
             x=x+1

#            Entry5Name = Label(win, font=('calibri',8,'bold'), text=row[4], bd=16, anchor='w')
#    	     Entry5Name.configure(width=15,bg="white")
#    	     Entry5Name.grid(row=x,column=8)
#            Entry5Nakshatram = Label(win, font=('calibri',8,'bold'), text=row[8], bd=16, anchor='w')
#    	     Entry5Nakshatram.configure(width=15,bg="white")
#    	     Entry5Nakshatram.grid(row=x,column=9)
#            line4 = row[4]+'\t'+row[9]+'\t'
#            file1.write(line4)
#            fullline = fullline + line4
             print(row[4]+'\t'+row[9]+'\t')
#            Epson.text('\t'+row[4].upper()+'\n'+'\t'+row[9].upper()+'\n'+'\n')

        

#    OPTIONSPOOJANAME = [i[0] for i in mycursor.fetchall()]
#    print(OPTIONSPOOJAINFORMATION)
#    OPTIONSPOOJAAMOUNT = [i[1] for i in mycursor.fetchall()]

    mycursor.close()
    mydb.close()

def printPoojaSelectedPooja(Date1,Root):

    Epson = Usb(0x04b8, 0x0046)
    Epson = printer.Usb(0x04b8, 0x0046)
   
    
    file3 = open("SelectedPooja.txt","r")
    PoojaName =  file3.readline()
    Epson.text(PoojaName+'\n')
    Epson.text('Date:'+str(Date1)+'\n')
    Epson.text('**********************'+'\n')

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="templeadmin",
    database="pkt_temple",
    auth_plugin='mysql_native_password'
    )

    mycursor = mydb.cursor()

    Query ="SELECT DEVOTEE1NAME,DEVOTEE2NAME,DEVOTEE3NAME,DEVOTEE4NAME,DEVOTEE5NAME,DEVOTEE1STAR,DEVOTEE2STAR,DEVOTEE3STAR,DEVOTEE4STAR,DEVOTEE5STAR from pkt_temple.BOOKINGHISTORY where POOJANAME="+"'"+str(PoojaName)+"'"+" and POOJADATE="+"'"+str(Date1)+"'"+";"
    print(Query)

    mycursor.execute(Query)
#    BOOKEDINFO = mycursor.fetchall()

#    win = Toplevel(Root)
#    win.config(bg='red',padx=10,pady=10)
#    win.wm_title(PoojaName)

    x=1

    for row in mycursor.fetchall():
    	print('\n'+'\t'+row[0].upper()+'\n'+'\t'+row[5].upper()+'\n'+'\n')
    #	Entry1Name = Label(win, font=('calibri',8,'bold'), text=row[0], bd=16, anchor='w')
    #	Entry1Name.configure(width=15,bg="white")
    #	Entry1Name.grid(row=x,column=0)
    #    Entry1Nakshatram = Label(win, font=('calibri',8,'bold'), text=row[5], bd=16, anchor='w')
    #	Entry1Nakshatram.configure(width=15,bg="white")
    #	Entry1Nakshatram.grid(row=x,column=1)

        Epson.text('\n'+'\t'+str(x)+') '+row[0].upper()+'\n'+'\t'+row[5].upper()+'\n'+'\n')
        x=x+1
#       file1.write(row[0]+'\t'+row[5]+'\t')
#        fullline = row[0]+'\t'+row[5]+'\t'
        if row[1]!='No':
#            Entry2Name = Label(win, font=('calibri',8,'bold'), text=row[1], bd=16, anchor='w')
#     	     Entry2Name.configure(width=15,bg="white")
#    	     Entry2Name.grid(row=x,column=2)
#            Entry2Nakshatram = Label(win, font=('calibri',8,'bold'), text=row[6], bd=16, anchor='w')
#     	     Entry2Nakshatram.configure(width=15,bg="white")
#     	     Entry2Nakshatram.grid(row=x,column=3)
#            line1 = row[1]+'\t'+row[6]+'\t'
#            file1.write(line1)
#            fullline = fullline + line1
             x=x+1
             print(row[1]+'\t'+row[6]+'\t') 
             Epson.text('\n'+'\t'+str(x)+') '+row[1].upper()+'\n'+'\t'+row[6].upper()+'\n'+'\n')
        if row[2]!= 'No':
#            Entry3Name = Label(win, font=('calibri',8,'bold'), text=row[2], bd=16, anchor='w')
#     	     Entry3Name.configure(width=15,bg="white")
#     	     Entry3Name.grid(row=x,column=4)
#            Entry3Nakshatram = Label(win, font=('calibri',8,'bold'), text=row[7], bd=16, anchor='w')
#     	     Entry3Nakshatram.configure(width=15,bg="white")
#     	     Entry3Nakshatram.grid(row=x,column=5)
#            line2 = row[2]+'\t'+row[7]+'\t'
#            file1.write(line2)
#            fullline = fullline + line2
             x=x+1
             print(row[2]+'\t'+row[7]+'\t')
             Epson.text('\n'+'\t'+str(x)+') '+row[2].upper()+'\n'+'\t'+row[7].upper()+'\n'+'\n')
        if row[3]!= 'No':
#            Entry4Name = Label(win, font=('calibri',8,'bold'), text=row[3], bd=16, anchor='w')
#    	     Entry4Name.configure(width=15,bg="white")
#    	     Entry4Name.grid(row=x,column=6)
#            Entry4Nakshatram = Label(win, font=('calibri',8,'bold'), text=row[8], bd=16, anchor='w')
#    	     Entry4Nakshatram.configure(width=15,bg="white")
#    	     Entry4Nakshatram.grid(row=x,column=7)

#            file1.write('\n')
#            line3 = row[3]+'\t'+row[8]+'\t'
#            file1.write(line3)
             x=x+1
             print(row[3]+'\t'+row[8]+'\t')
             Epson.text('\n'+'\t'+str(x)+') '+row[3].upper()+'\n'+'\t'+row[8].upper()+'\n'+'\n')
        if row[4]!= 'No':
#            Entry5Name = Label(win, font=('calibri',8,'bold'), text=row[4], bd=16, anchor='w')
#    	     Entry5Name.configure(width=15,bg="white")
#    	     Entry5Name.grid(row=x,column=8)
#            Entry5Nakshatram = Label(win, font=('calibri',8,'bold'), text=row[8], bd=16, anchor='w')
#    	     Entry5Nakshatram.configure(width=15,bg="white")
#    	     Entry5Nakshatram.grid(row=x,column=9)
#            line4 = row[4]+'\t'+row[9]+'\t'
#            file1.write(line4)
#            fullline = fullline + line4
             x=x+1
             print(row[4]+'\t'+row[9]+'\t')
             Epson.text('\n'+'\t'+str(x)+') '+row[4].upper()+'\n'+'\t'+row[9].upper()+'\n'+'\n')
             Epson.text('\n')

#       x=x+1

#    OPTIONSPOOJANAME = [i[0] for i in mycursor.fetchall()]
#    print(OPTIONSPOOJAINFORMATION)
#    OPTIONSPOOJAAMOUNT = [i[1] for i in mycursor.fetchall()]

    Epson.text('**********************'+'\n')

    Epson.text('\n')
    Epson.text('\n')
    Epson.text('\n')
    Epson.text('\n')
    Epson.text('\n')
    Epson.text('\n')
    Epson.text('\n')
    Epson.text('\n')
    Epson.text('\n')
    Epson.text('\n')
    Epson.text('\n')
    Epson.text('\n')
    Epson.text('\n')
    Epson.text('\n')
    Epson.text('\n')
    Epson.text('\n')

    
    mycursor.close()
    mydb.close()    
    

def ChangeToList():

    file1 = open("Mode.txt","w")
    file1.write('0')
    file1.close

    PoojaMenu = ttk.Combobox(BillingFrame, values=OPTIONSPOOJANAME)
    PoojaMenu.config(font=('calibri',8,'bold'))
    PoojaMenu.config(width=30)
    PoojaMenu.current(0)
    PoojaMenu.grid(row=1,column=1,sticky="ew")
    PoojaMenu.bind("<<ComboboxSelected>>", ComboFunction)

    #PoojaMenu = OptionMenu(BillingFrame, variable1, *OPTIONSPOOJANAME, command=func)
    #PoojaMenu.config(font=('calibri',8,'bold'),bg="white",)
    #PoojaMenu.config(width=15)
    #StringPooja1 = str(OPTIONSPOOJANAME[0])
    #PoojaMenu.setvar(StringPooja1)
    #PoojaMenu.grid(row=1,column=1,sticky="ew")


def Donationvaluesubmit(DonationAmount,top):
    file2 = open("Poojaamount.txt","w")
    file2.write(str(DonationAmount))    
    file2.close()
    top.destroy()
    AmountMenu = Label(BillingFrame, font=('calibri',8,'bold'), text=str(DonationAmount), bd=16, anchor='w')
    AmountMenu.configure(width=15,bg="white")
    AmountMenu.grid(row=2,column=1,sticky="ew")
    TotalAmountPooja = Label(BillingFrame, font=('calibri',8,'bold'), text="Total Amount", bd=16, anchor='w')
    TotalAmountPooja.configure(width=15,bg="white")
    TotalAmountPooja.grid(row=2,column=2,sticky="ew")
    TotalAmountPoojaValue = Label(BillingFrame, font=('calibri',8,'bold'), text=str(DonationAmount), bd=16, anchor='w')
    TotalAmountPoojaValue.configure(width=15,bg="white")
    TotalAmountPoojaValue.grid(row=2,column=3,sticky="ew")

 

def Ennavaluesubmit(DonationAmount,top):
    file2 = open("Poojaamount.txt","w")
    file2.write(str(DonationAmount))    
    file2.close()
    top.destroy()
    AmountMenu = Label(BillingFrame, font=('calibri',8,'bold'), text=str(DonationAmount), bd=16, anchor='w')
    AmountMenu.configure(width=15,bg="white")
    AmountMenu.grid(row=2,column=1,sticky="ew")
    TotalAmountPooja = Label(BillingFrame, font=('calibri',8,'bold'), text="Total Amount", bd=16, anchor='w')
    TotalAmountPooja.configure(width=15,bg="white")
    TotalAmountPooja.grid(row=2,column=2,sticky="ew")
    TotalAmountPoojaValue = Label(BillingFrame, font=('calibri',8,'bold'), text=str(DonationAmount), bd=16, anchor='w')
    TotalAmountPoojaValue.configure(width=15,bg="white")
    TotalAmountPoojaValue.grid(row=2,column=3,sticky="ew")


def func6(value):  

    file2 = open("Poojaamount.txt","r")
    file3 = open("Poojacount.txt","w")
    file3.write(str(value))
    Amountvalue = file2.read()  

    if len(Amountvalue)>2:
        TotalAmountValue = int(value)*float(Amountvalue)
        TotalAmountPooja = Label(BillingFrame, font=('calibri',8,'bold'), text="Total Amount", bd=16, anchor='w')
        TotalAmountPooja.configure(width=15,bg="white")
        TotalAmountPooja.grid(row=2,column=2,sticky="ew")
        TotalAmountPoojaValue = Label(BillingFrame, font=('calibri',8,'bold'), text=str(TotalAmountValue), bd=16, anchor='w')
        TotalAmountPoojaValue.configure(width=15,bg="white")
        TotalAmountPoojaValue.grid(row=2,column=3,sticky="ew")
    else:
        TotalAmountValue = Label(BillingFrame, font=('calibri',8,'bold'), text="Total Amount", bd=16, anchor='w')
        TotalAmountValue.configure(width=15,bg="white")
        TotalAmountValue.grid(row=2,column=2,sticky="ew")
        TotalAmountPoojaValue = Label(BillingFrame, font=('calibri',8,'bold'), text='0.00', bd=16, anchor='w')
        TotalAmountPoojaValue.configure(width=15,bg="white")
        TotalAmountPoojaValue.grid(row=2,column=3,sticky="ew")
    file2.close()
    file3.close()


def ChangeOfferingDate(FrameName):
   file1 = open("MyFile.txt","a")
   file1.write("DatechangeFlag:1&")
   file1.close()
   DateBox = Entry(FrameName, font=('calibri',8,'bold'), text="Date", bd=16)
   DateBox.delete(0,10)
   DateBox.insert(0,"2019-mm-dd")
   DateBox.configure(width=15,bg="white")
   DateBox.grid(row=9,column=1)
   TodayButton = Button(BillingFrame, font=('calibri',8,'bold'), text="Today",activebackground="white", padx=2, pady=2, bg='red', bd=3, fg='white', justify=CENTER, command= lambda : ChangeToToday(FrameName))
   TodayButton.configure(width=15)
   TodayButton.grid(row=9,column=2,sticky="ew")

def ChangeToToday(FrameName):
   file1 = open("MyFile.txt","a")
   file1.write("DatechangeFlag:0&")
   file1.close()
#  variabledate = StringVar(FrameName)
   variabledate = str(date.today())
   LabelDateValue = Label(BillingFrame, font=('calibri',8,'bold'), text=variabledate, bd=16, anchor='w')
   LabelDateValue.configure(width=15,bg="white")
   LabelDateValue.grid(row=9,column=1)
   ChangeDateButton = Button(BillingFrame, font=('calibri',8,'bold'), text="Change date", activebackground="white", padx=2, pady=2, bg='red', bd=3, fg='white', justify=CENTER, command= lambda : ChangeOfferingDate(FrameName))
   ChangeDateButton.configure(width=15)
   ChangeDateButton.grid(row=9,column=2,sticky="ew")

#..........................Selecting the pooja amount value for the Pooja..................
def func(value):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="templeadmin",
    database="pkt_temple",
    auth_plugin='mysql_native_password'
    )
    mycursor = mydb.cursor()
    a =  str(value)
    PoojaNameSelected = a
 #   print("Pooja selected in first function is "+PoojaNameSelected)
    SQL = "select POOJAAMOUNT from pkt_temple.POOJAINFORMATION where POOJANAME="+"'"+a+"'"+";"
    mycursor.execute(SQL)
    a=[i[0] for i in mycursor.fetchall()]
    AmountValue = a[0]
    AmountMenu = Label(BillingFrame, font=('calibri',8,'bold'), text=AmountValue, bd=16, anchor='w')
    AmountMenu.configure(width=15,bg="white")
    AmountMenu.grid(row=2,column=1,sticky="ew")

    file1 = open("MyFile.txt","a")
    file2 = open("Poojaamount.txt","w")
    file3 = open("Poojacount.txt","r")

    file1.write("PoojaNameSelected:"+PoojaNameSelected+"&")
    file1.write("PoojaAmount:"+str(AmountValue)+"&")

    file2.write(str(AmountValue))

    Poojacount = file3.read()
 #   print("Poojacount is"+Poojacount)
    if str(Poojacount)=="":
        Poojacount=str(1)
  #      print("Poojacount is"+Poojacount)

    if int(Poojacount)>1:
        TotalAmountValue = float(AmountValue)*int(Poojacount)
        TotalAmountPooja = Label(BillingFrame, font=('calibri',8,'bold'), text="Total Amount", bd=16, anchor='w')
        TotalAmountPooja.configure(width=15,bg="white")
        TotalAmountPooja.grid(row=2,column=2,sticky="ew")
        TotalAmountPoojaValue = Label(BillingFrame, font=('calibri',8,'bold'), text=str(TotalAmountValue), bd=16, anchor='w')
        TotalAmountPoojaValue.configure(width=15,bg="white")
        TotalAmountPoojaValue.grid(row=2,column=3,sticky="ew")
    else:
        if int(Poojacount)==1:
  #          print("Pooja amount total"+ str(AmountValue))
            TotalAmountPooja = Label(BillingFrame, font=('calibri',8,'bold'), text="Total Amount", bd=16, anchor='w')
            TotalAmountPooja.configure(width=15,bg="white")
            TotalAmountPooja.grid(row=2,column=2,sticky="ew")
            TotalAmountPoojaValue = Label(BillingFrame, font=('calibri',8,'bold'), text=str(AmountValue), bd=16, anchor='w')
            TotalAmountPoojaValue.configure(width=15,bg="white")
            TotalAmountPoojaValue.grid(row=2,column=3,sticky="ew")

    file1.close()
    file2.close()
    file3.close()

    mycursor.close()
    mydb.close()


#..........................Selecting the pooja amount value for the Pooja..................
def ComboFunction1(event):
    print str(event)
    PoojaNameSelected = PoojaMenu1.get()

    print('Pooja selected is'+ str(PoojaNameSelected))

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="templeadmin",
    database="pkt_temple",
    auth_plugin='mysql_native_password'
    )
    mycursor = mydb.cursor()
#   a =  str(value)
#   PoojaNameSelected = a
#   print("Pooja selected in first function is "+PoojaNameSelected)
    SQL = "select POOJAAMOUNT from pkt_temple.POOJAINFORMATION where POOJANAME="+"'"+str(PoojaNameSelected)+"'"+";"
    mycursor.execute(SQL)
    a=[i[0] for i in mycursor.fetchall()]
    AmountValue = a[0]
    AmountMenu = Label(BillingFrame, font=('calibri',8,'bold'), text=AmountValue, bd=16, anchor='w')
    AmountMenu.configure(width=15,bg="white")
    AmountMenu.grid(row=2,column=1,sticky="ew")

    file1 = open("MyFile.txt","a")
    file2 = open("Poojaamount.txt","w")
    file3 = open("Poojacount.txt","r")

    file1.write("PoojaNameSelected:"+PoojaNameSelected+"&")
    file1.write("PoojaAmount:"+str(AmountValue)+"&")

    file2.write(str(AmountValue))
    Poojacount = file3.read()

    file1.close()
    file2.close()
    file3.close()


 #   print("Poojacount is"+Poojacount)
    if str(Poojacount)=="":
        Poojacount=str(1)
  #      print("Poojacount is"+Poojacount)

    if int(Poojacount)>1:
        TotalAmountValue = float(AmountValue)*int(Poojacount)
        TotalAmountPooja = Label(BillingFrame, font=('calibri',8,'bold'), text="Total Amount", bd=16, anchor='w')
        TotalAmountPooja.configure(width=15,bg="white")
        TotalAmountPooja.grid(row=2,column=2,sticky="ew")
        TotalAmountPoojaValue = Label(BillingFrame, font=('calibri',8,'bold'), text=str(TotalAmountValue), bd=16, anchor='w')
        TotalAmountPoojaValue.configure(width=15,bg="white")
        TotalAmountPoojaValue.grid(row=2,column=3,sticky="ew")
    else:
        if int(Poojacount)==1:
  #          print("Pooja amount total"+ str(AmountValue))
            TotalAmountPooja = Label(BillingFrame, font=('calibri',8,'bold'), text="Total Amount", bd=16, anchor='w')
            TotalAmountPooja.configure(width=15,bg="white")
            TotalAmountPooja.grid(row=2,column=2,sticky="ew")
            TotalAmountPoojaValue = Label(BillingFrame, font=('calibri',8,'bold'), text=str(AmountValue), bd=16, anchor='w')
            TotalAmountPoojaValue.configure(width=15,bg="white")
            TotalAmountPoojaValue.grid(row=2,column=3,sticky="ew")

    mycursor.close()
    mydb.close()




#    ...........Selecting the pooja amount value for the Pooja...........................................................

def RadioButtonSelect(value,optionvalue):
    file1 = open("Mode.txt","w")
    file1.write('1')
    file1.close

    print("inside radio function"+str(optionvalue))
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="templeadmin",
    database="pkt_temple",
    auth_plugin='mysql_native_password'
    )
    mycursor = mydb.cursor()
    a =  str(value)
    PoojaNameSelected = a
 #   print("Pooja selected in first function is "+PoojaNameSelected)
    SQL = "select POOJAAMOUNT from pkt_temple.POOJAINFORMATION where POOJANAME="+"'"+a+"'"+";"
    mycursor.execute(SQL)
    a=[i[0] for i in mycursor.fetchall()]
    AmountValue = a[0]

#    print("Pooja is "+PoojaNameSelected)

    PoojaMenu = Label(BillingFrame, font=('calibri',8,'bold'), text=PoojaNameSelected, bd=16, anchor='w')
    PoojaMenu.configure(width=15,bg="white")
    PoojaMenu.grid(row=1,column=1,sticky="ew")


    AmountMenu = Label(BillingFrame, font=('calibri',8,'bold'), text=AmountValue, bd=16, anchor='w')
    AmountMenu.configure(width=15,bg="white")
    AmountMenu.grid(row=2,column=1,sticky="ew")

    file1 = open("MyFile.txt","a")
    file2 = open("Poojaamount.txt","w")
    file3 = open("Poojacount.txt","r")

    file1.write("PoojaNameSelected:"+PoojaNameSelected+"&")
    file1.write("PoojaAmount:"+str(AmountValue)+"&")

    file2.write(str(AmountValue))

    Poojacount = file3.read()

#    print("Poojacount is"+Poojacount)

    if str(Poojacount)=="":
        Poojacount=str(1)
 #       print("Poojacount is"+Poojacount)

    if int(Poojacount)>1:
        TotalAmountValue = float(AmountValue)*int(Poojacount)
        TotalAmountPooja = Label(BillingFrame, font=('calibri',8,'bold'), text="Total Amount", bd=16, anchor='w')
        TotalAmountPooja.configure(width=15,bg="white")
        TotalAmountPooja.grid(row=2,column=2,sticky="ew")
        TotalAmountPoojaValue = Label(BillingFrame, font=('calibri',8,'bold'), text=str(TotalAmountValue), bd=16, anchor='w')
        TotalAmountPoojaValue.configure(width=15,bg="white")
        TotalAmountPoojaValue.grid(row=2,column=3,sticky="ew")
    else:
        if int(Poojacount)==1:
    #        print("Pooja amount total"+ str(AmountValue))
            TotalAmountPooja = Label(BillingFrame, font=('calibri',8,'bold'), text="Total Amount", bd=16, anchor='w')
            TotalAmountPooja.configure(width=15,bg="white")
            TotalAmountPooja.grid(row=2,column=2,sticky="ew")
            TotalAmountPoojaValue = Label(BillingFrame, font=('calibri',8,'bold'), text=str(AmountValue), bd=16, anchor='w')
            TotalAmountPoojaValue.configure(width=15,bg="white")
            TotalAmountPoojaValue.grid(row=2,column=3,sticky="ew")

    file1.close()
    file2.close()
    file3.close()

    mycursor.close()
    mydb.close()

def WriteToDBandPrint(PoojaNamevalue, PoojaCount, PoojaAmountvalue, PoojaTotalAmount, variableName1, variableName2, variableName3, variableName4, variableName5, PoojaNakshatram1value, PoojaNakshatram2value, PoojaNakshatram3value, PoojaNakshatram4value, PoojaNakshatram5value, variablePoojaDate, TodayDateValue, variablePhoneNo):

    file2 = open("MyFile.txt","w")
    file2.write("")
    file2.close()

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="templeadmin",
    database="pkt_temple",
    auth_plugin='mysql_native_password'
    )
    mycursor = mydb.cursor()

    SQL1 = "SELECT MAX(BOOKINGID) FROM pkt_temple.BOOKINGHISTORY;"

    mycursor.execute(SQL1)
    Maxvalue =  mycursor.fetchone()
#    Maxvalue = Maxvalue
 #   print Maxvalue[0]

    newmaxvalue = Maxvalue[0] + 1

    PrintPoojaOfferings(str(newmaxvalue),PoojaNamevalue, PoojaCount, PoojaAmountvalue, PoojaTotalAmount, variableName1, variableName2, variableName3, variableName4, variableName5, PoojaNakshatram1value, PoojaNakshatram2value, PoojaNakshatram3value, PoojaNakshatram4value, PoojaNakshatram5value, variablePoojaDate, TodayDateValue, variablePhoneNo)


#    print variablePoojaDate
#    SQLvalues = str(newmaxvalue)+","+"'"+PoojaNamevalue+"'"+","+str(PoojaAmountvalue)+","+"'"+variableName+"'"+","+"'"+PoojaNakshatram1value+"'"+","+"'"+variableName2+"'"+","+"'"+PoojaNakshatram2value+"'"+","+str(variableAge)+","+str(variablePhoneNo)+","+"'"+variablePoojaDate+"'"+","+"'PAID'"+")"

    SQLvalues = str(newmaxvalue)+","+"'"+PoojaNamevalue+"'"+","+str(PoojaAmountvalue)+","+str(PoojaCount)+","+str(PoojaTotalAmount)+","+"'"+variableName1+"'"+","+"'"+variableName2+"'"+","+"'"+variableName3+"'"+","+"'"+variableName4+"'"+","+"'"+variableName5+"'"+","+"'"+PoojaNakshatram1value+"'"+","+"'"+PoojaNakshatram2value+"'"+","+"'"+PoojaNakshatram3value+"'"+","+"'"+PoojaNakshatram4value+"'"+","+"'"+PoojaNakshatram5value+"'"+","+variablePhoneNo+","+"'"+TodayDateValue+"'"+","+"'"+str(variablePoojaDate)+"'"+")"
    print SQLvalues

#    SQL_Part1 = "insert into pkt_temple.BOOKINGHISTORY (BOOKINGID,POOJANAME,POOJAAMOUNT,POOJACOUNT,POOJATOTALAMOUNT,DEVOTEE1NAME,DEVOTEE2NAME,DEVOTEE3NAME,DEVOTEE4NAME,DEVOTEE5NAME,DEVOTEE1STAR,DEVOTEE2STAR,DEVOTEE3STAR,DEVOTEE4STAR,DEVOTEE5STAR,DEVOTEEPHONENO,BOOKEDDATE,POOJADATE)"

    SQL_Part1 = "insert into pkt_temple.BOOKINGHISTORY (BOOKINGID,POOJANAME,POOJAAMOUNT,POOJACOUNT,POOJATOTALAMOUNT,DEVOTEE1NAME,DEVOTEE2NAME,DEVOTEE3NAME,DEVOTEE4NAME,DEVOTEE5NAME,DEVOTEE1STAR,DEVOTEE2STAR,DEVOTEE3STAR,DEVOTEE4STAR,DEVOTEE5STAR,DEVOTEEPHONENO,BOOKEDDATE,POOJADATE)"
    SQL2 = SQL_Part1+"values ("+SQLvalues

#    print SQL2

    a = mycursor.execute(SQL2)

#    print a

    mydb.commit()

#   PrintPoojaOfferings(str(newmaxvalue),PoojaNamevalue,str(PoojaAmountvalue),str(variablePoojaDate),variableName,PoojaNakshatram1value,variableName2,PoojaNakshatram2value)


    mycursor.close()
    mydb.close()

def PrintOnly(PoojaNamevalue, PoojaCount, PoojaAmountvalue, PoojaTotalAmount, variableName1, variableName2, variableName3, variableName4, variableName5, PoojaNakshatram1value, PoojaNakshatram2value, PoojaNakshatram3value, PoojaNakshatram4value, PoojaNakshatram5value, variablePoojaDate, TodayDateValue, variablePhoneNo):

    PrintPoojaOfferings('COPY',PoojaNamevalue, PoojaCount, PoojaAmountvalue, PoojaTotalAmount, variableName1, variableName2, variableName3, variableName4, variableName5, PoojaNakshatram1value, PoojaNakshatram2value, PoojaNakshatram3value, PoojaNakshatram4value, PoojaNakshatram5value, variablePoojaDate, TodayDateValue, variablePhoneNo)


def WriteToDBOnly(PoojaNamevalue, PoojaCount, PoojaAmountvalue, PoojaTotalAmount, variableName1, variableName2, variableName3, variableName4, variableName5, PoojaNakshatram1value, PoojaNakshatram2value, PoojaNakshatram3value, PoojaNakshatram4value, PoojaNakshatram5value, variablePoojaDate, TodayDateValue, variablePhoneNo):

    file2 = open("MyFile.txt","w")
    file2.write("")
    file2.close()

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="templeadmin",
    database="pkt_temple",
    auth_plugin='mysql_native_password'
    )
    mycursor = mydb.cursor()

    SQL1 = "SELECT MAX(BOOKINGID) FROM pkt_temple.BOOKINGHISTORY;"

    mycursor.execute(SQL1)
    Maxvalue =  mycursor.fetchone()
#    Maxvalue = Maxvalue
#    print Maxvalue[0]

    newmaxvalue = Maxvalue[0] + 1
#    print variablePoojaDate
#    SQLvalues = str(newmaxvalue)+","+"'"+PoojaNamevalue+"'"+","+str(PoojaAmountvalue)+","+"'"+variableName+"'"+","+"'"+PoojaNakshatram1value+"'"+","+"'"+variableName2+"'"+","+"'"+PoojaNakshatram2value+"'"+","+str(variableAge)+","+str(variablePhoneNo)+","+"'"+variablePoojaDate+"'"+","+"'PAID'"+")"

    SQLvalues = str(newmaxvalue)+","+"'"+PoojaNamevalue+"'"+","+str(PoojaAmountvalue)+","+str(PoojaCount)+","+str(PoojaTotalAmount)+","+"'"+variableName1+"'"+","+"'"+variableName2+"'"+","+"'"+variableName3+"'"+","+"'"+variableName4+"'"+","+"'"+variableName5+"'"+","+"'"+PoojaNakshatram1value+"'"+","+"'"+PoojaNakshatram2value+"'"+","+"'"+PoojaNakshatram3value+"'"+","+"'"+PoojaNakshatram4value+"'"+","+"'"+PoojaNakshatram5value+"'"+","+variablePhoneNo+","+"'"+TodayDateValue+"'"+","+"'"+str(variablePoojaDate)+"'"+")"
#    print SQLvalues

#    SQL_Part1 = "insert into pkt_temple.BOOKINGHISTORY (BOOKINGID,POOJANAME,POOJAAMOUNT,POOJACOUNT,POOJATOTALAMOUNT,DEVOTEE1NAME,DEVOTEE2NAME,DEVOTEE3NAME,DEVOTEE4NAME,DEVOTEE5NAME,DEVOTEE1STAR,DEVOTEE2STAR,DEVOTEE3STAR,DEVOTEE4STAR,DEVOTEE5STAR,DEVOTEEPHONENO,BOOKEDDATE,POOJADATE)"

    SQL_Part1 = "insert into pkt_temple.BOOKINGHISTORY (BOOKINGID,POOJANAME,POOJAAMOUNT,POOJACOUNT,POOJATOTALAMOUNT,DEVOTEE1NAME,DEVOTEE2NAME,DEVOTEE3NAME,DEVOTEE4NAME,DEVOTEE5NAME,DEVOTEE1STAR,DEVOTEE2STAR,DEVOTEE3STAR,DEVOTEE4STAR,DEVOTEE5STAR,DEVOTEEPHONENO,BOOKEDDATE,POOJADATE)"
    SQL2 = SQL_Part1+"values ("+SQLvalues

#   print SQL2

    a = mycursor.execute(SQL2)

 #   print a

    mydb.commit()

#   PrintPoojaOfferings(str(newmaxvalue),PoojaNamevalue,str(PoojaAmountvalue),str(variablePoojaDate),variableName,PoojaNakshatram1value,variableName2,PoojaNakshatram2value)

    mycursor.close()
    mydb.close()


def BookPooja(Root,FrameName,OPTIONSPOOJANAME,LabelDateValue):


#   win = Root.Toplevel() 

    print('Date selected is:'+str(LabelDateValue.get_date()))
    win = Toplevel(Root)
    win.config(bg='red',padx=10,pady=10)
    win.wm_title("POOJA CONFIRMATION")


 #    label.pack(side="top", fill="x")
 # #   win.wm_title("Pooja confirmation")

 #    variablePooja  = OptionMenu(BillingFrame).getvar()
 #   variableAmount = OptionMenu(BillingFrame).getvar("20.00")
 #   variableNakshathram = OptionMenu(BillingFrame).getvar("Aswathi")

#   print("Pooja selected in second function is "+PoojaNameSelected)
#     variableAmount = "20.00"
#     variableNakshathram = "Aswathi"

    PoojaNamevalue="No"
    PoojaAmountvalue=0
    PoojaCount = 0
    PoojaTotalAmount = 0
    ErrorMessage=""

    PoojaName1 ="No"
    PoojaName2 ="No"
    PoojaName3 ="No"
    PoojaName4 ="No"
    PoojaName5 ="No"

    PoojaNakshatram1value="No"
    PoojaNakshatram2value="No"
    PoojaNakshatram3value="No"
    PoojaNakshatram4value="No"
    PoojaNakshatram5value="No"

    Dateflag=0

    file10 = open("Mode.txt","r")
    ModeValue=file10.read()
    file10.close

    if(int(ModeValue)==2):

        EntryFields = FrameName.GetChildren()

        PoojaNameSelected = PoojaEntry.get()
        AmountValue = PoojaAmountEntry.get()

    	file1 = open("MyFile.txt","a")
    	file1.write("PoojaNameSelected:"+PoojaNameSelected+"&")
    	file1.write("PoojaAmount:"+str(AmountValue)+"&")
        file1.close

    
    file1 = open("MyFile.txt","r")
    Fullstring =  file1.readline()

    file3 = open("Poojacount.txt","r")
    FullPoojacountstring =  file3.readline()
    if(FullPoojacountstring==''):
        FullPoojacountstring='1'


    SubString =  Fullstring.split('&')
    # # print(SubString)
    # # print len(SubString)
    #
    #SubStringPoojaCount =  FullPoojacountstring.split('&')
    # print(SubStringPoojaCount)
    # print len(SubStringPoojaCount)

    print("Pooja count is"+FullPoojacountstring)

    PoojaCount = int(FullPoojacountstring)

    file1 = open("Poojaamount.txt","r")
    PoojaAmountvalue = str(file1.read())
    file1.close()

    j=0
    for i in SubString:
        PoojaName = i.split("PoojaNameSelected:")
        if(len(PoojaName)== 2):
            PoojaNamevalue = PoojaName[1]

#        PoojaAmount = i.split("PoojaAmount:")
#        if(len(PoojaAmount)== 2):
#            PoojaAmountvalue = PoojaAmount[1]

        PoojaNakshatram1 = i.split("Nakshatram1:")
        if(len(PoojaNakshatram1)== 2):
            PoojaNakshatram1value = PoojaNakshatram1[1]

        PoojaNakshatram2 = i.split("Nakshatram2:")
        if(len(PoojaNakshatram2)== 2):
            PoojaNakshatram2value = PoojaNakshatram2[1]

        PoojaNakshatram3 = i.split("Nakshatram3:")
        if(len(PoojaNakshatram3)== 2):
            PoojaNakshatram3value = PoojaNakshatram3[1]

        PoojaNakshatram4 = i.split("Nakshatram4:")
        if(len(PoojaNakshatram4)== 2):
            PoojaNakshatram4value = PoojaNakshatram4[1]

        PoojaNakshatram5 = i.split("Nakshatram5:")
        if(len(PoojaNakshatram5)== 2):
            PoojaNakshatram5value = PoojaNakshatram5[1]

        j=j+1

   #     variablePoojaDate = str(date.today())

   #     DateFlagString = i.split("DatechangeFlag:")

   #     if(len(DateFlagString)== 2):
   #         Dateflag = DateFlagString[1]

   #     if Dateflag == str(0) or Dateflag == 0:
   #         variablePoojaDate = str(date.today())
   #         print("Date selected is within : "+variablePoojaDate)
   #     else:
   #          variablePoojaDate = DateBox.get()

    PoojaTotalAmount = PoojaCount*float(PoojaAmountvalue)

    variablePoojaDate = LabelDateValue.get_date()

#    print("Date flag is "+str(Dateflag))

#    print("Date selected outside condition : "+variablePoojaDate)

    #
    # for i in variablePoojaDate:
    #     Poojavalidations = i.split("-")
    #     print len(Poojavalidations)
    #
    #     if(len(Poojavalidations)!=3):
    #         if(len(Poojavalidations[0])==4 and isinstance(Poojavalidations[0], int) ):
    #             if(len(Poojavalidations[1])==2 and isinstance(Poojavalidations[1], int) ):
    #                 if(len(Poojavalidations[2])==2 and isinstance(Poojavalidations[2], int) ):
    #                     "print date entered is good"
    #                 else:
    #                      ErrorMessage = ErrorMessage +"Date entered is wrong"+'\n'
    #             else:
    #                 ErrorMessage = ErrorMessage +"Month entered is wrong"+'\n'
    #         else:
    #             ErrorMessage = ErrorMessage +"Year entered is wrong"+'\n'
    #     else:
    #         ErrorMessage = ErrorMessage +"Not a valid date"+'\n'


    #try:
    #    datetime.datetime.strptime(variablePoojaDate, '%Y-%m-%d')
    #except ValueError:
    #    ErrorMessage = ErrorMessage +"Not a valid date"+'\n'

    # print("Pooja name selected finally is "+PoojaNamevalue+'\n')
    # print("Pooja Amount finally is "+PoojaAmountvalue+'\n')
    #
    # print("Pooja PoojaNakshatram1 value finally is "+PoojaNakshatram1value+'\n')
    # print("Pooja PoojaNakshatram2 value finally is "+PoojaNakshatram2value+'\n')
    # print("Pooja PoojaNakshatram3 value finally is "+PoojaNakshatram3value+'\n')
    # print("Pooja PoojaNakshatram4 value finally is "+PoojaNakshatram4value+'\n')
    # print("Pooja PoojaNakshatram5 value finally is "+PoojaNakshatram5value+'\n')

    if (PoojaNamevalue=="No"):
        ErrorMessage=ErrorMessage+"Please select Pooja"
    else:
        print("Poojaname is " +PoojaNamevalue)

    #     print("PoojaName:"+ PoojaNamevalue+"\n")
    # if (PoojaNamevalue!=0):
    #     print("PoojaAmount:"+ str(PoojaAmountvalue)+"\n")
    # if (PoojaNakshatram1value!="No"):
    #     print("PoojaNakshatram1:"+ PoojaNakshatram1value+"\n")
    # if (PoojaNakshatram2value!="No"):
    #     print("PoojaNakshatram2:"+ PoojaNakshatram2value+"\n")

    file1.close()


#   os.remove("MyFile.txt")
#   variableName="2000"


    variableName1 = Entry(FrameName).getvar("Name1")
    variableName2 = Entry(FrameName).getvar("Name2")
    variableName3 = Entry(FrameName).getvar("Name3")
    variableName4 = Entry(FrameName).getvar("Name4")
    variableName5 = Entry(FrameName).getvar("Name5")
    variablePhoneNo = Entry(FrameName).getvar("Phone1")

    if(variableName1=="" or variableName1==" " or variableName1=="  "):
        variableName1="No"
    if(variableName2=="" or variableName1==" " or variableName1=="  "):
        variableName2="No"
    if(variableName3=="" or variableName1==" " or variableName1=="  "):
        variableName3="No"
    if(variableName4=="" or variableName1==" " or variableName1=="  "):
        variableName4="No"
    if(variableName5=="" or variableName1==" " or variableName1=="  "):
        variableName5="No"
    # variableAge = Entry(FrameName).getvar("Age1")
    # variableName2 = Entry(FrameName).getvar("Name2")


    allowed = set(string.lowercase +string.uppercase + ' ')

    if (set(variableName1) - allowed or len(variableName1)==0 or variableName1=="No"):
        # you know it has forbidden characters
        ErrorMessage =  ErrorMessage+"\n"+"Please enter valid devotee name 1"+"\n"
    else:
          if (PoojaNakshatram1value=="No"):
              ErrorMessage =  ErrorMessage+"\n"+"Please select Nakshatram  for devotee 1"+"\n"

    if(variableName2!="No"):
        if (set(variableName2) - allowed or len(variableName2)==0):
            # you know it has forbidden characters
            ErrorMessage =  ErrorMessage+ "Please enter valid name2"+"\n"
        else:
            if (PoojaNakshatram2value=="No"):
                  ErrorMessage =  ErrorMessage+"Please select Nakshatram  for devotee 2"+"\n"

    if(variableName3!="No"):
        if (set(variableName3) - allowed or len(variableName3)==0):
            # you know it has forbidden characters
            ErrorMessage =  ErrorMessage+ "Please enter valid name3"+"\n"
        else:
            if (PoojaNakshatram3value=="No"):
                  ErrorMessage =  ErrorMessage+"Please select Nakshatram  for devotee 3"+"\n"

    if(variableName4!="No"):
        if (set(variableName4) - allowed or len(variableName4)==0):
            # you know it has forbidden characters
            ErrorMessage =  ErrorMessage+ "Please enter valid name4"+"\n"
        else:
            if (PoojaNakshatram4value=="No"):
                  ErrorMessage =  ErrorMessage+"Please select Nakshatram  for devotee 4"+"\n"

    if(variableName5!="No"):
        if (set(variableName5) - allowed or len(variableName5)==0):
            # you know it has forbidden characters
            ErrorMessage =  ErrorMessage+ "Please enter valid name5"+"\n"
        else:
            if (PoojaNakshatram5value=="No"):
                  ErrorMessage =  ErrorMessage+"Please select Nakshatram  for devotee 5"+"\n"

    # it doesn't have forbidden characters

    # try:
    #
    # PoojaDate=DateBox.get()
    # variablePoojaDate = str(date.today())

    if(len(variablePhoneNo)>1):
        try:
            valuetocheck = int(variablePhoneNo)
        except ValueError:
            ErrorMessage =  ErrorMessage + "Please enter valid Phone Number"+"\n"

    else:
         variablePhoneNo='0'


#*******************************Print error if any input values are wrong*******************************

    print ErrorMessage

    if len(ErrorMessage) > 2:
        MessageToDisplay = "PLEASE FIX BELOW ERRORS\n\n"+ErrorMessage
        ErrorMessageBox = Label(win, font=('calibri',8,'bold'), text=MessageToDisplay, bd=5, anchor='w')
        ErrorMessageBox.configure(width=30,bg="white")
        ErrorMessageBox.grid(row=0)
        # CloseButton = Button(win,font=('calibri',8,'bold'), text="Close", justify=CENTER,)
        # CloseButton.configure(width=30,bg="white")
        # CloseButton.grid(row=1)
        ErrorMessageBox.mainloop()

    # print("Name is " + variableName)
    # print("Age is " + variableAge)
    # print("Phone is " + variablePhoneNo)

 #   variabledate = str(date.today())
 #   variablePoojaDate = Label(BillingFrame).getvar(variabledate)

 #   PoojaGrid = Label(win, font=('calibri',8,'bold'), text=variablePooja, bd=16, anchor='w')
 #   PoojaGrid.configure(width=30,bg="white")
 #   PoojaGrid.grid(row=0,column=0)

 #   PoojaAmount = Label(win, font=('calibri',8,'bold'), text=variableAmount, bd=16, anchor='w')
 #   PoojaAmount.configure(width=30,bg="white")
 #   PoojaAmount.grid(row=1,column=0)

 #   DevoteeNakshathram = Label(win, font=('calibri',8,'bold'), text=variableNakshathram, bd=16, anchor='w')
 #   DevoteeNakshathram.configure(width=30,bg="white")
 #   DevoteeNakshathram.grid(row=2,column=0)

    PoojaName = Label(win, font=('calibri',8,'bold'), text="Pooja Name", bd=16, anchor='w')
    PoojaName.configure(width=30,bg="white")
    PoojaName.grid(row=0,column=0)
    PoojaValue = Label(win, font=('calibri',8,'bold'), text=PoojaNamevalue, bd=16, anchor='w')
    PoojaValue.configure(width=30,bg="white")
    PoojaValue.grid(row=0,column=1)

    PoojaAmount = Label(win, font=('calibri',8,'bold'), text="Pooja Amount", bd=16, anchor='w')
    PoojaAmount.configure(width=30,bg="white")
    PoojaAmount.grid(row=0,column=2)
    PoojaAmountValue = Label(win, font=('calibri',8,'bold'), text=str(PoojaAmountvalue), bd=16, anchor='w')
    PoojaAmountValue.configure(width=30,bg="white")
    PoojaAmountValue.grid(row=0,column=3)

    PoojaAmount = Label(win, font=('calibri',8,'bold'), text="Pooja Count", bd=16, anchor='w')
    PoojaAmount.configure(width=30,bg="white")
    PoojaAmount.grid(row=1,column=0)
    PoojaAmountValue = Label(win, font=('calibri',8,'bold'), text=str(PoojaCount), bd=16, anchor='w')
    PoojaAmountValue.configure(width=30,bg="white")
    PoojaAmountValue.grid(row=1,column=1)

    PoojaAmount = Label(win, font=('calibri',8,'bold'), text="Pooja Total Amount", bd=16, anchor='w')
    PoojaAmount.configure(width=30,bg="white")
    PoojaAmount.grid(row=1,column=2)
    PoojaAmountValue = Label(win, font=('calibri',8,'bold'), text=str(PoojaTotalAmount), bd=16, anchor='w')
    PoojaAmountValue.configure(width=30,bg="white")
    PoojaAmountValue.grid(row=1,column=3)

    DevoteeName1 = Label(win, font=('calibri',8,'bold'), text="Devotee Name1", bd=16, anchor='w')
    DevoteeName1.configure(width=30,bg="white")
    DevoteeName1.grid(row=2,column=0)
    DevoteeName1 = Label(win, font=('calibri',8,'bold'), text=variableName1, bd=16, anchor='w')
    DevoteeName1.configure(width=30,bg="white")
    DevoteeName1.grid(row=2,column=1)

    DevoteeStar1 = Label(win, font=('calibri',8,'bold'), text="Devotee Nakshatram", bd=16, anchor='w')
    DevoteeStar1.configure(width=30,bg="white")
    DevoteeStar1.grid(row=2,column=2)
    DevoteeStar1Value = Label(win, font=('calibri',8,'bold'), text=PoojaNakshatram1value, bd=16, anchor='w')
    DevoteeStar1Value.configure(width=30,bg="white")
    DevoteeStar1Value.grid(row=2,column=3)

    x=3

    if len(variableName2)>3:
        DevoteeName2 = Label(win, font=('calibri',8,'bold'), text="Devotee Name2", bd=16, anchor='w')
        DevoteeName2.configure(width=30,bg="white")
        DevoteeName2.grid(row=x,column=0)
        DevoteeName2 = Label(win, font=('calibri',8,'bold'), text=variableName2, bd=16, anchor='w')
        DevoteeName2.configure(width=30,bg="white")
        DevoteeName2.grid(row=x,column=1)

        DevoteeStar2 = Label(win, font=('calibri',8,'bold'), text="Devotee Nakshatram", bd=16, anchor='w')
        DevoteeStar2.configure(width=30,bg="white")
        DevoteeStar2.grid(row=x,column=2)
        DevoteeStar2Value = Label(win, font=('calibri',8,'bold'), text=PoojaNakshatram2value, bd=16, anchor='w')
        DevoteeStar2Value.configure(width=30,bg="white")
        DevoteeStar2Value.grid(row=x,column=3)
        x=x+1

    else:
        variableName2="No"

    if len(variableName3)>3:
        DevoteeName2 = Label(win, font=('calibri',8,'bold'), text="Devotee Name3", bd=16, anchor='w')
        DevoteeName2.configure(width=30,bg="white")
        DevoteeName2.grid(row=x,column=0)
        DevoteeName2 = Label(win, font=('calibri',8,'bold'), text=variableName3, bd=16, anchor='w')
        DevoteeName2.configure(width=30,bg="white")
        DevoteeName2.grid(row=x,column=1)

        DevoteeStar2 = Label(win, font=('calibri',8,'bold'), text="Devotee Nakshatram", bd=16, anchor='w')
        DevoteeStar2.configure(width=30,bg="white")
        DevoteeStar2.grid(row=x,column=2)
        DevoteeStar2Value = Label(win, font=('calibri',8,'bold'), text=PoojaNakshatram3value, bd=16, anchor='w')
        DevoteeStar2Value.configure(width=30,bg="white")
        DevoteeStar2Value.grid(row=x,column=3)
        x=x+1

    else:
        variableName3="No"

    if len(variableName4)>3:
        DevoteeName2 = Label(win, font=('calibri',8,'bold'), text="Devotee Name4", bd=16, anchor='w')
        DevoteeName2.configure(width=30,bg="white")
        DevoteeName2.grid(row=x,column=0)
        DevoteeName2 = Label(win, font=('calibri',8,'bold'), text=variableName4, bd=16, anchor='w')
        DevoteeName2.configure(width=30,bg="white")
        DevoteeName2.grid(row=x,column=1)

        DevoteeStar2 = Label(win, font=('calibri',8,'bold'), text="Devotee Nakshatram", bd=16, anchor='w')
        DevoteeStar2.configure(width=30,bg="white")
        DevoteeStar2.grid(row=x,column=2)
        DevoteeStar2Value = Label(win, font=('calibri',8,'bold'), text=PoojaNakshatram4value, bd=16, anchor='w')
        DevoteeStar2Value.configure(width=30,bg="white")
        DevoteeStar2Value.grid(row=x,column=3)
        x=x+1

    else:
        variableName4="No"

    if len(variableName5)>3:
        DevoteeName2 = Label(win, font=('calibri',8,'bold'), text="Devotee Name5", bd=16, anchor='w')
        DevoteeName2.configure(width=30,bg="white")
        DevoteeName2.grid(row=x,column=0)
        DevoteeName2 = Label(win, font=('calibri',8,'bold'), text=variableName5, bd=16, anchor='w')
        DevoteeName2.configure(width=30,bg="white")
        DevoteeName2.grid(row=x,column=1)

        DevoteeStar2 = Label(win, font=('calibri',8,'bold'), text="Devotee Nakshatram", bd=16, anchor='w')
        DevoteeStar2.configure(width=30,bg="white")
        DevoteeStar2.grid(row=x,column=2)
        DevoteeStar2Value = Label(win, font=('calibri',8,'bold'), text=PoojaNakshatram5value, bd=16, anchor='w')
        DevoteeStar2Value.configure(width=30,bg="white")
        DevoteeStar2Value.grid(row=x,column=3)
        x=x+1

    else:
        variableName5="No"


    OfferDate = Label(win, font=('calibri',8,'bold'), text="Pooja Date ", bd=16, anchor='w')
    OfferDate.configure(width=30,bg="white")
    OfferDate.grid(row=x,column=0)
    PoojaDate = Label(win, font=('calibri',8,'bold'), text=variablePoojaDate, bd=16, anchor='w')
    PoojaDate.configure(width=30,bg="white")
    PoojaDate.grid(row=x,column=1)
    DevoteePhone = Label(win, font=('calibri',8,'bold'), text="Devotee Phone No", bd=16, anchor='w')
    DevoteePhone.configure(width=30,bg="white")
    DevoteePhone.grid(row=x,column=2)
    DevoteePhoneNo = Label(win, font=('calibri',8,'bold'), text=variablePhoneNo, bd=16, anchor='w')
    DevoteePhoneNo.configure(width=30,bg="white")
    DevoteePhoneNo.grid(row=x,column=3)
    x=x+1

#..........inserting blank spaces for styling............................................

    LabelBlankSpace1 = Label(win, font=('calibri',8,'bold'), text="", bd=16, anchor='w')
    LabelBlankSpace1.configure(bg="white")
    LabelBlankSpace1.configure(width=30,bg="white",fg="white")
    LabelBlankSpace1.grid(row=x, column=0)


    TodayDateValue = str(date.today())
    TodayDate = Label(win, font=('calibri',8,'bold'), text="Booked Date ", bd=16, anchor='w')
    TodayDate.configure(width=30,bg="white")
    TodayDate.grid(row=x,column=1)
    TodayDateDisplay = Label(win, font=('calibri',8,'bold'), text=TodayDateValue, bd=16, anchor='w')
    TodayDateDisplay.configure(width=30,bg="white")
    TodayDateDisplay.grid(row=x,column=2)


    # print("Pooja is "+PoojaNamevalue+'\n')
    # print("Pooja count is "+str(PoojaCount)+'\n')
    # print("Pooja Amount is "+str(PoojaAmountvalue)+'\n')
    # print("Pooja Total Amount is"+str(PoojaTotalAmount)+'\n')
    # print("Devotee1 Name is "+variableName1+'\n')
    # print("Devotee2 Name is"+variableName2+'\n')
    # print("Devotee3 Name is"+variableName3+'\n')
    # print("Devotee4 Name is"+variableName4+'\n')
    # print("Devotee5 Name is"+variableName5+'\n')
    # print("Devotee1 Birthstar is "+PoojaNakshatram1value+'\n')
    # print("Devotee2 Birthstar is "+PoojaNakshatram2value+'\n')
    # print("Devotee3 Birthstar is "+PoojaNakshatram3value+'\n')
    # print("Devotee4 Birthstar is "+PoojaNakshatram4value+'\n')
    # print("Devotee5 Birthstar is "+PoojaNakshatram5value+'\n')
    # print("Pooja date is"+variablePoojaDate+'\n')
    # print("Booked date is"+TodayDateValue+'\n')
    # print("Phone number"+variablePhoneNo+'\n')

#    print("Error message is" +ErrorMessage)


#..........inserting blank spaces for styling............................................

    LabelBlankSpace2 = Label(win, font=('calibri',8,'bold'), text="", bd=16, anchor='w')
    LabelBlankSpace2.configure(bg="white")
    LabelBlankSpace2.configure(width=30,bg="white",fg="white")
    LabelBlankSpace2.grid(row=x, column=3)


#..........Buttons on the confirmation page ............................................
#    BookPoojaButton = Button(win,font=('calibri',8,'bold'), text="BOOK & PRINT", bg="white",activebackground="red", command=lambda : WriteToDBandPrint(PoojaNamevalue,str(PoojaCount),str(PoojaAmountvalue),str(PoojaTotalAmount),variableName1,variableName2,variableName3,variableName4,variableName5,PoojaNakshatram1value,PoojaNakshatram2value,PoojaNakshatram3value,PoojaNakshatram4value,PoojaNakshatram5value,variablePoojaDate,TodayDateValue,variablePhoneNo), justify=CENTER)

    BookPoojaButton = Button(win,font=('calibri',8,'bold'), text="BOOK & PRINT", bg="white",activebackground="red", command=lambda : [WriteToDBandPrint(PoojaNamevalue,str(PoojaCount),str(PoojaAmountvalue),str(PoojaTotalAmount),variableName1,variableName2,variableName3,variableName4,variableName5,PoojaNakshatram1value,PoojaNakshatram2value,PoojaNakshatram3value,PoojaNakshatram4value,PoojaNakshatram5value,variablePoojaDate,TodayDateValue,variablePhoneNo), win.destroy()], justify=CENTER)
    BookPoojaButton.configure(width=30,bg="white")
    BookPoojaButton.grid(row=x+2, column=0)
#    BookPoojaButton.invoke(win.destroy())

    BookPoojaPrintButton = Button(win,font=('calibri',8,'bold'), text="BOOK Only", bg="white",activebackground="red", command=lambda : [WriteToDBOnly(PoojaNamevalue, PoojaCount, PoojaAmountvalue, PoojaTotalAmount, variableName1, variableName2, variableName3, variableName4, variableName5, PoojaNakshatram1value, PoojaNakshatram2value, PoojaNakshatram3value, PoojaNakshatram4value, PoojaNakshatram5value, variablePoojaDate, TodayDateValue, variablePhoneNo), win.destroy()], justify=CENTER)
    BookPoojaPrintButton.configure(width=30,bg="white")
    BookPoojaPrintButton.grid(row=x+2, column=1)

    PrintOnlyPoojaButton = Button(win,font=('calibri',8,'bold'), text="PRINT Only", bg="white",activebackground="red", command=lambda : [PrintOnly(PoojaNamevalue, PoojaCount, PoojaAmountvalue, PoojaTotalAmount, variableName1, variableName2, variableName3, variableName4, variableName5, PoojaNakshatram1value, PoojaNakshatram2value, PoojaNakshatram3value, PoojaNakshatram4value, PoojaNakshatram5value, variablePoojaDate, TodayDateValue, variablePhoneNo), win.destroy()], justify=CENTER)
    PrintOnlyPoojaButton.configure(width=30,bg="white")
    PrintOnlyPoojaButton.grid(row=x+2, column=2)

    # BookPoojaPrintButton = Button(win,font=('calibri',8,'bold'), text="BOOK Only", bg="white",activebackground="red", command=lambda : WriteToDBOnly(PoojaNamevalue,PoojaAmountvalue,variableName,PoojaNakshatram1value,variableName2,PoojaNakshatram2value,variableAge,variablePhoneNo,variablePoojaDate), justify=CENTER)
    # BookPoojaPrintButton.configure(width=30,bg="white")
    # BookPoojaPrintButton.grid(row=x, column=2)

    # win.destroy()
    win.mainloop()


# def func6(value):
#     file1 = open("MyFile.txt","a")
#     file1.write("Nakshatram4:"+value+"&")
#     file1.close()

#.........................All imports of the Python libraries and custome libraries.....................
import os
import mysql.connector



from datetime import date
import string
import decimal
import tkMessageBox as MessageBox
import random
import time
from Tkinter import *
import ttk
#from tkinter import ttk
from DatabaseFunctions import *
from PrintFunctions import *
from PrintFunctions import PrintPoojaOfferings
from GeneralFunctions import *


#................Global variables.........................................................................



#........................Home UI for the Application and window size definitions......................................
AppRoot = Tk()
AppRoot.geometry("1200x700+0+0")
AppRoot.title("Pookkattupadi Bhagavathi Temple")


#........................General variable declarations and lists.......................................................

OPTIONSNAKSHATHRA1 = [
    "Not known",
    "Aswathi",
    "Bharani",
    "Kartika",
    "Rohini",
    "Makayiram",
    "Thiruvathira",
    "Punartham",
    "Pooyam",
    "Aayilyam",
    "Makam",
    "Pooram",
    "Uthram",
    "Atham",
    "Chithira",
    "Chothi",
    "Vishagham",
    "Anizham",
    "Thrikketta",
    "Moolam",
    "Pooradam",
    "Uthradam",
    "Thiruvonam",
    "Avittam",
    "Chathayam",
    "Pooruruttathi",
    "Uthrattathi",
    "Revathi"
]

OPTIONSNAKSHATHRA2 = [
    "Not known",
    "Aswathi",
    "Bharani",
    "Kartika",
    "Rohini",
    "Makayiram",
    "Thiruvathira",
    "Punartham",
    "Pooyam",
    "Aayilyam",
    "Makam",
    "Pooram",
    "Uthram",
    "Atham",
    "Chithira",
    "Chothi",
    "Vishagham",
    "Anizham",
    "Thrikketta",
    "Moolam",
    "Pooradam",
    "Uthradam",
    "Thiruvonam",
    "Avittam",
    "Chathayam",
    "Pooruruttathi",
    "Uthrattathi",
    "Revathi"
]

OPTIONSNAKSHATHRA3 = [
    "Not known",
    "Aswathi",
    "Bharani",
    "Kartika",
    "Rohini",
    "Makayiram",
    "Thiruvathira",
    "Punartham",
    "Pooyam",
    "Aayilyam",
    "Makam",
    "Pooram",
    "Uthram",
    "Atham",
    "Chithira",
    "Chothi",
    "Vishagham",
    "Anizham",
    "Thrikketta",
    "Moolam",
    "Pooradam",
    "Uthradam",
    "Thiruvonam",
    "Avittam",
    "Chathayam",
    "Pooruruttathi",
    "Uthrattathi",
    "Revathi"
]

OPTIONSNAKSHATHRA4 = [
    "Not known",
    "Aswathi",
    "Bharani",
    "Kartika",
    "Rohini",
    "Makayiram",
    "Thiruvathira",
    "Punartham",
    "Pooyam",
    "Aayilyam",
    "Makam",
    "Pooram",
    "Uthram",
    "Atham",
    "Chithira",
    "Chothi",
    "Vishagham",
    "Anizham",
    "Thrikketta",
    "Moolam",
    "Pooradam",
    "Uthradam",
    "Thiruvonam",
    "Avittam",
    "Chathayam",
    "Pooruruttathi",
    "Uthrattathi",
    "Revathi"
]

OPTIONSNAKSHATHRA5 = [
    "Not known",
    "Aswathi",
    "Bharani",
    "Kartika",
    "Rohini",
    "Makayiram",
    "Thiruvathira",
    "Punartham",
    "Pooyam",
    "Aayilyam",
    "Makam",
    "Pooram",
    "Uthram",
    "Atham",
    "Chithira",
    "Chothi",
    "Vishagham",
    "Anizham",
    "Thrikketta",
    "Moolam",
    "Pooradam",
    "Uthradam",
    "Thiruvonam",
    "Avittam",
    "Chathayam",
    "Pooruruttathi",
    "Uthrattathi",
    "Revathi"
]

NOOFPOOJAMENU = [
    1,2,3,4,5
    ]

OPTIONSPUJAINFORMATION = GetPoojaInformation()

OPTIONSPUJAINFORMATION.sort()

OPTIONSPOOJANAME = [i[0] for i in OPTIONSPUJAINFORMATION]

OPTIONSPOOJANAME.remove('PUSHPANJALI')
OPTIONSPOOJANAME.remove('RAKTHA PUSHPANJALI')
OPTIONSPOOJANAME.remove('AIKAMATHYA PUSHPANJALI')
OPTIONSPOOJANAME.remove('VIDYASOOKTHA PUSHPANJALI')
OPTIONSPOOJANAME.remove('SHATHRUSAMHARA PUSHPANJALI')
OPTIONSPOOJANAME.remove('BHAGYASOOKTHA ARCHANA')
#OPTIONSPOOJANAME.remove('ENNA')SHREESOOKTHA ARCHANA
OPTIONSPOOJANAME.remove('SHREESOOKTHA ARCHANA')
OPTIONSPOOJANAME.remove('NEY VILAKKU')
OPTIONSPOOJANAME.remove('GURUTHI PUSHPANJALI')
OPTIONSPOOJANAME.remove('KARYA SIDDHI POOJA')
OPTIONSPOOJANAME.remove('PATTUM MANIYUM')
OPTIONSPOOJANAME.remove('PONKALA-FULL')
OPTIONSPOOJANAME.remove('PONKALA-POOJA')

OPTIONSAMOUNT = [i[1] for i in OPTIONSPUJAINFORMATION]


variable1 = StringVar(AppRoot)
variable1.set(OPTIONSPOOJANAME[0]) # default value

variable2 = StringVar(AppRoot)
variable2.set(OPTIONSNAKSHATHRA1[0]) # default value

variable3 = StringVar(AppRoot)
variable3.set(OPTIONSNAKSHATHRA2[0]) # default value

variable4 = StringVar(AppRoot)
variable4.set(OPTIONSNAKSHATHRA2[0]) # default value

variable5 = StringVar(AppRoot)
variable5.set(OPTIONSNAKSHATHRA2[0]) # default value

variable6 = StringVar(AppRoot)
variable6.set(OPTIONSNAKSHATHRA2[0]) # default value

variable7 = IntVar(AppRoot)
variable7.set(NOOFPOOJAMENU[0])

variable10 = StringVar(AppRoot)
#variable10.set(OPTIONSBOOKEDPOOJAS[0])

variabledate = StringVar(AppRoot)
variabledate = str(date.today())

#file1 = open("MyFile.txt","w")
file2 = open("Poojaamount.txt","w")
file3 = open("Poojacount.txt","w")

#file1.write("")
file2.write("")
file3.write("")


POOJANAMES = ["GANAPATI POOJA","VAHANA POOJA","NAAL POOJA","SHASTHA POOJA","DURGA POOJA","SHIVA POOJA","BHAIRAVA POOJA","VEERABHADRA POOJA"]

optionvalue = IntVar()
optionvalue.set(0)  # initialize
x1=0;

#..........................UI Frame definitions.....................................................................

TopFrame = Frame(AppRoot,height=25,width=1200,bg="blue",relief=FLAT)
TopFrame.pack(side=TOP)

MostRecentFrame = Frame(AppRoot,height=725,width=400,bg="white",bd=10, relief=SUNKEN)
MostRecentFrame.pack(side=LEFT)

BillingFrame = Frame(AppRoot,height=725,width=600,bg="white",bd=10, relief=SUNKEN)
BillingFrame.pack(side=LEFT)

# ReportFrame = Frame(AppRoot,height=550,width=300,bg="white",bd=10, relief=SUNKEN)
# ReportFrame.pack(side=LEFT)

# BottomFrame = Frame(AppRoot,height=150,width =1200,bg="gold",relief=SUNKEN)
# BottomFrame.pack(side=BOTTOM)

#..........................Title of the Temple ....................................................................



TempleTitle = Label(TopFrame,font=('calibri',20,'bold'),text="Pookkattupadi Bhagavathi Temple Billing System                                                                                                                                 ", fg="Red", bd=20,bg="white", anchor='w')
TempleTitle.grid(row=0, column=0)
TopFrame.config(bg='white')


#..........................All List option menu configurations .........................................................

Amount1 = 0;

PoojaMenu = ttk.Combobox(BillingFrame, values=OPTIONSPOOJANAME)
PoojaMenu.bind("<<ComboboxSelected>>", ComboFunction)
PoojaMenu.current(0)
#PoojaMenu.config(font=('calibri',8,'bold'))
#PoojaMenu.config(width=30)

NakshathramMenu1 = OptionMenu(BillingFrame, variable2, *OPTIONSNAKSHATHRA1, command=func1)
NakshathramMenu2 = OptionMenu(BillingFrame, variable3, *OPTIONSNAKSHATHRA2, command=func2)
NakshathramMenu3 = OptionMenu(BillingFrame, variable4, *OPTIONSNAKSHATHRA3, command=func3)
NakshathramMenu4 = OptionMenu(BillingFrame, variable5, *OPTIONSNAKSHATHRA4, command=func4)
NakshathramMenu5 = OptionMenu(BillingFrame, variable6, *OPTIONSNAKSHATHRA5, command=func5)
NoofPoojaMenu = OptionMenu(BillingFrame, variable7, *NOOFPOOJAMENU, command=func6)
DateBox = Entry(BillingFrame, font=('calibri',8,'bold'), text="Date", bd=16)
DateBox.delete(0,10)
DateBox.insert(0,"2019-mm-dd")
DateBox.configure(width=15,bg="white")

PoojaMenu.config(font=('calibri',8,'bold'))
PoojaMenu.config(width=30)
NakshathramMenu1.config(font=('calibri',8,'bold'),bg="white",takefocus=1)
NakshathramMenu1.config(width=15)
NakshathramMenu2.config(font=('calibri',8,'bold'),bg="white",takefocus=1)
NakshathramMenu2.config(width=15)
NakshathramMenu3.config(font=('calibri',8,'bold'),bg="white",takefocus=1)
NakshathramMenu3.config(width=15)
NakshathramMenu4.config(font=('calibri',8,'bold'),bg="white",takefocus=1)
NakshathramMenu4.config(width=15)
NakshathramMenu5.config(font=('calibri',8,'bold'),bg="white",takefocus=1)
NakshathramMenu5.config(width=15)
NoofPoojaMenu.config(font=('calibri',8,'bold'),bg="white",takefocus=1)
NoofPoojaMenu.config(width=15)

#************Frequent Poojas****************************

optionvalue = IntVar()
# checkVariable2 = IntVar()
# checkVariable3 = IntVar()
# checkVariable4 = IntVar()
# checkVariable5 = IntVar()
# checkVariable6 = IntVar()
# checkVariable7 = IntVar()
# checkVariable8 = IntVar()


LabelOffering = Label(MostRecentFrame, font=('calibri',10,'bold'), text="Most common offerings", fg="Red", bd=12, anchor='w')
LabelOffering.configure(width=30,bg="white")
LabelOffering.grid(row=0)

POOJANAMES = ["PUSHPANJALI","RAKTHA PUSHPANJALI","AIKAMATHYA PUSHPANJALI","VIDYASOOKTHA PUSHPANJALI","SHATHRUSAMHARA PUSHPANJALI","SWAYAMVARA PUSHPANJALI","BHAGYASOOKTHA ARCHANA","SHREESOOKTHA ARCHANA","NEY VILAKKU","GURUTHI PUSHPANJALI","KARYA SIDDHI POOJA","PATTUM MANIYUM","PONKALA-FULL","PONKALA-POOJA"]

C1 = Radiobutton(MostRecentFrame, text =POOJANAMES[0], value=POOJANAMES[0], var=optionvalue, padx=1, pady=1, font=('calibri',8,'bold'), bg='white', width=35, bd=2, height=2, justify=LEFT, command=lambda : RadioButtonSelect(POOJANAMES[0],optionvalue), relief=FLAT)
C2 = Radiobutton(MostRecentFrame, text =POOJANAMES[1], value=POOJANAMES[1], var=optionvalue, padx=1, pady=1, font=('calibri',8,'bold'), bg='white', width=35, bd=2, height=2, justify=LEFT, command=lambda : RadioButtonSelect(POOJANAMES[1],optionvalue), relief=FLAT)
C3 = Radiobutton(MostRecentFrame, text =POOJANAMES[2], value=POOJANAMES[2], var=optionvalue, padx=1, pady=1, font=('calibri',8,'bold'), bg='white', width=35, bd=2, height=2, justify=LEFT, command=lambda : RadioButtonSelect(POOJANAMES[2],optionvalue), relief=FLAT)
C4 = Radiobutton(MostRecentFrame, text =POOJANAMES[3], value=POOJANAMES[3], var=optionvalue, padx=1, pady=1, font=('calibri',8,'bold'), bg='white', width=35, bd=2, height=2, justify=LEFT, command=lambda : RadioButtonSelect(POOJANAMES[3],optionvalue), relief=FLAT)
C5 = Radiobutton(MostRecentFrame, text =POOJANAMES[4], value=POOJANAMES[4], var=optionvalue, padx=1, pady=1, font=('calibri',8,'bold'), bg='white', width=35, bd=2, height=2, justify=LEFT, command=lambda : RadioButtonSelect(POOJANAMES[4],optionvalue), relief=FLAT)
C6 = Radiobutton(MostRecentFrame, text =POOJANAMES[5], value=POOJANAMES[5], var=optionvalue, padx=1, pady=1, font=('calibri',8,'bold'), bg='white', width=35, bd=2, height=2, justify=LEFT, command=lambda : RadioButtonSelect(POOJANAMES[5],optionvalue), relief=FLAT)
C7 = Radiobutton(MostRecentFrame, text =POOJANAMES[6], value=POOJANAMES[6], var=optionvalue, padx=1, pady=1, font=('calibri',8,'bold'), bg='white', width=35, bd=2, height=2, justify=LEFT, command=lambda : RadioButtonSelect(POOJANAMES[6],optionvalue), relief=FLAT)
C8 = Radiobutton(MostRecentFrame, text =POOJANAMES[7], value=POOJANAMES[7], var=optionvalue, padx=1, pady=1, font=('calibri',8,'bold'), bg='white', width=35, bd=2, height=2, justify=LEFT, command=lambda : RadioButtonSelect(POOJANAMES[7],optionvalue), relief=FLAT)
C9 = Radiobutton(MostRecentFrame, text =POOJANAMES[8], value=POOJANAMES[8], var=optionvalue, padx=1, pady=1, font=('calibri',8,'bold'), bg='white', width=35, bd=2, height=2, justify=LEFT, command=lambda : RadioButtonSelect(POOJANAMES[8],optionvalue), relief=FLAT)
C10 = Radiobutton(MostRecentFrame, text =POOJANAMES[9], value=POOJANAMES[9], var=optionvalue, padx=1, pady=1, font=('calibri',8,'bold'), bg='white', width=35, bd=2, height=2, justify=LEFT, command=lambda : RadioButtonSelect(POOJANAMES[9],optionvalue), relief=FLAT)
C11 = Radiobutton(MostRecentFrame, text =POOJANAMES[10], value=POOJANAMES[10], var=optionvalue, padx=1, pady=1, font=('calibri',8,'bold'), bg='white', width=35, bd=2, height=2, justify=LEFT, command=lambda : RadioButtonSelect(POOJANAMES[10],optionvalue), relief=FLAT)
C12 = Radiobutton(MostRecentFrame, text =POOJANAMES[11], value=POOJANAMES[11], var=optionvalue, padx=1, pady=1, font=('calibri',8,'bold'), bg='white', width=35, bd=2, height=2, justify=LEFT, command=lambda : RadioButtonSelect(POOJANAMES[11],optionvalue), relief=FLAT)
C13 = Radiobutton(MostRecentFrame, text =POOJANAMES[12], value=POOJANAMES[12], var=optionvalue, padx=1, pady=1, font=('calibri',8,'bold'), bg='white', width=35, bd=2, height=2, justify=LEFT, command=lambda : RadioButtonSelect(POOJANAMES[12],optionvalue), relief=FLAT)
C14 = Radiobutton(MostRecentFrame, text =POOJANAMES[13], value=POOJANAMES[13], var=optionvalue, padx=1, pady=1, font=('calibri',8,'bold'), bg='white', width=35, bd=2, height=2, justify=LEFT, command=lambda : RadioButtonSelect(POOJANAMES[13],optionvalue), relief=FLAT)

C1.grid(row=1)
C2.grid(row=2)
C3.grid(row=3)
C4.grid(row=4)
C5.grid(row=5)
C6.grid(row=6)
C7.grid(row=7)
C8.grid(row=8)
C9.grid(row=9)
C10.grid(row=10)
C11.grid(row=11)
C12.grid(row=12)
C13.grid(row=13)
C14.grid(row=14)

# LabelBlankSpace4 = Label(MostRecentFrame, font=('calibri',8,'bold'), text="", bd=16, anchor='w')
# LabelBlankSpace4.configure(bg="white")
# LabelBlankSpace4.configure(width=25,bg="white",fg="white")
# LabelBlankSpace4.grid(row=8, column=0)
#
# LabelBlankSpace4 = Label(MostRecentFrame, font=('calibri',8,'bold'), text="", bd=16, anchor='w')
# LabelBlankSpace4.configure(bg="white")
# LabelBlankSpace4.configure(width=25,bg="white",fg="white")
# LabelBlankSpace4.grid(row=9, column=0)

#LabelBlankSpace4 = Label(MostRecentFrame, font=('calibri',8,'bold'), text="", bd=16, anchor='w')
#LabelBlankSpace4.configure(bg="white")
#LabelBlankSpace4.configure(width=15,bg="white",fg="white")
#LabelBlankSpace4.grid(row=13, column=0)


#ResetButton = Button(BillingFrame, font=('calibri',8,'bold'), text="RESET", bg="white",activebackground="red", justify=CENTER)
ChangePoojaButton = Button(MostRecentFrame, font=('calibri',8,'bold'), text="Change to List", activebackground="white", padx=2, pady=2, bg='red', bd=3, fg='white', justify=CENTER, command= lambda : ChangeToList())
ChangePoojaButton.configure(width=15)
ChangePoojaButton.grid(row=15)

#ChangePoojaButton = Button(MostRecentFrame, font=('calibri',8,'bold'), text="Manual Entry", activebackground="white", padx=2, pady=2, bg='red', #bd=3, fg='white', justify=CENTER, command= lambda : ManualEntry())
#ChangePoojaButton.configure(width=15)
#ChangePoojaButton.grid(row=16)

LabelBlankSpace4 = Label(MostRecentFrame, font=('calibri',8,'bold'), text="", bd=16, anchor='w')
LabelBlankSpace4.configure(bg="white")
LabelBlankSpace4.configure(width=15,bg="white",fg="white")
LabelBlankSpace4.grid(row=17)
#
# LabelBlankSpace4 = Label(MostRecentFrame, font=('calibri',8,'bold'), text="", bd=16, anchor='w')
# LabelBlankSpace4.configure(bg="white")
# LabelBlankSpace4.configure(width=25,bg="white",fg="white")
# LabelBlankSpace4.grid(row=12, column=0)

# C3 = Radiobutton(MostRecentFrame, text = "NAAL POOJA", var=optionvalue, font=('courier', 15, 'bold'), bd=5, bg='white', width=25, height=1, justify=LEFT, relief=FLAT)
# MostRecentFrame.configure(width=15,bg="white")
# C3.grid(row=3,column=0)
#
# C4 = Radiobutton(MostRecentFrame, text = "SHASTHA POOJA", var=optionvalue, font=('courier', 15, 'bold'), bd=5, bg='white', width=25, height=1, justify=LEFT, relief=FLAT)
# MostRecentFrame.configure(width=15,bg="white")
# C4.grid(row=4,column=0)
#
# C5 = Radiobutton(MostRecentFrame, text = "DURGA POOJA", variable=optionvalue, font=('courier', 15, 'bold'), bd=5, bg='white', width=25, height=1,  justify=LEFT, relief=FLAT)
# MostRecentFrame.configure(width=15,bg="white")
# C5.grid(row=5,column=0)
#
# C6 = Radiobutton(MostRecentFrame, text = "SHIVA POOJA", variable=optionvalue, font=('courier', 15, 'bold'), bd=5, bg='white', width=25, height=1, justify=LEFT, relief=FLAT)
# MostRecentFrame.configure(width=15,bg="white")
# C6.grid(row=6,column=0)
#
# C7 = Radiobutton(MostRecentFrame, text = "BHAIRAVA POOJA", variable=optionvalue, font=('courier', 15, 'bold'), bd=5, bg='white', width=25, height=1, justify=LEFT, relief=FLAT)
# MostRecentFrame.configure(width=15,bg="white")
# C7.grid(row=7,column=0)
#
# C8 = Radiobutton(MostRecentFrame, text = "VEERABHADRA POOJA", variable=optionvalue, font=('courier', 15, 'bold'),bd=5, bg='white', width=25, height=1, justify=LEFT, relief=FLAT)
# MostRecentFrame.configure(width=15,bg="white")
# C8.grid(row=7,column=0)


# for pooja in POOJANAMES:
#     RadioButtonPooja = Radiobutton(MostRecentFrame, text=pooja, value=pooja, variable=optionvalue, font=('courier', 15, 'bold'),bd=5, bg='white', width=25, height=1, justify=LEFT, command=lambda : RadioButtonSelect(pooja,optionvalue), relief=FLAT)
#     RadioButtonPooja.grid(row=x1,column=0)
#     x1=x1+1


# LabelBlankSpace4 = Label(MostRecentFrame, font=('calibri',8,'bold'), text="Please print receipt", bd=16, anchor='w')
# #LabelDateValue.configure(bg="white")
# LabelBlankSpace4.configure(width=25,height=10,bg="white",fg="white")
# LabelBlankSpace4.grid(row=8, column=0)

# LabelBlankSpace4 = Label(MostRecentFrame, font=('calibri',8,'bold'), text="Please print receipt", bd=16, anchor='w')
# #LabelDateValue.configure(bg="white")
# LabelBlankSpace4.configure(width=25,height=5,bg="white",fg="white")
# LabelBlankSpace4.grid(row=9, column=0)


#...........Heading of the Booking page..............
# LabelOffering = Label(BillingFrame, font=('calibri',14,'bold'), text="Offer your prayers to Amma!", fg="Red", bd=12, anchor='w')
# LabelOffering.configure(width=25,bg="white")
# LabelOffering.grid(row=0,column=0)

#...........Pooja selection..............
LabelOffering = Label(BillingFrame, font=('calibri',8,'bold'), text="Name of the offering", bd=16, anchor='w')
LabelOffering.configure(width=15,bg="white")
LabelOffering.grid(row=1,column=0)

StringPooja = str(OPTIONSPOOJANAME[0])
PoojaMenu.setvar(StringPooja)
PoojaMenu.grid(row=1,column=1,sticky="ew")

#...........No:of poojas selection ..............
#LabelAmount = Label(BillingFrame, font=('calibri',8,'bold'), text="No:of offerings", bd=16, anchor='w')
#LabelAmount.configure(width=15,bg="white")
#LabelAmount.grid(row=1,column=2)
#NoofPoojaMenu.setvar(str(OPTIONSPOOJANAME[0]))
#NoofPoojaMenu.grid(row=1,column=3,sticky="ew")

LabelPhone = Label(BillingFrame, font=('calibri',8,'bold'), text="Phone:", bd=16, anchor='w')
LabelPhone.configure(width=15,bg="white")
LabelPhone.grid(row=1,column=2)
EntryPhone1 = Entry(BillingFrame, font=('calibri',8,'bold'), text="Phone1", bd=16)
EntryPhone1.grid(row=1,column=3,sticky="ew")


#...........Amount display..............
LabelAmount = Label(BillingFrame, font=('calibri',8,'bold'), text="Amount", bd=16, anchor='w')
LabelAmount.configure(width=15,bg="white")
LabelAmount.grid(row=2,column=0)

#...........Amount display..............
LabelTotalAmount = Label(BillingFrame, font=('calibri',8,'bold'), text="Total Amount", bd=16, anchor='w')
LabelTotalAmount.configure(width=15,bg="white")
LabelTotalAmount.grid(row=2,column=2)

#...........Devotee details 1 ..............
LabelName = Label(BillingFrame, font=('calibri',8,'bold'), text="Devotee Name1", bd=16, anchor='w')
LabelName.configure(width=15,bg="white")
LabelName.grid(row=3,column=0)
EntryName1 = Entry(BillingFrame, font=('calibri',8,'bold'), text="Name1", bd=16)
EntryName1.grid(row=3,column=1,sticky="ew")

#...........Nakshathram display..............
LabelNakshathram1 = Label(BillingFrame, font=('calibri',8,'bold'), text="Janma Nakshathram", bd=16, anchor='w')
LabelNakshathram1.configure(width=15,bg="white")
LabelNakshathram1.grid(row=3,column=2,sticky="ew")
NakshathramMenu1.grid(row=3,column=3,sticky="ew")

#...........Devotee details 2..............
LabelName = Label(BillingFrame, font=('calibri',8,'bold'), text="Devotee Name2", bd=16, anchor='w')
LabelName.configure(width=15,bg="white")
LabelName.grid(row=4,column=0)
EntryName2 = Entry(BillingFrame, font=('calibri',8,'bold'), text="Name2", bd=16)
EntryName2.grid(row=4,column=1,sticky="ew")

#...........Nakshathram display..............
LabelNakshathram2 = Label(BillingFrame, font=('calibri',8,'bold'), text="Janma Nakshathram", bd=16, anchor='w')
LabelNakshathram2.configure(width=15,bg="white")
LabelNakshathram2.grid(row=4,column=2,sticky="ew")
NakshathramMenu2.grid(row=4,column=3,sticky="ew")

#...........Devotee details 3..............
LabelName = Label(BillingFrame, font=('calibri',8,'bold'), text="Devotee Name3", bd=16, anchor='w')
LabelName.configure(width=15,bg="white")
LabelName.grid(row=5,column=0)
EntryName3 = Entry(BillingFrame, font=('calibri',8,'bold'), text="Name3", bd=16)
EntryName3.grid(row=5,column=1,sticky="ew")

#...........Nakshathram display..............
LabelNakshathram3 = Label(BillingFrame, font=('calibri',8,'bold'), text="Janma Nakshathram", bd=16, anchor='w')
LabelNakshathram3.configure(width=15,bg="white")
LabelNakshathram3.grid(row=5,column=2,sticky="ew")
NakshathramMenu3.grid(row=5,column=3,sticky="ew")

#...........Devotee details 4..............
LabelName = Label(BillingFrame, font=('calibri',8,'bold'), text="Devotee Name4", bd=16, anchor='w')
LabelName.configure(width=15,bg="white")
LabelName.grid(row=6,column=0)
EntryName4 = Entry(BillingFrame, font=('calibri',8,'bold'), text="Name4", bd=16)
EntryName4.grid(row=6,column=1,sticky="ew")

#...........Nakshathram display..............
LabelNakshathram4 = Label(BillingFrame, font=('calibri',8,'bold'), text="Janma Nakshathram", bd=16, anchor='w')
LabelNakshathram4.configure(width=15,bg="white")
LabelNakshathram4.grid(row=6,column=2,sticky="ew")
NakshathramMenu4.grid(row=6,column=3,sticky="ew")

#...........Devotee details 5..............
LabelName = Label(BillingFrame, font=('calibri',8,'bold'), text="Devotee Name5", bd=16, anchor='w')
LabelName.configure(width=15,bg="white")
LabelName.grid(row=7,column=0)
EntryName5 = Entry(BillingFrame, font=('calibri',8,'bold'), text="Name5", bd=16)
EntryName5.grid(row=7,column=1,sticky="ew")

#...........Nakshathram display..............
LabelNakshathram5 = Label(BillingFrame, font=('calibri',8,'bold'), text="Janma Nakshathram", bd=16, anchor='w')
LabelNakshathram5.configure(width=15,bg="white")
LabelNakshathram5.grid(row=7,column=2,sticky="ew")
NakshathramMenu5.grid(row=7,column=3,sticky="ew")

#...........Date display......................
LabelDate = Label(BillingFrame, font=('calibri',8,'bold'), text="Date of offering", bd=16, anchor='w')
LabelDate.configure(width=15,bg="white")
LabelDate.grid(row=9,column=0)
#LabelDateValue = Label(BillingFrame, font=('calibri',8,'bold'), text=variabledate, bd=16, anchor='w')
#LabelDateValue.configure(width=15,bg="white")
#LabelDateValue.grid(row=9,column=1)

LabelDateValue = DateEntry(BillingFrame, width=12, font=('calibri',8,'bold'), background='darkblue', foreground='white', borderwidth=2)
LabelDateValue.grid(row=9,column=1)


#ChangeDateButton = Button(BillingFrame, font=('calibri',8,'bold'), text="Change date", activebackground="white", padx=2, pady=2, bg='red', bd=3, fg='white', justify=CENTER, command= lambda : ChangeOfferingDate(BillingFrame))
#ChangeDateButton.configure(width=15)
#ChangeDateButton.grid(row=9,column=2,sticky="ew")

#...........Phone number display......................
#LabelPhone = Label(BillingFrame, font=('calibri',8,'bold'), text="Phone no of devotee", bd=16, anchor='w')
#LabelPhone.configure(width=15,bg="white")
#LabelPhone.grid(row=10,column=0)
#EntryPhone1 = Entry(BillingFrame, font=('calibri',8,'bold'), text="Phone1", bd=16)
#EntryPhone1.grid(row=10,column=1,sticky="ew")

#...........No:of pooja display......................
LabelNumber = Label(BillingFrame, font=('calibri',8,'bold'), text="No:of offerings", bd=16, anchor='w')
LabelNumber.configure(width=15,bg="white")
LabelNumber.grid(row=10,column=0)
DefaultCount = str(NOOFPOOJAMENU[4])
NoofPoojaMenu.setvar(DefaultCount)
NoofPoojaMenu.grid(row=10,column=1,sticky="ew")


#...........AddPooja button ................................................................................................
AddPoojaListButton = Button(BillingFrame, font=('calibri',8,'bold'), text="ADD POOJA", activebackground="white", padx=2, pady=2, bg='red', bd=3, fg='white', justify=CENTER, command = lambda : AddPoojaList(AppRoot))
#BookButton.configure(width=15)
AddPoojaListButton.grid(row=10,column=3,sticky="ew")

#...........Booking button ................................................................................................
BookButton = Button(BillingFrame, font=('calibri',8,'bold'), text="BOOK", activebackground="white", padx=2, pady=2, bg='red', bd=3, fg='white', justify=CENTER, command = lambda : BookPooja(AppRoot,BillingFrame,OPTIONSPOOJANAME,LabelDateValue))
#BookButton.configure(width=15)
BookButton.grid(row=12,column=0,sticky="ew")

#...........Reset button ................................................................................................
ResetButton = Button(BillingFrame, font=('calibri',8,'bold'), text="RESET", activebackground="white", padx=2, pady=2, bg='red', bd=3, fg='white', command=lambda : ResetBilling(), justify=CENTER)
#ResetButton.configure(height=5,width=5)
ResetButton.grid(row=12,column=1,sticky="ew")

#...........Add Pooja ................................................................................................
DeleteButton = Button(BillingFrame, font=('calibri',8,'bold'), text="DELETE", activebackground="white", padx=2, pady=2, bg='red', bd=3, fg='white', command=lambda : DeleteBilling(), justify=CENTER)
#AddButton.configure(height=5,width=5)
DeleteButton.grid(row=12,column=2,sticky="ew")

#...........Add Pooja ................................................................................................
ViewButton = Button(BillingFrame, font=('calibri',8,'bold'), text="VIEW", activebackground="white", padx=2, pady=2, bg='red', bd=3, fg='white', command=lambda : ViewPooja(AppRoot), justify=CENTER)
#AddButton.configure(height=5,width=5)
ViewButton.grid(row=12,column=3,sticky="ew")

LabelBlankSpace4 = Label(BillingFrame, font=('calibri',8,'bold'), text="", bd=16, anchor='w')
LabelBlankSpace4.configure(bg="white")
LabelBlankSpace4.configure(width=25,bg="white",fg="white")
LabelBlankSpace4.grid(row=13, column=0)

LabelBlankSpace4 = Label(BillingFrame, font=('calibri',8,'bold'), text="", bd=16, anchor='w')
LabelBlankSpace4.configure(bg="white")
LabelBlankSpace4.configure(width=25,bg="white",fg="white")
LabelBlankSpace4.grid(row=14, column=0)

AppRoot.mainloop()


