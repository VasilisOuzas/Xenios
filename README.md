<div align="center">
  <img src="assets/logo.png" alt="Xenios" width="120" />
  <h1>Xenios</h1>
  <p>A an application for hospitality.</p>

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

# Current-Version (v.0.1)
Following the previous v.0.7 ([v.0.7 code_report.md](https://github.com/VasilisOuzas/Xenios/commit/d9c9e438e1dea038a2b111fd6e458207ff963800)) the application was updated with a visual upgrade, showing which rooms have extra camp beds or baby coats. The leatest version also includes a reservation edit tool that helps the user to edit all detail of amy reservation from the list, which now is alphabeticaly sorted. Moreover, if the reservation is long enough on the calendar, it will include the full name instead of only the last/first name compared to previous versions.


# How to use
The user downloads the [xenios.v.1.0.zip](https://github.com/VasilisOuzas/Xenios/releases/tag/v1.0) and extracts it. On the extracted folder, the user can access the /data folder and modify the rooms.json file accordingly to their needs. Each room entry should have a distinct id, an optional name and a choice between "double room"/"triple room"/"qudruple room" (("Δίκλινο"/"Τρίκλινο"/"Τετράκλινο")right now the app can only used in Greek. Later version will support English). After the rooms.json has been modified, the user can simply run the Xenios.exe . The "callendar"/"Ημερολόγιο" tab inlcudes the calendar/matrix that is arranged according to the rooms.json. Hovering on any reservation will show you information about them. you can navigate through the months via the arrows on the top left corner. On the "New Reservation"/"Νέα Κράτηση" tab, the user inputs new reservations. If the room/rooms are already reserved for the wanted period, they get promted an error message telling them that there is a dates conflit with another reservation. All the reservations done (which already exist in the data/reservations.json) are alphabetically sorted in the list below. Clicking/selecting a reservation enables you to modify it. By clicking "Modify"/"Επεξεργασία" after selecting a reservation you will see all the saved data displayed on the inputs which you can modify again, to save the modified data, you simply click "add reservation"/"Πρσθήκη Κράτησης". Deleting reservations is as simple as selecting them and then clicking "Delete Reservation"/"Διγραφή Κράτησης". Additionaly, the third and last tab acts as a way to check the availability of the room types that you are interesetd in making a reservation for a specific time period. The app informs  this way the user about the available rooms. 

# The Spark
My parents own a Hotel at my hometown and they have been working on with the help of their parents for a lot of years now. They are very experienced and I got myself working on the bussiness when I became a teenager. When I got into university and learned how to code, I realised that they should advance, past using outdated methods like printed lists and papers where they note each reservation/accommodation and try to find a new better and more easy solution for their job. Since I am into homelabing and I partisipated in reasearch teams in my university, I decided to make a custom solution by myself. Anybody is allowed to distribute/share and modify my work, although doing so for self profit is prohibited by the GNU Public Lisence. I trully intend into updating this app and making it more accessible for anybody. If you're interested in helping me please contact me before trying to commit anything on any branches.

# Social:
`discord:`@jay_bulker  
 `Mail:` vasilisouzas@gmail.com  
 `Instagram:` @Vas_Ouzas

# Similar Open Source Projects:
 [HotelDruid](https://www.hoteldruid.com/en/)  
[MRBS](https://mrbs.sourceforge.io/sshots.php)
