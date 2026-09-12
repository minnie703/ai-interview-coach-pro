from flask import Flask, render_template, request
import ollama

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/interview", methods=["POST"])
def interview():

    role = request.form["role"]
    answer = request.form.get("answer", "")

    # Generate Question
    if answer == "":

        prompt = f"""
        You are a professional technical interviewer.

        Generate ONE interview question for a {role}.

        Return only the question.
        """

        response = ollama.chat(
            model="llama3.2",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        question = response["message"]["content"]

        return render_template(
            "index.html",
            role=role,
            question=question
        )

    # Evaluate Answer
    prompt = f"""
You are a senior interview coach.

Job Role:
{role}

Interview Question:
{request.form['question']}

Candidate Answer:
{answer}

Evaluate the answer and provide:

1. Score out of 10
2. Strengths
3. Weaknesses
4. Improved Answer Example

Keep the feedback professional and easy to understand.
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    feedback = response["message"]["content"]

    return render_template(
        "index.html",
        role=role,
        question=request.form["question"],
        answer=answer,
        feedback=feedback
    )


if __name__ == "__main__":
    app.run(debug=True)