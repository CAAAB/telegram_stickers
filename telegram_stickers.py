import telebot
import io
import os
from PIL import Image, ImageOps
import requests
import random

keep_bg = False
BOT_TOKEN = os.environ.get('BOT_TOKEN')
removebgkey = os.environ.get('REMOVEBGKEY')
removebg_keys = removebgkey.split(', ')
user_handle, user_name = os.environ.get('USER_INFO').split(", ")
my_username_noat = os.environ.get('MYUSERNAMENOAT')
my_telegram = os.environ.get("MY_TELEGRAM")
other_telegram = os.environ.get("OTHER_TELEGRAM")
mean_list = ["You are the reason everyone does everything without you","I'd explain it to you, but I don't have crayons","I can't depend on you to understand when you can't even tie your own shoelaces","You remind me of the sound a chalkboard makes when being scratched","Sorry, I can't comprehend your level of stupidity","If I threw a stick, would you leave?","Why don’t you check eBay and see if they have a life for sale","The best part of you ran down your mother's leg","You look like a 'before picture'","Your face looks like it was set on fire and put out with chains","Is your ass jealous of all the shit that comes out of your mouth?","You're about as useful as an ashtray on a motorcycle","Your birth certificate is an apology from the condom factory","If there’s a village looking for its idiot, I found you","I’d slap you, but that would be animal abuse","I wish I could get that time back from talking to you","You're so ugly, your portraits hang themselves","Your family tree must be a cactus because everyone on it is a prick","Even Bob the Builder can't fix your level of stupidity","I thought of you today... it reminded me to take out the garbage","Even evolution couldn't craft a creature with a feature as pitiful as yours","Did you fall from heaven? Because your face looks like it hit the ground first","Are you always this slow, or are you making a special effort today?","Somewhere out there, is a tree tirelessly producing oxygen for you. You owe it an apology","You're not the dumbest person on earth, but you sure better hope he doesn't die","Your birth was a waste of a good hospital bed","You're so dense, light bends around you","Every time I'm next to you, I get a fierce desire to be alone","I refuse to engage in a battle of wits with an unarmed person","You're as bright as a black hole, and twice as dense","You look like the failed first draft of an idiot's self-portrait","Your face is so ugly, even happy emojis frown","Two wrongs don't make a right, take your parents as an example","Congratulations on your new job! The zoo has been calling, they're wondering about their missing monkey","The chances of anyone loving you are the same as a snowball surviving in hell","You’re like Monday mornings, nobody likes you","You’re so ugly, when you got robbed, they made you wear the mask","I would rather be alone than be seen with you","I'd rather listen to nails on a chalkboard than hear your voice","You're so slow, even Internet Explorer tries to console you","Don't tell me what you think. I have no interest in the grotesque inner workings of your feeble mind","You're like a grey sky. Not because you're mysterious, but because people avoid looking at you","Even your shadow must be embarrassed to be seen with you","Listening to your opinions feels like a personal assault on my intelligence","Seeing you is a workout. I strain my eye muscles from rolling them so much","I don't know what your problem is, but I'm guessing it's hard to pronounce","You're so stupid, even Google wouldn't be able to find a solution for you","You're so insignificant, even atoms look down on you","How about you do us all a favor and go play a game of hide and go away?","Talking to you is like trying to explain quantum physics to a toddler","You're the poster child for birth control","If you were twice as smart, you'd still be stupid","Your voice is more irritating than a screaming baby on an airplane","Keep talking. I'm diagnosing you","You're so boring, even your shadow falls asleep on you","Your existence is as necessary as a white crayon","There's not a word yet, for how little you matter","Next time, leave your brain in charge. Your emotions are a terrible manager","You're as useful as a solar powered flashlight","Are you the dulled blade on the Swiss army knife of life?","Your presence is as welcoming as a shark in a swimming pool","You're as welcome as a toothache","You're the human equivalent of a participation award","If only your IQ was as high as your ego","Mirrors can't talk, thankfully for you, they can't laugh either","Any plan with you in it, is a bad plan","You could break steel, with your level of stupidity","I'd tell you to go to hell, but I'm afraid you'd just end up ruling the place","If I wanted to kill myself, I'd climb your ego and jump to your IQ level","You're like a penny, two-faced and worthless","If brains were dynamite, you wouldn't have enough to blow your hat off","I'd love to insult you, but nature did a better job","I don't believe in reincarnation, but in your case, I'm willing to make an exception","What did you do with all the brains God gave you? Stash them for a rainy day?","Your face is the reason horror movies will never go out of business","Your voice is the sound that drives people to deafness","I'd agree with you, but then we'd both be wrong","You're an emotional rollercoaster, except the ride only goes down","I'm not insulting you, I'm describing you","You're a few cards short of a full deck, aren't you?","As an outsider, what's your take on intelligence?","You're so slow, even a glacier could outrun you","Having a conversation with you is like trying to put toothpaste back into the tube","You light up a room. When you leave it","You'll never be half the man your mother was","Don’t act stupid, you're not pretending","The more I learn about you, the less I like you","The only thing dumber than your statements are your actions","If I had a face like yours, I'd probably make obscure claims too, just to distract people","You're more disappointing than an unsalted pretzel","You're like an unpaid bill. I don't want to see you, and I wish you'd go away","If stupidity were a crime, you'd be serving a life sentence","You're the reason the gene pool needs a lifeguard","Your IQ is miles from average – in the negative direction","You're an insult to all life forms out there, not just humans","If you spoke less, fewer people would realize how stupid you are","If you were any dumber, I'd have to water you twice a week","You're like sandpaper to people's spirits, always causing irritation","I don’t have the time or the crayons to explain it to you","You're those extra buttons on remote controls, absolutely pointless"]

