import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Chave da API do Telegram
key_api = "8027596930:AAEC0uSwZ8zKv_b6xzyDvD7STlFjOMIumZM"
bot = telebot.TeleBot(key_api)

# Diretório onde as imagens de amostra estão armazenadas
image_folder = os.path.join(os.path.dirname(__file__), 'img')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Primeira mensagem de boas-vindas com toque intrigante
    bot.send_message(
        message.chat.id, 
        "Hey 😉 Ready to see something a little... special? Just a taste. Let me know if you want more! 🍹"
    )
    
    # Criação dos botões de resposta
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Yes, show me 😏", callback_data="resposta_sim"),
        InlineKeyboardButton("Of course! 🌴", callback_data="resposta_claro")
    )
    
    # Pergunta para engajar o usuário com opções de resposta
    bot.send_message(message.chat.id, "You ready?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["resposta_sim", "resposta_claro"])
def handle_query(call):
    try:
        # Loop para enviar cada imagem na pasta de forma gradual
        for filename in os.listdir(image_folder):
            file_path = os.path.join(image_folder, filename)
            if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                with open(file_path, 'rb') as image:
                    bot.send_photo(call.message.chat.id, image)
                
                # Mensagem curta entre as fotos para manter o interesse
                bot.send_message(call.message.chat.id, "Just a peek... imagine the rest 🔥")
        
        # Chamada para ação após o envio de todas as imagens
        link_markup = InlineKeyboardMarkup()
        link_button = InlineKeyboardButton("Get the FULL collection... if you can handle it 🔥", url="https://malocastatus.gumroad.com/l/pack10picpremiere")
        link_markup.add(link_button)
        
        bot.send_message(
            call.message.chat.id,
            "You’ve seen just a glimpse... Imagine what’s waiting for you 😏. For only $10, unlock the *entire collection* and indulge yourself. You won’t regret it... 👀",
            reply_markup=link_markup,
            parse_mode="Markdown"
        )
        
        # Responde a interação do usuário no callback
        bot.answer_callback_query(call.id)
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Oops! Something went wrong: {e}")
        bot.answer_callback_query(call.id)

# Inicia o bot
bot.polling()
