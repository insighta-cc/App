# Insighta.cc
![](./app/static/images/Logo-Insighta-V.png)
## How To Deploy

## Setup .env

```shell
PYTHONPATH=.
GEMINI_API_KEY=<Your-Gemini-Secret-Key>
SKILL_LIST=Java, Javascript, Python, C, C++, C#, PHP, Swift, Ruby, TypeScript, Go, Kotlin, Rust, Objective-C, Scala, Shell, Dart, Haskell, Matlab, Perl, R, Groovy, Lua, Ada, Assembly, COBOL, D, Elixir, Erlang, F#, Fortran, Julia, Lisp, OCaml, Pascal, PowerShell, Prolog, Scheme, Scratch, Smalltalk, SQL, Tcl, VBA, Visual Basic, ABAP, Apex, Awk, ColdFusion, Crystal, Other
LIST_ADDRESS_URL=https://main-wjaxre4ena-uc.a.run.app/usage_addresses
USAGE_RECORDS_URL=https://main-wjaxre4ena-uc.a.run.app/usage_records
GOOGLE_STORAGE_BUCKET_URL=https://storage.googleapis.com/contextpilot/summary_data
```

```plaintext
1. install python3, python3-pip
2. mkdir demo; cd demo
3. git clone https://github.com/jdyuankai/Insighta.AI.git
4. cd Insighta.AI
5. python -m venv venv
6. source venv/bin/activate
7. pip install -r requirements.txt
8. flask db migrate; flask db init; flask db upgrade
9. flask run (python run.py is ok too)
```

## Setup Scheduler Interval 

```shell
nano app/__init__.py
```

```python
    scheduler.add_job(id='Fetch Chat Record', func=fetch_chat_with_context, trigger='interval', hours=1)    # Customize your interval for fetching data
    scheduler.add_job(id='Summary Score', func=summary_score_with_context, trigger='interval', hours=6)     # Customize your interval for summary
```

## Query Score

```shell
curl -X GET https://insighta.cc/api/v1/summary/<address>
```