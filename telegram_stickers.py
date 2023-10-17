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

import telebot
import io
import os
from PIL import Image, ImageOps
import requests

keep_bg = False

def remove_background(input_stream, output_stream, removebgkey):
    print("Attempting to remove background...")
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
        print(f"Failed to remove background. Status code: {response.status_code}")
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
    bot.reply_to(message, "Hello! Send me an image to process.")

@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    try:
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
            no_bg_image_stream = remove_background(original_image_stream, no_bg_image_stream, removebgkey)

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
        
        response = delete_sticker_from_set(BOT_TOKEN, sticker_file_id)
        
        if response.get('ok'):
            bot.send_message(message.chat.id, "Sticker successfully removed from pack.")
        else:
            bot.send_message(message.chat.id, f"Failed to remove sticker: {response.get('description')}")

    except Exception as e:
        print(f"An exception occurred: {e}")
        bot.send_message(message.chat.id, f'Oops, an error occurred: {e}')



bot.polling()