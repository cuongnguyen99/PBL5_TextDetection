# PBL5_TextDetection

#Cương
- Install tesseract Raspberry Pi : https://www.pyimagesearch.com/2018/09/17/opencv-ocr-and-text-recognition-with-tesseract/
- Install tesseract for Windows (Ver 4.0.1) : https://digi.bib.uni-mannheim.de/tesseract/
- Tesseract OCR for Non-English Languages : https://www.pyimagesearch.com/2020/08/03/tesseract-ocr-for-non-english-languages/?fbclid=IwAR15hFBBoGhOT0nLvRe5CTMrV6BvJVlPRwlFjlwsWYlsGQqM1KngIWg1-OI
- Text recognition (OCR) with Tesseract and Python: 
		https://www.youtube.com/watch?v=6DjFscX4I_c
		https://www.youtube.com/watch?v=JkzFjj2hjtw

#Hoàng
* Because Tesseract only detect the text at a certain angle, use Detect corners of the package, then align the package to the right angle.
* Somehow the model can not upload on github so I upload it on drive
* https://drive.google.com/drive/folders/1SxuBtjnOlrw2f86C5kGL2Y4keVVZrWoF?usp=sharing

#Cường
* Install unidecode : https://gist.github.com/thuandt/3421905?fbclid=IwAR2TTRuHQSdr1jqRA49raOQw94JhvKWj2gkr2CLrCcI1atPBEZofr4FZc1g
* run project : file all.py (Demo 12-6-2021)

#Phúc

* Requirement :
	- node version up 14.17
	- npm version up 7.x

* Run project:
	- cd serverNodejs
	- npm install
	- edit file db.js in serverNodejs models > db.js
	- npm run sync-db  (create and settup db on mysql)
	- npm run init-admin (create and init admin account into db)
	- npm start (run on port 8000)
