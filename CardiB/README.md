# CarDB

Your task is to implement `CarDB` class which is meant to be a high level
interface for accessing and modifying database containing information about cars.
There are some tests for this class in `tests/test_cardb.py` which should
give you an idea how implemented methods should work.
Please stick to the following points during implementation:


- Use `Python` version >= `3.6` and apply `PEP8` rules
- Use `pytest` test framework ([link](https://docs.pytest.org/en/latest/))
- Use `PostgreSQL` database version >= `10.0` ([link](https://www.postgresql.org/))
- Do not modify `tests/test_cardb.py` - these tests should pass in their current form
- All tests should be executed on 'clear' database
- Write more tests! The more code coverage the better ([pytest-cov](https://pytest-cov.readthedocs.io/en/latest/))
- You will get a lot of bonus points for designing and implementing `REST API` around `CarDB` class
- Use `JSONB` datatype for `info` attribute of `types.Car`
- Implementing `query_cars` method is too hard? Leave it and start with `REST API`


## Get started
```sh
# install pytest
pip install pytest

# install cardb package
cd straal-intern-task-2018/
pip install -e .
```
## Questions?
Don't hesitate to mail me: pawel.dobrowolski@straal.com
