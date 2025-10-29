1) Run ```database.py``` (to create database and/or database tables)
2) Run ```load_database.py``` (to load dummy data into tables)
3) Edit ```app.py```, if necessary (if you have a ```MYSQL``` password, insert into empty ```password``` string)
5) Run your model's ```.py``` file (i.e., ```drivers.py```)

Note:
```.env.example``` can be used to store your personal ```MYSQL``` data for reference

Helpful Functions:
```db.session.add()```
```db.session.commit()```