# fn_ont_expunge
Performs ONTs expunge from OLT and DB

## Usage
```python
from fn_ont_expunge import ONTExpunge
with ONTExpunge(
        ont_sn='ont_sn',
        ontid=1,
        portid=0,
        slotid=1,
        frameid=0,
        olt_device_details={'host': 'some_host', 'password': 'password'},
        logger=logger, # logging.Logger object
        old_db_session=db_session # sqlachemy.orm.Session object
) as expunge:
    expunge.expunge_ont()
```



