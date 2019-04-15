from tkinter import *
import pandas as pd
import re
import datetime
    
class Room:
    def __init__(self):
        self.roomData = None
        return
    def setRoom(self, event):
        self.roomData = str(suggestRooms_list.get(suggestRooms_list.curselection()))
        return
    def altRooms(self):
        tempRoom = roomID_input.get().upper()
        allMatches = []
        if tempRoom in roomList:
            self.roomData = roomID_input.get().upper()
            suggestRooms_list.delete(0, END)
            suggestRooms_list.insert(END,tempRoom)
        else:
            suggestRooms_list.delete(0, END)
            for i in range(len(roomList)):
                check_room = re.search(tempRoom, roomList[i])
                if check_room is not None:
                    allMatches.append(roomList[i])
            for j in range(len(allMatches)):
                suggestRooms_list.insert(j, allMatches[j])
        return
    def showRoomSch(self, event):
        self.clearBox()
        weekDays = ['Monday', 'Tuesday', 'Wednesday','Thursday','Friday','Saturday','Sunday']
        for days in weekDays:
            userRoom = roomSchedule[self.roomData][days]
            scheduleRooms_list.insert(0, days, str(userRoom))
        return
    def clearBox(self):
        scheduleRooms_list.delete(0,END)
        return
    def setDate(self):
        userMonth = str(dateStart_month.get())
        userDay = str(dateStart_day.get())
        userYear = str(dateStart_year.get())
        convertDate = str(userMonth + "/" + userDay + "/" + userYear)
        startDate = datetime.datetime.strptime(convertDate, "%m/%d/%Y")
        return startDate
    def setTime(self):
        # Allows the user to schedule a meeting with in a room through input
        weekDay = self.setDate().strftime('%A')
        startHours = int(timeStart_hours.get())
        startMinutes = timeStart_minutes.get()
        if (timeStart_PM.get() == "1"):
            startHours = startHours + 12
        endHours = int(timeEnd_hours.get())
        endMinutes = timeEnd_minutes.get()
        if (timeEnd_PM.get() == "1"):
            endHours = endHours + 12
        if (startHours > endHours):
            timeStart_hours.delete(0, END)
            timeStart_minutes.delete(0, END)
            timeEnd_hours.delete(0, END)
            timeEnd_minutes.delete(0, END)
            timeStart_hours.insert(0, "*Invalid input")
            timeStart_minutes.insert(0, "*Invalid input")
            timeEnd_hours.insert(0, "*Invalid input")
            timeEnd_minutes.insert(0, "*Invalid input")
            return
        else :
            convertStart = str(str(startHours) + ":" + str(startMinutes))
            convertEnd =  str(str(endHours) + ":" + str(endMinutes))
            startTime = datetime.datetime.strptime(convertStart, "%H:%M").time()
            endTime = datetime.datetime.strptime(convertEnd, "%H:%M").time()
            roomSchedule[self.roomData][weekDay].append(str(str(startTime) + " " + str(endTime)))
            userRoom = roomSchedule[self.roomData][weekDay]
            self.showRoomSch(self)
            return
            
# Import data from excel
# -----------------------------------------------------------------------------------------
roomData = pd.read_csv('RoomList.csv')
meetingTimes = pd.read_csv('MeetingTimes.csv')
print(meetingTimes)
campusList = list(dict.fromkeys(roomData['Campus'])) # List of campuses in UCC
roomList = list(dict.fromkeys(roomData['Room'])) # List of rooms in UCC
roomCampus = dict(zip(campusList, (roomList for i in range(len(campusList)))))
roomSchedule = dict(zip(roomList,({'Monday':[], 'Tuesday':[], 'Wednesday':[],'Thursday':[],'Friday':[],'Saturday':[],'Sunday':[]} for i in range(len(roomList))))) # Creates empty rooms to store a schedule
# -----------------------------------------------------------------------------------------

window = Tk()
room = Room()

# Search for a room Frame
# -----------------------------------------------------------------------------------------
# Frame set up
searchRoom_frame = LabelFrame(window, text="Search Room", relief=RIDGE)
searchRoom_frame.grid(row=0, column=0, sticky=E + W + N + S)
# Search engine
room_ID = Label(searchRoom_frame, text = "Room")
room_ID .grid(row=1,column=0)
roomID_input = Entry(searchRoom_frame, width = 35)
roomID_input.grid(row = 1, column = 1)
# Shows suggestions to the user when looking for a room
suggestRooms_list = Listbox(searchRoom_frame, height = 6, width = 35, selectmode = SINGLE)
suggestRooms_list.grid(row = 2, column = 1, rowspan = 6)
## Scroll
suggestRooms_scroll = Scrollbar(searchRoom_frame)
suggestRooms_scroll.grid(row = 2, column = 2, rowspan = 6)
suggestRooms_list.configure(yscrollcommand=suggestRooms_scroll.set)
suggestRooms_scroll.configure(command=suggestRooms_list.yview)
# -----------------------------------------------------------------------------------------

