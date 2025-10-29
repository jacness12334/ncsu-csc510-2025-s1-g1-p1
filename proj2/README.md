# Backend Instructions
1) Run ```database.py``` (to create database and/or database tables)
2) Run ```load_database.py``` (to load dummy data into tables)
3) Edit ```app.py```, if necessary (if you have a ```MYSQL``` password, insert into empty ```password``` string)
5) Run your model's ```.py``` file (i.e., ```drivers.py```)

##Notes
* ```.env.example``` can be used to store your personal ```MYSQL``` data for reference
* Recommended to make sub-branches from backend for each model (i.e., ```backend-drivers```)

##Helpful Functions
- ```db.session.add()``` (adding instance of model to session)
- ```db.session.commit()``` (committing all session changes to database)
