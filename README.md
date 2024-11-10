# create-rekordbox-xml-from-music-folder
Generates XML file for importing in Rekordbox that creates playlists from all folders within your primary music folder. The XML file will be generated in a way that prevents duplicate tracks from appearing in your main collection, but keeps all playlists complete.

Download the .exe file under the releases section of this repo for easy usage of this app.

This will be primarily useful for people that are trying to set up a fresh rekordbox library and people that are transitioning their library in to Rekordbox from other DJ software or music management applications.

To use the application:
  1. select a source folder that contains folders that you would like to import in to rekordbox as a playlist
  2. select a destination folder and file name for your XML
  3. click generate. It will take a few minutes for the file to be created.


To import the file in to Rekordbox:
  1. file > preferences > advanced
  2. click 'browse' under 'imported library'
  3. select your generated XML
  4. close out of preferences menu
  5. find the "Display Rekordbox XML" tab on the collection explorer in the bottom left of the screen
  6. Your folders should be displayed in this window as playlists. If there were tracks not in playlists they should be under the "all tracks" section of this menu.
  7. right click on the master playlist to import all playlists, or right click on individual playlists that you would like to import
