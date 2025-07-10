py -m venv env

2
env\Scripts\activate

3
pip install -r requirements.txt

4. crear DB
python -c "from dao.db import init_db; init_db()"

5. ejecutar
py main.py