def create_sticker_pack(bot, message, sticker_file_stream, pack_name, emojis):
    try:
        print(f"Creating a new sticker pack named {pack_name}...")
        bot.create_new_sticker_set(
            user_id=message.chat.id,
            name=f"{pack_name}_by_foxyflamingobot",
            title=pack_name,
            png_sticker=sticker_file_stream,
            emojis=emojis
        )
        print("Sticker pack created and sticker added successfully.")
    except Exception as e:
        print(f"Failed to create new sticker pack: {e}")
        bot.send_message(message.chat.id, f"Failed to create new sticker pack: {e}")


def add_sticker_to_pack(bot, message, sticker_file_stream, user_provided_pack_name, user_provided_emoji):
    try:
        # Extracting chat_id from the message object
        chat_id = message.chat.id

        # Send the sticker to the Telegram servers as a new file
        sent_message = bot.send_document(chat_id, sticker_file_stream)

        # Extract the file_id from the sent message
        sticker_file_id = sent_message.document.file_id

        full_pack_name = f"{user_provided_pack_name}_by_foxyflamingobot"

        # Create or add the sticker to the user-provided pack
        bot.add_sticker_to_set(user_id=chat_id, name=full_pack_name, png_sticker=sticker_file_id, emojis=user_provided_emoji)

        bot.send_message(chat_id, "Sticker successfully added to pack.")

    except Exception as e:
        print(f"Couldn't add the sticker to {full_pack_name}: {e}")
        bot.send_message(chat_id, f"Failed to add sticker to pack: {e}")


def add_or_create_sticker_to_pack(bot, message, sticker_file_stream, user_provided_pack_name, user_provided_emoji):
    chat_id = message.chat.id
    full_pack_name = f"{user_provided_pack_name}_by_foxyflamingobot"
    emoji_list = [e.strip() for e in user_provided_emoji.split(',')]

    try:
        # Send the sticker to the Telegram servers as a new file
        sent_message = bot.send_document(chat_id, sticker_file_stream)
        sticker_file_id = sent_message.document.file_id  # Extract the file_id from the sent message

        # Try adding the sticker to the existing pack
        bot.add_sticker_to_set(user_id=chat_id, name=full_pack_name, png_sticker=sticker_file_id, emojis=emoji_list)
        bot.send_message(chat_id, f"Sticker successfully added to pack [{full_pack_name}](https://t.me/addstickers/{full_pack_name}).", parse_mode='Markdown')


    except telebot.apihelper.ApiException as e:
        if 'STICKERSET_INVALID' in str(e):
            # Create the sticker pack and add the sticker
            bot.create_new_sticker_set(user_id=chat_id, name=full_pack_name, title=user_provided_pack_name, png_sticker=sticker_file_id, emojis=emoji_list)
            bot.send_message(chat_id, f"Sticker successfully added to new pack [{full_pack_name}](https://t.me/addstickers/{full_pack_name}).", parse_mode='Markdown')
        else:
            print(f"Failed to add sticker to pack: {e}")
            bot.send_message(chat_id, f"Failed to add sticker to pack: {e}")
    except Exception as e:
        print(f"Couldn't add the sticker to {full_pack_name}: {e}")
        bot.send_message(chat_id, f"Failed to add sticker to pack: {e}")

def delete_sticker_from_set(bot_token, file_id):
    data = {'sticker': file_id}
    response = requests.post(f'https://api.telegram.org/bot{bot_token}/deleteStickerFromSet', data=data)
    return response.json()

def remove_background(input_stream, output_stream, removebg_keys):
    for i, removebgkey in enumerate(removebg_keys):
        print(f"Attempting to remove background with key {i}...")
        input_stream.seek(0)  # Reset stream position to the start
        image = Image.open(input_stream)
        image.show()
        input_stream.seek(0)
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': input_stream},
            data={'size': 'auto'},
            headers={'X-Api-Key': removebgkey},
        )
        if response.status_code == requests.codes.ok:
            output_stream.write(response.content)
            output_stream.seek(0)
            print("Background removed successfully.")
            return output_stream
        else:
            print(f"Failed with key {i}. Status code: {response.status_code} - {response.text}")
    print("All keys exhausted. Failed to remove background.")
    return None

