# Progress (Version 0.3)
> This is an experimental version of the application. It is not optimized, polished or properly tested yet. Use it with your own resonsibility
---
This is the third unofficial version of the application. It is not woring properly yet. It implements a more advanced GUI than version one for checking availability through specific dates and booking reservations.
The data input/output stream is hosted via .json files that are saved in the `/data` directory.

# Fixes/Upgrades over prior Version 0.1
- The dating format changed, from DD-MM to DD/MM
- The colours on the gui now work as intented
- The room identification got fixed
- Reservation deletion now works flawlessly
- Reservation/Date checking now gives the correct result
- 





 # Issues 
- The program counts one more staying than it should. By default when you make a reservation for, let's say 17 - 27, the customer would stay for 10 nights and on the 27th he would give up the room ending up with 10 nights instead of 1 that the coloured matrix shows. This way, people can rent the room again on the 27th after the first customer leaves.
- Still the GUI could be more visually appealing
- There are more interactive stuff missing from the panel
- I want tot debloat the code by removing some useless stuff about phone number validation added by claude.

## Extra notes
On this version, the .json files were also changed
