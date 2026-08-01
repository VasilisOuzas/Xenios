<div align="center">
  <img src="assets/logo.png" alt="Xenios" width="120" />
  <h1>Xenios</h1>
 

  <p>
    <a href="https://github.com/VasilisOuzas/Xenios/releases/latest"><img alt="GitHub Release" src="https://img.shields.io/github/v/release/VasilisOuzas/Xenios?style=for-the-badge&logo=github&color=1a1a2e&labelColor=0d0d0d"/></a>
    <a href="https://github.com/VasilisOuzas/Xenios/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/VasilisOuzas/Xenios?style=for-the-badge&logo=github&color=1a1a2e&labelColor=0d0d0d"/></a>
    <a href="https://github.com/VasilisOuzas/Xenios/releases/latest"><img alt="Downloads" src="https://img.shields.io/github/downloads/VasilisOuzas/Xenios/total?style=for-the-badge&logo=github&color=1a1a2e&labelColor=0d0d0d"/></a>
    <a href="https://matrix.to/#/#xenios:matrix.org"><img alt="matrix" src="https://img.shields.io/badge/Matrix-26A5E4?style=for-the-badge&logo=matrix&labelColor=0d0d0d"/></a>
    <a href="LICENSE"><img alt="License" src="https://img.shields.io/github/license/VasilisOuzas/Xenios?style=for-the-badge&color=1a1a2e&labelColor=0d0d0d"/></a>
  </p>
<div>
  
# Overview
Xenios is a custom software solution ,helping people of the hospitality industry to plan accomodations at their facilities with an easier and more effective way. This open source project helps hotelers and room renters create and manage lists on a calendar-based system. It provides high customizability and flexibility regarding the different types of information that can be noted for each accommodation. Although there are similar open source projects, most of them are web based and their user inderface can feel rather complex and outdated at times. Xenios uses a modern, vivid GUI and needs no access to the internet to work. It uses .json files to save and modify all the data (/data directory). All the work is done localy on the users computer (fow the time being Xenios is only supported on windows devices. I am currently working on a working version for linux). All the work is done through python and the code is available at the [main.py](https://github.com/VasilisOuzas/Xenios/blob/main/src/main.py) file.

# Current-Version (v.1.1)
The latest version has added support for both Greek and English users. To achieve this, there are separate Xenios_GR.exe and Xenios_EN.exe for each language's speakers respectfully. Moreover, `/src` now includes the code (.py) for each executable. In order to work around to separate .exe's there are now two directories, one for each language (/data_EN and /data_GE). Each directory includes its own `rooms.json` file and the `reservations.json` still remains in the original /data directory.  
The latest version also fixed a bug that deleted entries from the reservations.json when the user exited the program while there was a reservation edit underway. There is also new code to support the usage of more room types such as suites and single rooms.


# How to use
The user downloads the [xenios.v.1.1.zip](https://github.com/VasilisOuzas/Xenios/releases/tag/v.1.1) and extracts it. On the extracted folder, the user can access the /data_EN or the /data_GR folders and modify the rooms.json files accordingly to their needs. Each room entry should have a distinct id, an optional name and a choice between "double room"/"triple room"/"qudruple room" ("Δίκλινο"/"Τρίκλινο"/"Τετράκλινο"). Here's an example entry:
```
[{"id": 1, "number": "1", "type": "Single"},
  {"id": 2, "number": "2", "type": "Double"},
  {"id": 3, "number": "3", "type": "Triple"}]
```
After the rooms.json has been modified, the user can simply run the Xenios_GR.exe or Xenios_EN.exe . The "callendar"/"Ημερολόγιο" tab inlcudes the calendar/matrix that is arranged according to the rooms.json. Hovering on any reservation will show you information about them. you can navigate through the months via the arrows on the top left corner. On the "New Reservation"/"Νέα Κράτηση" tab, the user inputs new reservations. If the room/rooms are already reserved for the wanted period, they get promted an error message telling them that there is a dates conflit with another reservation. All the reservations done (which already exist in the data/reservations.json) are alphabetically sorted in the list below. Clicking/selecting a reservation enables you to modify it. By clicking "Modify"/"Επεξεργασία" after selecting a reservation you will see all the saved data displayed on the inputs which you can modify again, to save the modified data, you simply click "add reservation"/"Πρσθήκη Κράτησης". Deleting reservations is as simple as selecting them and then clicking "Delete Reservation"/"Διγραφή Κράτησης". Additionaly, the third and last tab acts as a way to check the availability of the room types that you are interesetd in making a reservation for a specific time period. The app informs  this way the user about the available rooms. 

# The Spark
My parents own a Hotel at my hometown and they have been working on with the help of their parents for a lot of years now. They are very experienced and I got myself working on the bussiness when I became a teenager. When I got into university and learned how to code, I realised that they should advance, past using outdated methods like printed lists and papers where they note each reservation/accommodation and try to find a new better and more easy solution for their job. Since I am into homelabing and I partisipated in reasearch teams in my university, I decided to make a custom solution by myself. Anybody is allowed to distribute/share and modify my work, although doing so for self profit is prohibited by the GNU Public Lisence. I trully intend into updating this app and making it more accessible for anybody. If you're interested in helping me please contact me before trying to commit anything on any branches.

# Social:
`discord:`@jay_bulker  
 `Mail:` vasilisouzas@gmail.com  
 `Instagram:` @Vas_Ouzas

# Similar Open Source Projects:
 [HotelDruid](https://www.hoteldruid.com/en/)  
[MRBS](https://mrbs.sourceforge.io/sshots.php)
