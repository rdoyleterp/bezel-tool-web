Bezel Tool Workflow - README

Overview
The Bezel Tool is a utility designed to streamline the creation of device-specific presentation slides. It allows users to capture screenshots, process them with bezels, and integrate them into Google Slides presentations automatically.

This document provides detailed instructions for each step in the workflow.

Workflow Steps

1. Prepare Screenshots
Before using the Bezel Tool, ensure your screenshots are captured in the required dimensions:
- Desktop: 1680x1050
- iPad (Landscape): 1366x1024
- iPad (Portrait): 1024x1366
- iPhone 15: 440x844

Recommended Tool: Window Resizer Chrome Extension
Setup Instructions:
1. Install the Window Resizer extension from the Chrome Web Store.
2. Use the extension to adjust your browser's Viewport dimensions (not the window size).
   - Enable the "Resize Viewport" toggle in the extension settings.
3. Enter the required dimensions for the desired device and capture the screenshot.

2. Use the Bezel Tool GUI
1. Launch the Bezel Tool:
   - Open the executable file (bezel_tool_gui).
2. Set Series Name:
   - Enter a name for your image series (e.g., Project_X).
3. Set Output Folder:
   - Click Set Folder to choose the directory where processed images will be saved.
4. Select Bezel:
   - Choose the appropriate bezel from the dropdown menu.
5. Upload Images:
   - Click Upload and select the screenshots you want to process.
6. Process Images:
   - Click Process to apply bezels and save processed images to the output folder.
   - The tool will log progress and any errors in the status box.

3. Upload to Google Drive
1. Create a Folder:
   - In Google Drive, create a folder for your processed images.
2. Upload Images:
   - Drag and drop or upload the processed images to the folder.

4. Configure the Google Slides Template
1. Open the Presentation:
   - Use the provided Google Slides template: Google Slides Template.
     (https://docs.google.com/presentation/d/1E1eAcTJoVag5GOawpvxoNpuI9Sl1ObNuKxFwnghKcq4/edit#slide=id.g31c76747aa4_0_1051)
2. Set the Folder ID:
   - From the Custom Tools menu, select Update Folder ID.
   - Enter the Google Drive Folder ID for the uploaded images. The ID can be found in the folder's URL:
     https://drive.google.com/drive/folders/<Folder_ID>
3. Run the Script:
   - From the Custom Tools menu, select Process New Files.
   - The script will automatically add the images to slides using the appropriate templates.

Frequently Asked Questions (FAQs)

Q1. What if my screenshots don't match the required dimensions?
- Use the Window Resizer Chrome extension to adjust your viewport dimensions and capture screenshots with precision.

Q2. How do I find the Google Drive Folder ID?
- Navigate to your folder in Google Drive and copy the string of characters in the URL after /folders/.

Q3. What should I do if the tool can't find matching templates?
- Ensure your processed image filenames follow the convention:
  seriesname_bezelname_index.png
  Example:
  Project_X_desktop_1.png

Q4. Can I reprocess images or change the folder ID?
- Yes. Simply re-run the Update Folder ID function in Google Slides to update the configuration.

Q5. What if I encounter errors during processing?
- Check the status box in the Bezel Tool or the log output in Google Slides for details.

Support
For further assistance, contact [Your Team/Support Contact Information].

Known Limitations
- The tool currently requires manual setup for screenshots.
