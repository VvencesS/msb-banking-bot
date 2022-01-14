import json
from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import os

from GetCurrencyRate import CurrencyRate

# Creating a chatbot Instance
bot = ChatBot(
    'MSBBankingBot',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    logic_adapters=[{
        'import_path': 'chatterbot.logic.BestMatch',
        'default_response': 'Quý khách vui lòng đặt câu hỏi rõ ràng hơn!',
        'maximum_similarity_threshold': 0.90
    }],
    read_only=True,
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace',
        'chatterbot.preprocessors.unescape_html'
    ],
    database_uri='mongodb://127.0.0.1:27017/msbchatbotdb'
)

# user choose whether to train with English corpus data
# decision = input('Huấn luyện chatbot với  dữ liệu English corpus? (Y/N): ')

# if decision == 'Y':
#     print('\nĐang huấn luyện chatbot với dữ liệu English corpus')
#     trainer_corpus = ChatterBotCorpusTrainer(bot)
#     trainer_corpus.train('chatterbot.corpus.english')

# Cập nhật giá ngoại tệ và lưu giá vào file huấn luyện
# dateTime, exrateList = CurrencyRate.getCurrencyRate()
# data = '\n\nTỷ giá ngoại tệ (cập nhật lúc: '+dateTime+ ') \n'
# data += ' n-Mã ngoại tệ / Tên ngoại tệ / Mua / Transfer / Bán '
# for exrate in exrateList:
#     data += ' n-' + exrate['currencyCode']
#     data += ' / ' + exrate['currencyName']
#     data += ' / ' + exrate['buy']
#     data += ' / ' + exrate['transfer']
#     data += ' / ' + exrate['sell']
# print(data)

# file = open('./banking_data/tygiangoaitevavang.txt', 'ab')
# file.write(bytes(data, encoding='utf8'))
# file.close()
# print(dateTime)
# print(exrateList)

# Tạo app
app = Flask(__name__)
app.static_folder = 'static'


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/get-response", methods=['GET'])
def get_bot_response():
    userText = request.args.get('msg')
    result = str(bot.get_response(userText))
    return jsonify({'result': result})


@app.route("/api/delete-learned-data", methods=['GET'])
def delete_learned_data():
    # delete learned data
    bot.storage.drop()
    return jsonify({'result': 'Đã xóa dữ liệu!'})


@app.route("/api/write-data-to-file", methods=['POST'])
def writeDataToFile():
    data = json.loads(request.data)

    for duLieu in data:
        directory = './banking_data_test/'
        tenFileCuaNhan = 'cauhoichung'
        locationFile = ''
        list_CH_TL_Str=''

        if duLieu.get('tenFile') != None:
            tenFileCuaNhan = duLieu.get('tenFile')
        locationFile = directory + tenFileCuaNhan + '.txt'

        for ch_tl in duLieu.get('dsCH_TL'):
            list_CH_TL_Str+='\n'+ch_tl.get('cauHoi')
            list_CH_TL_Str+='\n'+ch_tl.get('traLoi')
        file = open(locationFile, 'w+')
        file.write(bytes(list_CH_TL_Str, encoding='utf8'))
        file.close()

    return jsonify({'result': 'Đã ghi dữ liệu!'})


@app.route("/api/training-bot", methods=['GET'])
def training_bot():
    # locate training folder
    directory = './banking_data'
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):  # only pick txt file for training
            print('\nĐang huấn luyện chatbot với file: ' +
                  os.path.join(directory, filename))
            training_data = open(os.path.join(
                directory, filename), encoding="utf8").read().splitlines()
            trainer = ListTrainer(bot)  # bot training
            trainer.train(training_data)
        else:
            continue
    return jsonify({'result': 'Đã huấn luyện xong!'})


if __name__ == "__main__":
    app.run()
