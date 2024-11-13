inventory={}
def add():
    check=True
    count=1
    while(check):
        print(f"Enter item {count}:")
        count+=1
        item=input(f"Enter item to be added or type exit or e to return to the MENU:")
        if(item=="e" or item=="exit"):
            break
        amt=int(input("Enter amount in numbers(in kg,dozens etc.):"))
        if item in inventory:
            inventory[item]+=amt
        else:
            inventory[item]=amt
def remove():
    if(len(inventory)==0):
        print("Inventory Empty")
        return
    print("Inventory:")
    for i,j in inventory.items():
        print("item :",i,"\tAmount :",j)
    item=input()
    if item in inventory:
        amt=int(input("Amount to be taken:"))
        if(inventory[item]>=amt):
            inventory[item]-=amt
        else:
            print("Amount Exceeds availability")
    else:
        print("Item not in inventory")
def alerts():
    count=1
    for i,j in inventory.items():
        print(f"item {count} :",i,"\tAmount",j)
        count+=1
    for i,j in inventory.items():
        if(j==0):
            print("Low Inventory for",i)
check=True
while(check):
    print("1. Add Item")
    print("2. Remove Item")
    print("3. Check Inventory")
    val=int(input("Enter Choice:"))
    if(val==1):
        print("---------------------------------------------------------------------")
        add()
        print("---------------------------------------------------------------------")
    elif(val==2):
        print("---------------------------------------------------------------------")
        remove()
        print("---------------------------------------------------------------------")
    elif(val==3):
        print("---------------------------------------------------------------------")
        alerts()
        print("---------------------------------------------------------------------")
    else:
        break
