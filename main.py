from flask import Flask, redirect, render_template, request
from chatbot import main
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import random

app = Flask(__name__)

news_headlines = [
        "Breaking News: Scientists discover a new species of dinosaur",
        "Technology Update: New smartphone with advanced features released",
        "Sports News: Local team wins championship title",
        "Business Update: Stocks soar to all-time high",
        "Entertainment Buzz: Highly anticipated movie trailer released",
    ]

exit_words = [
    "goodbye",
    "farewell",
    "bye",
    "adios",
    "later",
    "ciao",
    "cheers",
    "so long",
    "peace",
    "see ya",
    "out",
    "toodles",
    "hasta",
    "sayonara",
    "exit",
    "end",
    "stop",
    "quit",
    "close",
    "finish",
]
goodbye_words = [
    "Farewell, dear friend! Until our next digital encounter.",
    "As my circuits rest, I bid you adieu, and may your days be filled with wonder.",
    "It's time to sign off now. Remember, I'm just a chat away if you need me again.",
    "Wishing you a wonderful day ahead! Goodbye for now.",
    "Stay curious, stay kind, and remember that I'll be here whenever you need a virtual pal. Goodbye!",
    "Thank you for sharing this conversation with me. Until we meet again, take care.",
    "It's been a pleasure chatting with you. Goodbye and keep exploring the vast realms of knowledge.",
    "May the digital winds guide you towards new adventures. Farewell!",
    "Signing off, but never truly gone. I'll be eagerly awaiting our next interaction. Goodbye!",
    "Until our paths cross in the digital realm once more, stay safe and farewell!",
]

@app.route("/",methods=['GET', 'POST'])
def home():
    data={}
    response_num = 0
    if request.method == 'POST':
        tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
        model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
        question = request.form.get('input')
        user_input = tokenizer.encode(question + tokenizer.eos_token, return_tensors="pt")
        ques_lst = question.split()
        global chat_history
        chatbot_input = (
            torch.cat([chat_history, user_input], dim=-1)
            if response_num > 0
            else user_input
        )
        chat_history = model.generate(
            chatbot_input,
            max_length=10000000,
            do_sample=True,
            top_k=70,
            top_p=0.95,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id,
        )

        chat = tokenizer.decode(
            chat_history[:, chatbot_input.shape[-1] :][0], skip_special_tokens=True
        )

        if any(word in question.lower() for word in ["news", "update", "headline"]):
            response = "Here are some recent news headlines:\n" + "\n".join(news_headlines)
        elif any(word in exit_words for word in ques_lst):
            cont = False
            response = random.choice(goodbye_words)
        else:
            response = chat

        print(f"Bot: {response}")
        response_num += 1

    return render_template("index.html",context=data)
    # print(current_user.is_authenticated)
    # curr_user_id = current_user.id
    # # current_user gives us the info about the current user that is logged in
    # events_lst = Event.query.filter_by(user_id=curr_user_id).all()
    # event_name = []
    # event_id = []
    # for i in events_lst:
    #     event_name.append(i.ename)
    # for j in events_lst:
    #     event_id.append(i.id)
    # return render_template("home.html", uname=current_user.name.upper(), event_name=event_name, user_id=curr_user_id, event_id=event_id)

# @app.route("/response/<string:user_input")
# def api_response():


if __name__ == '__main__':
    app.run(debug=True)