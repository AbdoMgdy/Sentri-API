from flask_table import Table, Col


class Results(Table):
    id = Col('Id', show=False)
    number = Col('Number')
    items = Col('Items')
    total = Col('Total')
    finished = Col('Finished')


class Items(Table):
    name = Col('Name')
    quantity = Col('Quantity')
    _type = Col('Spicy/Normal')
    notes = Col('Notes')
    combo = Col('Combo')


   
