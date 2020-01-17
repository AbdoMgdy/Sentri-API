from flask_table import Table, Col


class Results(Table):
    id = Col('Id', show=False)
    user_id = Col('User_id')
    number = Col('Number')
    items = Col('Items')
    total = Col('Total')
    finished = Col('Finished')
