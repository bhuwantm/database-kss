# Database and Query Optimization

## Database Setup
Follow the instruction in the <a href='./setup/README.md'>README.md</a>


## Script Setup

#### Install Dependencies

```
pip install -r requirements.txt
```

#### Copy env file
```
cp .env.example .env
```

#### Creating Table and Seeding Data
```
python main.py seed
```

## Running Scripts
Once setup has been completed each script in the main folder can be run. For example
```
python shared_locks.py
```

Once the script is executed the outputs will be seen in the terminal. <br/>
Each script will simulate the corresponding behavior.