def resize_image(input_stream, output_stream):
    print("Attempting to resize image...")
    image = Image.open(input_stream)
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    max_size = 512
    target_size = (max_size, max_size)

    # Calculate padding
    aspect_ratio = image.width / image.height
    if image.width > image.height:
        new_width = max_size
        new_height = int(max_size / aspect_ratio)
    else:
        new_height = max_size
        new_width = int(max_size * aspect_ratio)

    # Resize the image
    image_resized = image.resize((new_width, new_height), Image.ANTIALIAS)

    # Create a new image with white background
    padded_img = Image.new("RGBA", target_size, (0, 0, 0, 0))

    # Paste the resized image into the center of the new image
    x_offset = (target_size[0] - image_resized.width) // 2
    y_offset = (target_size[1] - image_resized.height) // 2

    # Replace the above line with this
    temp_img = Image.new("RGBA", target_size)
    temp_img.paste(image_resized, (x_offset, y_offset))
    padded_img = Image.alpha_composite(padded_img, temp_img)

    # Save the output
    padded_img.save(output_stream, 'PNG')
    output_stream.seek(0)

    print(f"Image resized and padded successfully to {padded_img.size}")
    return output_stream


# Telegram bot setup
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print("Received start or help command.")
    #bot.reply_to(message, user_handle)
    bot.reply_to(message, "Hello! Send me an image to process, provide the name of the sticker pack the sticker should be added to and the corresponding emoji separated by a comma.")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.from_user.username == my_username_noat:
        bot.send_message(other_telegram, message.text)
    else:
        mean_message = random.choice(mean_list)
        bot.send_message(message.chat.id, mean_message) # Mean message
        bot.forward_message(my_telegram, message.chat.id, message.message_id) # Forward message
        bot.send_message(my_telegram, mean_message) # Mean message
        #bot.send_message(my_telegram, message.chat.id) # Send ID

@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    try:
        if message.from_user.username == user_handle:
            mean_message = random.choice(mean_list) + f", {user_name}"
            bot.send_message(message.chat.id, mean_message)
        bot.forward_message(my_telegram, message.chat.id, message.message_id)
        print("Received an image. Attempting to process...")

        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        original_image_stream = io.BytesIO(downloaded_file)
        resized_image_stream = io.BytesIO()
        no_bg_image_stream = io.BytesIO()

        keep_bg = False
        if message.caption:
            components = message.caption.split(',')
            pack_name = components[0].strip()
            emojis = components[1].strip()

            # Check if "keepbg" is in the caption as an optional argument
            if len(components) > 2 and "keepbg" in components[2].lower().strip():
                keep_bg = True
                print("Keeping background as per user request.")

        # Remove background
        if keep_bg:
            no_bg_image_stream = original_image_stream
        else:
            no_bg_image_stream = remove_background(original_image_stream, no_bg_image_stream, removebg_keys)

        # Resize the image
        resized_image_stream = resize_image(no_bg_image_stream, resized_image_stream)

        if resized_image_stream:
            print("Sending processed image back to user.")
            resized_image_stream.name = "processed_image.png"  # Set name attribute
            bot.send_document(message.chat.id, resized_image_stream, caption="Here's your processed image.")
            resized_image_stream.seek(0)
        else:
            print("Failed to process image.")
            bot.reply_to(message, 'Failed to remove background.')

        # Check if a message with sticker pack name and emojis is attached
        if message.caption:
            print('Caption detected')
            try:
                print(f"Attempting to add sticker to pack: {pack_name}")
                add_or_create_sticker_to_pack(bot, message, resized_image_stream, pack_name.strip(), emojis.strip())
            except ValueError:
                print("Could not extract pack name and emojis. Skipping sticker pack addition.")
                bot.send_message(message.chat.id, "Could not extract pack name and emojis. Skipping sticker pack addition.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                bot.send_message(message.chat.id, f"Oops, an error occurred: {e}")


    except Exception as e:
        print(f"An exception occurred: {e}")
        bot.send_message(message.chat.id, f'Oops, an error occurred: {e}')

@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    try:
        print("Received a sticker. Attempting to remove from pack...")

        sticker_file_id = message.sticker.file_id

        if message.from_user.username == my_username_noat:
            response = delete_sticker_from_set(BOT_TOKEN, sticker_file_id)
            if response.get('ok'):
                bot.send_message(message.chat.id, "Sticker successfully removed from pack.")
            else:
                bot.send_message(message.chat.id, f"Failed to remove sticker: {response.get('description')}")
        else:
            bot.send_message(message.chat.id, "You do not have the right to remove stickers.")

    except Exception as e:
        print(f"An exception occurred: {e}")
        bot.send_message(message.chat.id, f'Oops, an error occurred: {e}')

bot.polling()
