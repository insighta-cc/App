# Get Json Response From LLM

## Setting Expectations with the “System” Role

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
