# Insighta.AI


## [Requirement](./Requirement.md)

## How To Deploy

```text
1. install python, python-pip
2. mkdir demo; cd demo
3. git clone https://github.com/jdyuankai/Insighta.AI.git
4. cd Insighta.AI
5. python -m venv venv
6. source venv/bin/activate
7. pip install -r requirements.txt
8. flask db init; flask db migrate; flask db upgrade
9. flask run (python run.py is ok too)
```

## Setup .env

```shell
PYTHONPATH=.
GEMINI_API_KEY=<Your-Gemini-Secret-Key>
SKILL_LIST=Java, Javascript, Python, C, C++, C#, PHP, Swift, Ruby, TypeScript, Go, Kotlin, Rust, Objective-C, Scala, Shell, Dart, Haskell, Matlab, Perl, R, Groovy, Lua, Ada, Assembly, COBOL, D, Elixir, Erlang, F#, Fortran, Julia, Lisp, OCaml, Pascal, PowerShell, Prolog, Scheme, Scratch, Smalltalk, SQL, Tcl, VBA, Visual Basic, ABAP, Apex, Awk, ColdFusion, Crystal, Other
LIST_ADDRESS_URL=https://main-wjaxre4ena-uc.a.run.app/usage_addresses
USAGE_RECORDS_URL=https://main-wjaxre4ena-uc.a.run.app/usage_records
GOOGLE_STORAGE_BUCKET_URL=https://storage.googleapis.com/contextpilot/summary_data
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
curl -X GET http://<your uri>/summary/<address>
```


## Get Json Response From LLM -Setting Expectations with the “System” Role

I noticed that setting an initial message with the role as “system” helped. This way, you can instruct the model to stick to certain types of responses. For example, I used the following setup:

```json
{
  role: "system",
  content: "You are a machine that only returns and replies with valid, iterable RFC8259 compliant JSON in your responses"
}
```

This helps set a “systemic” instruction for the model to abide by, and I’ve found that it significantly improves consistency.

## Precise Prompt Formatting

Be as specific and clear as possible with your prompt. If you need a specific structure, don’t be shy to explicitly spell it out. For instance:

```javascript
const prompt = `generate a 4 question advanced and very hard quiz about ${subject} - provide the question, one correct answer and 3 wrong answers in a json array format. The objects will be called question1-4, correct_answer, and wrong_answers`;

```

## Sanity Check the Response

After I get the response, I validate and filter it to ensure that it follows the format I want. This can act as a fail-safe in case the model output deviates:

```javascript
const content = data.choices[0].message.content;
const parsedContent = JSON.parse(content);
if (Array.isArray(parsedContent)) {
  // Your logic here...
} else {
  console.error("Invalid format: Iterable array should be an array.");
  return null;
}
```

## The Big Picture

Here’s a chunk from my own code that incorporates the above principles:

```javascript
const generateQuizQuestions = async (apiKey, prompt) => {
  const url = 'https://api.openai.com/v1/chat/completions';
  const headers = {
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json'
  };
  const body = JSON.stringify({
    model: 'gpt-3.5-turbo',
    messages: [
      {
        role: "system",
        content: "You are a machine that only returns and replies with valid, iterable RFC8259 compliant JSON in your responses"
      },
      {
        role: 'user',
        content: prompt
      }],
    temperature: 0.7
  });

  const response = await fetch(url, { method: 'POST', headers, body });
  const data = await response.json();

  if (!data.choices || !data.choices[0] || !data.choices[0].message || !data.choices[0].message.content) {
    return null;
  }

  const content = data.choices[0].message.content;
  const parsedContent = JSON.parse(content);

  if (Array.isArray(parsedContent)) {
    return parsedContent.map(q => {
      return {
        question: q.question,
        correct_answer: q.correct_answer,
        options: [q.correct_answer, ...q.wrong_answers].sort(() => 0.5 - Math.random())
      };
    });
  } else {
    console.error("Invalid format: Iterable array should be an array.");
    return null;
  }
};
```

It works for ChatGPT and Gemini.