# Time and date Frame
# -----------------------------------------------------------------------------------------
# Frame set up
timedate_frame = LabelFrame(window, text="Time and Date", relief=RIDGE)
timedate_frame.grid(row=0, column=1, sticky=E + W + N + S)
# Date set up
## What is the date the room will be used?
date_start = Label(timedate_frame, text = "Date").grid(row=1,column=3)
Label(timedate_frame, text = "/").grid(row=1,column=5)
Label(timedate_frame, text = "/").grid(row=1,column=7)
### Month
dateStart_month = Entry(timedate_frame)
dateStart_month.insert(0, datetime.datetime.now().strftime("%m"))
dateStart_month.grid(row=1,column=4)
### Day
dateStart_day = Entry(timedate_frame)
dateStart_day.insert(0, datetime.datetime.now().strftime("%d"))
dateStart_day.grid(row=1,column=6)
### Year
dateStart_year = Entry(timedate_frame)
dateStart_year.insert(0, datetime.datetime.now().strftime("%Y"))
dateStart_year.grid(row=1,column=8)
# Time set up
## What time will the room be used from?
time_start = Label(timedate_frame, height = 3, text = "Time Start")
time_start.grid(row=2,column=3)
Label(timedate_frame, text = ":").grid(row=2,column=5)
### AM or PM
timeStart_PM = StringVar()
timeStart_PM.set(0)
### Start Hours
timeStart_hours = Entry(timedate_frame)
timeStart_hours.grid(row=2,column=4)
### Start Minutes
timeStart_minutes = Entry(timedate_frame)
timeStart_minutes.grid(row=2,column=6)
## What time will the room be used until?
time_end = Label(timedate_frame, text = "Time Ends")
time_end.grid(row=4,column=3)
Label(timedate_frame, text = ":").grid(row=4,column=5)
### AM or PM
timeEnd_PM = StringVar()
timeEnd_PM.set(0)
### Ending Hours
timeEnd_hours = Entry(timedate_frame)
timeEnd_hours.grid(row=4,column=4)
### Ending Minutes
timeEnd_minutes = Entry(timedate_frame)
timeEnd_minutes.grid(row=4,column=6)
# -----------------------------------------------------------------------------------------

# Show schedule Frame
# -----------------------------------------------------------------------------------------
# Frame set up
showSched_frame = LabelFrame(window, text="Schedule", relief=RIDGE)
showSched_frame.grid(row=8, column=1, sticky=E + W + N + S)
# Show a rooms's schedule
scheduleRooms_list = Listbox(showSched_frame, height = 20, width = 120)
#scheduleRooms_list = Treeview(showSched_frame, height = 20, width = 120, columns=('Dose', 'Modification date'))
scheduleRooms_list.grid(row = 9, column = 1, rowspan = 20, columnspan = 9)
## Scroll
scheduleRooms_scroll = Scrollbar(showSched_frame)
scheduleRooms_scroll.grid(row = 9, column = 11, rowspan = 20)
scheduleRooms_list.configure(yscrollcommand=scheduleRooms_scroll.set)
scheduleRooms_scroll.configure(command=scheduleRooms_list.yview)
# -----------------------------------------------------------------------------------------

# Window Buttons
# -----------------------------------------------------------------------------------------
searchRoom_button = Button(searchRoom_frame, text = "Search", command = room.altRooms)
searchRoom_button.grid(row = 1, column = 2)
suggestRooms_list.bind("<Double-1>", room.setRoom)
suggestRooms_list.bind("<Double-1>", room.showRoomSch, add="+")
timeStart1_button = Radiobutton(timedate_frame, text = "A.M.", variable = timeStart_PM, value="0")
timeStart1_button.grid(row=2,column=8)
timeStart2_button = Radiobutton(timedate_frame, text = "P.M.", variable = timeStart_PM, value="1")
timeStart2_button.grid(row=2,column=9)
timeEnd1_button = Radiobutton(timedate_frame, text = "A.M.", variable = timeEnd_PM, value="0")
timeEnd1_button.grid(row=4,column=8)
timeEnd2_button = Radiobutton(timedate_frame, text = "P.M.", variable = timeEnd_PM, value="1")
timeEnd2_button.grid(row=4,column=9)
enterTime_button = Button(timedate_frame, text = "Enter time", command = room.setTime)
enterTime_button.grid(row=2,column=10, rowspan = 8)
clearBoard_button = Button(window, text = "Clear", command = room.clearBox)
clearBoard_button.grid(row=8,column=0)
# -----------------------------------------------------------------------------------------
window.mainloop()
