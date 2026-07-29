# Verification

## Baseline
- Ran the existing pytest suite before changes; recorded baseline (see below).

## Test runs (current)

```
python c:\workspace\app\.venv-1\Scripts\python.exe
cwd c:\workspace
...........                                                              [100%]
============================== warnings summary ===============================
app\models.py:52
	c:\workspace\app\models.py:52: PydanticDeprecatedSince20: Pydantic V1 style `@validator` validators are deprecated. You should migrate to Pydantic V2 style `@field_validator` validators, see the migration guide for more details. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
		@validator("title")

app\models.py:58
	c:\workspace\app\models.py:58: PydanticDeprecatedSince20: Pydantic V1 style `@validator` validators are deprecated. You should migrate to Pydantic V2 style `@field_validator` validators, see the migration guide for more details. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
		@validator("tags", pre=True)

app\models.py:43
	c:\workspace\app\models.py:43: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
		class TaskCreate(BaseModel):

app\models.py:75
	c:\workspace\app\models.py:75: PydanticDeprecatedSince20: Pydantic V1 style `@validator` validators are deprecated. You should migrate to Pydantic V2 style `@field_validator` validators, see the migration guide for more details. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
		@validator("title")

app\models.py:85
	c:\workspace\app\models.py:85: PydanticDeprecatedSince20: Pydantic V1 style `@validator` validators are deprecated. You should migrate to Pydantic V2 style `@field_validator` validators, see the migration guide for more details. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
		@validator("tags", pre=True)

app\models.py:66
	c:\workspace\app\models.py:66: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
		class TaskUpdate(BaseModel):

app\\.venv-1\\Lib\\site-packages\\fastapi\\routing.py:233
	c:\workspace\app\.venv-1\Lib\site-packages\fastapi\routing.py:233
	c:\workspace\app\.venv-1\Lib\site-packages\fastapi\routing.py:233
	c:\workspace\app\.venv-1\Lib\site-packages\fastapi\routing.py:233
	c:\workspace\app\.venv-1\Lib\site-packages\fastapi\routing.py:233
	c:\workspace\app\.venv-1\Lib\site-packages\fastapi\routing.py:233
		c:\workspace\app\.venv-1\Lib\site-packages\fastapi\routing.py:233: DeprecationWarning: 'asyncio.iscoroutinefunction' is deprecated and slated for removal in Python 3.16; use inspect.iscoroutinefunction() instead
		is_coroutine = asyncio.iscoroutinefunction(dependant.call)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
11 passed, 12 warnings in 0.38s
```

## Manual checks
- Create a task with a due date and see the due date on the card.
- Create a task with tags and see tag chips on the card.
- Use the overdue filter and tag filter to narrow the list.

## Break tests
- Planned Break Test: create invalid inputs (too many tags, invalid date) and expect 422 responses.


(Verification run output appended below.)
